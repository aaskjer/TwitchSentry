"""Turns a TwitchSentry share ticket into a pull request.

.github/workflows/community-submissions.yml runs this whenever an issue carrying one of the share
labels is opened or edited. The ticket comes from one of the three forms in .github/ISSUE_TEMPLATE
(share-spam-list, share-profile, share-translation), typed in by hand or prefilled by the settings
window, and it becomes one file under Submissions/, on a branch of its own, in a pull request that
closes the ticket when it is merged.

Merging accepts a submission. It does not ship it: nothing under Submissions/ reaches an install.
Spam wording only gets into Feed/spam.json through a deliberate promotion step, because the feed
reaches every channel within hours.

Anyone with a GitHub account can open these tickets, so everything in one is untrusted. It is read
from the event file here rather than handed over on a command line, git and gh are called with
argument lists and never through a shell, and every piece of it that goes back into a pull request
or a comment sits inside a code fence, where a mention notifies nobody.

The entry rules mirror SpamFeedRules.IsValidEntry in TwitchSentry-SpamFilter.cs, which is not in
this repository. They are a first filter only - tools/check-feed.ps1 is still the gate before
anything is promoted - and tools/run-submission-tests.ps1 holds the two to the same verdicts.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata

SPAM_LISTS = ["spamDomains", "strongKeywords", "keywords", "spacedUrlTlds", "beatRapport",
              "beatCritique", "beatSolution", "beatPitch", "handoffPhrases", "serviceOffers"]
CANONICAL_LIST = {name.lower(): name for name in SPAM_LISTS}

MAX_ENTRY_LENGTH = 100
MAX_ENTRIES = 200
MAX_TEXT = 2000
MAX_PROFILE_CHARS = 60000
MAX_PROFILE_SETTINGS = 400

KIND_BY_LABEL = {
    "share: spam list": "spam",
    "share: profile": "profile",
    "share: translation": "translation",
}

# Each form field shows up in the ticket as a heading carrying the field's label. These have to match
# the `label:` of each field in the templates; test_submission.py checks that they still do.
FIELDS = {
    "spam": [("entries", "Entries"), ("context", "Where did it show up?"),
             ("version", "TwitchSentry version"), ("privacy", "Before you submit")],
    "profile": [("name", "Profile name"), ("purpose", "What is it for?"),
                ("profile", "Profile file"), ("privacy", "Before you submit")],
    "translation": [("language", "Language"), ("english", "The English text"),
                    ("current", "What it says now"), ("suggestion", "What it should say"),
                    ("why", "Why is it better?")],
}

FOLDER = {"spam": "spam", "profile": "profiles", "translation": "translations"}
NO_RESPONSE = "_No response_"

# TSSettings.ProfileExcluded and SecretNameParts in TwitchSentry-GUI.cs. The window's export already
# leaves all of these out; a pasted file that still carries one was edited by hand, or is not an export.
PROFILE_EXCLUDED = [
    "discordWebhookUrl", "discordWebhookName", "discordWebhookAvatarUrl",
    "virusTotalApiKey", "ipqsApiKey",
    "excludedUsers", "excludedGroups", "trustedUsers", "trustedRaiders", "whitelistDomains",
    "autoModWhitelist", "voteExcludedUsers", "voteExcludedGroups", "fgBlockedList",
    "learnerIgnoreTerms", "selfPermitRewardId",
    "useBotAccount", "DarkMode", "guiLanguage", "uiExpertMode", "dismissedHints",
    "settingsSchema", "activeProfile", "updateChannel", "logToFile", "backupFolder", "backupSettings",
    "backupLearned", "backupLanguages", "backupLogs", "backupCache",
    "dryRunEnabled", "dryRunMinutes",
]
SECRET_NAME_PARTS = ["apikey", "webhook", "token", "secret", "password"]
RESERVED_PROFILE_NAMES = ["Relaxed", "Balanced", "Strict", "Under Attack", "Just Chatting"]
WEBHOOK_PATTERN = re.compile(r"discord(?:app)?\.com/api/webhooks", re.I)


# ---------------------------------------------------------------------------------------------------
# The entry rules, as SpamFeedRules.IsValidEntry has them. .NET judges a string one UTF-16 unit at a
# time, so anything outside the Basic Multilingual Plane arrives there as a surrogate and is refused;
# refusing every code point above 0xFFFF here gives the same verdict.
# ---------------------------------------------------------------------------------------------------

def _is_net_whitespace(c):
    return c in "\t\n\x0b\x0c\r\x85" or unicodedata.category(c) in ("Zs", "Zl", "Zp")


def _net_trim(s):
    start, end = 0, len(s)
    while start < end and _is_net_whitespace(s[start]):
        start += 1
    while end > start and _is_net_whitespace(s[end - 1]):
        end -= 1
    return s[start:end]


def _net_lower(s):
    # ToLowerInvariant maps one character to one character; str.lower() may produce two.
    out = []
    for c in s:
        low = c.lower()
        out.append(low if len(low) == 1 else c)
    return "".join(out)


def _is_letter(c):
    return ord(c) <= 0xFFFF and unicodedata.category(c).startswith("L")


def _is_letter_or_digit(c):
    return ord(c) <= 0xFFFF and (unicodedata.category(c).startswith("L") or unicodedata.category(c) == "Nd")


def normalize(entry):
    """How an install stores an entry: trimmed, no '!' marker, lower case."""
    return _net_lower(_net_trim(_net_trim(entry or "").lstrip("!")))


def entry_problem(list_name, raw):
    """None when an install would accept the entry, otherwise a clause saying why it would not."""
    s = _net_trim(raw or "")
    if not s:
        return "is empty"
    if sum(2 if ord(c) > 0xFFFF else 1 for c in s) > MAX_ENTRY_LENGTH:
        return "is longer than %d characters" % MAX_ENTRY_LENGTH
    if s[0] == "!":
        return "starts with '!'"
    for c in s:
        if ord(c) > 0xFFFF or unicodedata.category(c) in ("Cc", "Cf", "Cs", "Co"):
            return "contains an invisible or special character"
    if not any(_is_letter(c) for c in s):
        return "has no letters in it"

    lower = _net_lower(s)
    if list_name == "spamDomains":
        bare = (len(lower) >= 4
                and all("a" <= c <= "z" or "0" <= c <= "9" or c in ".-" for c in lower)
                and lower[0] not in ".-" and lower[-1] not in ".-" and ".." not in lower)
        return None if bare else "is not a bare site name (4 or more of a-z, 0-9, '.' and '-')"
    if list_name == "spacedUrlTlds":
        ending = 2 <= len(lower) <= 24 and all("a" <= c <= "z" for c in lower)
        return None if ending else "is not a domain ending (2 to 24 letters a-z)"

    if len(lower) < 4:
        return "is shorter than 4 characters"
    for c in lower:
        if _is_letter_or_digit(c) or c == " " or c == "\u2019" or c in "'-.,!?&:/+":
            continue
        return "contains a character no phrase needs"
    if "  " in lower:
        return "has a double space in it"
    return None


# ---------------------------------------------------------------------------------------------------
# Reading the ticket
# ---------------------------------------------------------------------------------------------------

def parse_form(body, fields):
    """The value under each field's heading, looked for in template order. None for a missing heading."""
    text = (body or "").replace("\r\n", "\n")
    found = []
    start = 0
    for key, label in fields:
        match = re.compile(r"^### " + re.escape(label) + r"[ \t]*$", re.M).search(text, start)
        if match:
            found.append((key, match.start(), match.end()))
            start = match.end()
    values = {key: None for key, _ in fields}
    for i, (key, _, end) in enumerate(found):
        stop = found[i + 1][1] if i + 1 < len(found) else len(text)
        value = text[end:stop].strip()
        values[key] = "" if value == NO_RESPONSE else value
    return values


def unfence(value):
    """A textarea with `render:` arrives wrapped in a code fence; this takes the fence off."""
    match = re.match(r"^(`{3,}|~{3,})[^\n]*\n(.*?)\n?\1[ \t]*$", (value or "").strip(), re.S)
    return match.group(2) if match else (value or "")


def is_checked(value):
    return bool(re.search(r"^\s*- \[[xX]\] ", value or "", re.M))


def clip(text, limit):
    text = (text or "").replace("\r\n", "\n").strip()
    return text if len(text) <= limit else text[:limit]


def printable(text, limit=60):
    """For quoting a piece of the ticket back in a list: no control characters, no backticks."""
    out = []
    for c in text or "":
        if unicodedata.category(c) in ("Cc", "Cf"):
            out.append("?")
        elif c == "`":
            out.append("'")
        else:
            out.append(c)
    s = "".join(out)
    return s if len(s) <= limit else s[:limit] + "..."


def version_of(value):
    match = re.match(r"^\s*v?(\d+\.\d+\.\d+(?:-[A-Za-z0-9.]+)?)\s*$", value or "")
    return "v" + match.group(1) if match else None


class Result:
    def __init__(self, kind):
        self.kind = kind
        self.problems = []
        self.document = None
        self.path = None
        self.title = None
        self.summary = None
        self.nothing_new = None


def read_json(path, default):
    try:
        with open(path, encoding="utf-8-sig") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def _sets(block):
    block = block if isinstance(block, dict) else {}
    return {name: {normalize(e) for e in (block.get(name) or []) if isinstance(e, str)} for name in SPAM_LISTS}


def build_spam(issue, values, root):
    result = Result("spam")
    if not is_checked(values.get("privacy")):
        result.problems.append("The box saying the entries hold no chat message and no username is not ticked.")

    text = values.get("entries") or ""
    if not text.strip():
        result.problems.append("There are no entries.")

    entries, counts, seen = {}, {}, set()
    for number, line in enumerate(text.split("\n"), 1):
        if not line.strip():
            continue
        stats = {}
        if "|" in line:
            line, _, tail = line.partition("|")
            for key, val in re.findall(r"\b(users|clean)\s*=\s*(\d{1,9})\b", tail):
                stats[key] = int(val)
        match = re.match(r"^\s*([A-Za-z]+)\s*:(.*)$", line)
        if not match:
            result.problems.append("Line %d is not written as `list: entry`." % number)
            continue
        name = CANONICAL_LIST.get(match.group(1).lower())
        if name is None:
            result.problems.append("Line %d: `%s` is not one of the lists." % (number, printable(match.group(1), 30)))
            continue
        # A copy out of the streamer's own spam.json may carry the '!' that protects it from decay.
        entry = normalize(match.group(2))
        why = entry_problem(name, entry)
        if why:
            result.problems.append("Line %d: `%s` %s." % (number, printable(entry), why))
            continue
        if (name, entry) in seen:
            continue
        seen.add((name, entry))
        entries.setdefault(name, []).append(entry)
        if stats:
            counts.setdefault(name, {})[entry] = stats

    if len(seen) > MAX_ENTRIES:
        result.problems.append("That is %d entries; one ticket takes up to %d." % (len(seen), MAX_ENTRIES))
    if result.problems:
        return result

    feed = read_json(os.path.join(root, "Feed", "spam.json"), {})
    listed, retracted = _sets(feed.get("lists")), _sets(feed.get("retracted"))
    fresh, known, withdrawn = {}, {}, {}
    for name in SPAM_LISTS:
        for entry in entries.get(name, []):
            if entry in listed[name] and entry not in retracted[name]:
                known.setdefault(name, []).append(entry)
            else:
                fresh.setdefault(name, []).append(entry)
                if entry in retracted[name]:
                    withdrawn.setdefault(name, []).append(entry)

    if not fresh:
        result.nothing_new = known
        return result

    number = issue["number"]
    document = {
        "type": "spam list",
        "issue": number,
        "submittedBy": issue["user"]["login"],
        "submittedAt": issue.get("created_at"),
        "entries": fresh,
    }
    kept_counts = {name: {e: c for e, c in counts.get(name, {}).items() if e in fresh.get(name, [])} for name in fresh}
    kept_counts = {name: c for name, c in kept_counts.items() if c}
    if kept_counts:
        document["counts"] = kept_counts
    version = version_of(values.get("version"))
    if version:
        document["twitchSentry"] = version
    context = clip(values.get("context"), 1000)
    if context:
        document["context"] = context

    total = sum(len(v) for v in fresh.values())
    result.document = document
    result.path = "Submissions/spam/%d.json" % number
    result.title = "Spam wording from #%d (%d %s)" % (number, total, "entry" if total == 1 else "entries")

    lines = ["**Spam wording** shared in #%d by %s." % (number, issue["user"]["login"]), ""]
    lines += ["| List | New | Already in the feed |", "|---|---|---|"]
    for name in SPAM_LISTS:
        if name in fresh or name in known:
            lines.append("| `%s` | %d | %d |" % (name, len(fresh.get(name, [])), len(known.get(name, []))))
    lines += ["", "New:", fence("\n".join("%s: %s" % (n, e) for n in SPAM_LISTS for e in fresh.get(n, [])))]
    if known:
        lines += ["Already in the feed, so left out of the file:",
                  fence("\n".join("%s: %s" % (n, e) for n in SPAM_LISTS for e in known.get(n, [])))]
    if withdrawn:
        lines += ["**Retracted from the feed before** - kept, for you to judge:",
                  fence("\n".join("%s: %s" % (n, e) for n in SPAM_LISTS for e in withdrawn.get(n, [])))]
    if context:
        lines += ["Where it showed up:", fence(context)]
    lines += ["Checked here: the list names and the rules every install applies to an entry. "
              "**Not checked:** defaults a release already shipped, and the spam corpus - "
              "`tools/check-feed.ps1` covers both when this is promoted into the feed."]
    result.summary = "\n".join(lines)
    return result


def build_profile(issue, values, root):
    result = Result("profile")
    if not is_checked(values.get("privacy")):
        result.problems.append("The box saying the profile holds no key, webhook or list of people is not ticked.")

    name = _net_trim(values.get("name") or "")
    if not name:
        result.problems.append("The profile has no name.")
    elif len(name) > 40:
        result.problems.append("The name is longer than 40 characters.")
    elif any(unicodedata.category(c) in ("Cc", "Cf") or c in '\\/:*?"<>|`' for c in name):
        result.problems.append("The name holds a character a file name cannot.")
    elif name.lower() in [n.lower() for n in RESERVED_PROFILE_NAMES]:
        result.problems.append("`%s` is one of the built-in stances; give it a name of its own." % printable(name))

    purpose = clip(values.get("purpose"), 1000)
    if not purpose:
        result.problems.append("There is nothing under *What is it for?*.")

    raw = unfence(values.get("profile"))
    profile = None
    if not raw.strip():
        result.problems.append("There is no profile file.")
    elif len(raw) > MAX_PROFILE_CHARS:
        result.problems.append("The profile is longer than any export from the window.")
    else:
        try:
            profile = json.loads(raw, object_pairs_hook=_no_duplicate_keys)
        except ValueError as ex:
            result.problems.append("The profile is not valid JSON (%s)." % printable(str(ex), 80))

    settings = None
    if profile is not None:
        if not isinstance(profile, dict) or profile.get("twitchSentryProfile") != 1 or not isinstance(profile.get("settings"), dict):
            result.problems.append("That is not a TwitchSentry profile. Paste the whole file the Export button writes.")
        else:
            settings = profile["settings"]
            result.problems += _profile_setting_problems(settings)

    if result.problems:
        return result

    number = issue["number"]
    carried = {"twitchSentryProfile": 1, "name": name}
    version = version_of(profile.get("twitchSentry") if isinstance(profile.get("twitchSentry"), str) else None)
    if version:
        carried["twitchSentry"] = version
    carried["settings"] = settings
    result.document = {
        "type": "profile",
        "issue": number,
        "submittedBy": issue["user"]["login"],
        "submittedAt": issue.get("created_at"),
        "name": name,
        "purpose": purpose,
        "profile": carried,
    }
    result.path = "Submissions/profiles/%d.json" % number
    result.title = "Profile \"%s\" from #%d" % (printable(name, 40).replace('"', "'"), number)
    result.summary = "\n".join([
        "**A profile** shared in #%d by %s: %d settings%s." % (number, issue["user"]["login"], len(settings),
                                                             ", exported from " + version if version else ""),
        "", "Name:", fence(name), "What it is for:", fence(purpose),
        "Checked here: it is a profile export, and it carries no key, webhook, token or list of people - "
        "the same filter the window applies on import. Read the settings through before merging."
    ])
    return result


def _no_duplicate_keys(pairs):
    keys = [k for k, _ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError("a key appears twice")
    return dict(pairs)


def _profile_setting_problems(settings):
    problems = []
    if len(settings) > MAX_PROFILE_SETTINGS:
        return ["The profile carries %d settings, more than the window has." % len(settings)]
    for key, value in settings.items():
        if not re.match(r"^[A-Za-z][A-Za-z0-9_]{0,63}$", key):
            problems.append("`%s` is not a setting name." % printable(key, 40))
            continue
        if key in PROFILE_EXCLUDED:
            problems.append("It carries `%s`, which a profile never shares." % key)
            continue
        if isinstance(value, str) and any(part in key.lower() for part in SECRET_NAME_PARTS):
            problems.append("It carries `%s`, which looks like a key or a webhook." % key)
            continue
        items = value if isinstance(value, list) else [value]
        if isinstance(value, list) and len(value) > 200:
            problems.append("`%s` holds more items than any setting does." % key)
            continue
        for item in items:
            if isinstance(item, (dict, list)):
                problems.append("`%s` holds a value no setting has." % key)
                break
            if isinstance(item, str) and (len(item) > MAX_TEXT or WEBHOOK_PATTERN.search(item)):
                problems.append("`%s` holds text that does not belong in a shared profile." % key)
                break
    return problems


def build_translation(issue, values, root):
    result = Result("translation")
    index = read_json(os.path.join(root, "Language", "index.json"), [])
    codes = [str(e.get("code")) for e in index if isinstance(e, dict) and e.get("code") and e.get("code") != "en"]

    match = re.search(r"\(([A-Za-z]{2,3}(?:-[A-Za-z]{2,4})?)\)\s*$", values.get("language") or "")
    code = match.group(1) if match else None
    if code not in codes:
        result.problems.append("Pick one of the languages TwitchSentry has.")

    english = clip(values.get("english"), MAX_TEXT)
    current = clip(values.get("current"), MAX_TEXT)
    suggestion = clip(values.get("suggestion"), MAX_TEXT)
    why = clip(values.get("why"), 1000)
    if not english:
        result.problems.append("The English text is missing.")
    if not suggestion:
        result.problems.append("There is nothing under *What it should say*.")
    elif current and suggestion == current:
        result.problems.append("The suggestion is the same as what it says now.")
    for label, text in (("The English text", english), ("What it should say", suggestion)):
        if any(unicodedata.category(c) == "Cf" or (unicodedata.category(c) == "Cc" and c not in "\n\t") for c in text):
            result.problems.append("*%s* holds an invisible character." % label)
    if result.problems:
        return result

    english_file = read_json(os.path.join(root, "Language", "en.json"), {})
    known = isinstance(english_file, dict) and english in english_file

    number = issue["number"]
    document = {
        "type": "translation",
        "issue": number,
        "submittedBy": issue["user"]["login"],
        "submittedAt": issue.get("created_at"),
        "language": code,
        "english": english,
        "suggestion": suggestion,
    }
    if current:
        document["current"] = current
    if why:
        document["why"] = why
    result.document = document
    result.path = "Submissions/translations/%d.json" % number
    result.title = "Translation (%s) from #%d" % (code, number)
    lines = ["**A translation fix** for `%s`, shared in #%d by %s." % (code, number, issue["user"]["login"]), "",
             "The English text:", fence(english)]
    if current:
        lines += ["What it says now:", fence(current)]
    lines += ["What it should say:", fence(suggestion)]
    if why:
        lines += ["Why:", fence(why)]
    lines.append("The English text is %s the published `Language/en.json`%s." % (
        "in" if known else "**not** in",
        "" if known else " - it may belong to a window newer than that file, or be copied inexactly"))
    result.summary = "\n".join(lines)
    return result


BUILDERS = {"spam": build_spam, "profile": build_profile, "translation": build_translation}


def without_lone_surrogates(text):
    # Valid UTF-8 cannot carry one, but a JSON escape in the event can, and a single one would stop the
    # file from being written at all.
    return "".join(c for c in (text or "") if not 0xD800 <= ord(c) <= 0xDFFF)


def build(kind, issue, root):
    values = parse_form(without_lone_surrogates(issue.get("body")), FIELDS[kind])
    missing = [label for key, label in FIELDS[kind] if values[key] is None]
    if missing:
        result = Result(kind)
        result.problems.append("The ticket no longer has the form's parts (missing: %s). "
                               "Open a new one from the form rather than editing the headings."
                               % ", ".join("*%s*" % m for m in missing))
        return result
    return BUILDERS[kind](issue, values, root)


def fence(text):
    """A code fence longer than any run of backticks inside, so nothing in the text can close it."""
    longest = max([len(run) for run in re.findall(r"`+", text or "")] + [0])
    ticks = "`" * max(3, longest + 1)
    return "%s text\n%s\n%s\n" % (ticks, text or "", ticks)


def kind_of(issue):
    for label in issue.get("labels") or []:
        kind = KIND_BY_LABEL.get((label or {}).get("name"))
        if kind:
            return kind
    return None


# ---------------------------------------------------------------------------------------------------
# Talking to git and GitHub
# ---------------------------------------------------------------------------------------------------

def run(args, check=True):
    return subprocess.run(args, check=check, text=True, capture_output=True)


def write_temp(text):
    handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False)
    with handle:
        handle.write(text)
    return handle.name


def comment(repo, number, text):
    run(["gh", "issue", "comment", str(number), "--repo", repo, "--body-file", write_temp(text)])


def problems_comment(result):
    return "\n".join(["This ticket could not be turned into a pull request yet:", ""]
                     + ["- " + p for p in result.problems]
                     + ["", "Edit the ticket to put it right, and it is checked again."])


def publish(result, issue, repo, base, root):
    number = issue["number"]
    branch = "submission/%d" % number
    content = json.dumps(result.document, ensure_ascii=False, indent=2) + "\n"

    # An edit that changed nothing about the file must not force-push the branch again.
    fetched = run(["git", "fetch", "--depth=1", "origin", "+refs/heads/%s:refs/remotes/origin/%s" % (branch, branch)], check=False)
    unchanged = False
    if fetched.returncode == 0:
        shown = run(["git", "show", "origin/%s:%s" % (branch, result.path)], check=False)
        unchanged = shown.returncode == 0 and shown.stdout == content

    if not unchanged:
        target = os.path.join(root, *result.path.split("/"))
        os.makedirs(os.path.dirname(target), exist_ok=True)
        run(["git", "checkout", "-B", branch])
        with open(target, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        run(["git", "add", result.path])
        run(["git", "-c", "user.name=github-actions[bot]",
             "-c", "user.email=41898282+github-actions[bot]@users.noreply.github.com",
             "commit", "-m", "Add submission #%d (%s)" % (number, result.kind)])
        run(["git", "push", "--force", "origin", "HEAD:refs/heads/%s" % branch])

    body = "\n".join(["Closes #%d" % number, "", result.summary])
    listed = run(["gh", "pr", "list", "--repo", repo, "--head", branch, "--state", "open", "--json", "number,url"])
    existing = json.loads(listed.stdout or "[]")
    if existing:
        run(["gh", "pr", "edit", str(existing[0]["number"]), "--repo", repo,
             "--title", result.title, "--body-file", write_temp(body)])
        return existing[0]["url"], False
    created = run(["gh", "pr", "create", "--repo", repo, "--base", base, "--head", branch,
                   "--title", result.title, "--body-file", write_temp(body)])
    return created.stdout.strip().splitlines()[-1], True


def main():
    with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as f:
        event = json.load(f)
    issue = event.get("issue") or {}
    kind = kind_of(issue)
    if issue.get("state") != "open" or issue.get("pull_request") or kind is None:
        print("Not an open share ticket - nothing to do.")
        return 0

    repo = os.environ["GITHUB_REPOSITORY"]
    base = (event.get("repository") or {}).get("default_branch") or "main"
    root = os.environ.get("GITHUB_WORKSPACE") or os.getcwd()
    number = issue["number"]
    result = build(kind, issue, root)

    try:
        if result.problems:
            print("Ticket #%d has %d problem(s); telling the submitter." % (number, len(result.problems)))
            comment(repo, number, problems_comment(result))
            return 0
        if result.nothing_new is not None:
            print("Ticket #%d holds nothing the feed lacks." % number)
            comment(repo, number, "\n".join([
                "Thank you - every entry here is already in the spam feed, so there is nothing new to add:", "",
                fence("\n".join("%s: %s" % (n, e) for n in SPAM_LISTS for e in result.nothing_new.get(n, []))),
                "This ticket can be closed."]))
            return 0

        url, created = publish(result, issue, repo, base, root)
        print("Ticket #%d is %s" % (number, url))
        if created:
            comment(repo, number, "Thank you! This is now a pull request: %s\n\n"
                                  "Merging it accepts the submission and closes this ticket. Editing the ticket "
                                  "updates the pull request." % url)
        return 0
    except subprocess.CalledProcessError as ex:
        print("Failed: %s\n%s" % (" ".join(ex.cmd[:3]), (ex.stderr or "").strip()), file=sys.stderr)
        try:
            comment(repo, number, "Something went wrong turning this ticket into a pull request. "
                                  "The maintainer can see what in the workflow run.")
        except subprocess.CalledProcessError:
            pass
        return 1


if __name__ == "__main__":
    sys.exit(main())
