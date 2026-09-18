"""Turns a TwitchSentry share ticket into a pull request, or a shared profile into a file.

.github/workflows/community-submissions.yml runs this whenever an issue carrying one of the share
labels is opened or edited, and when a pull request into the submissions branch is merged. The ticket
comes from one of the three forms in .github/ISSUE_TEMPLATE (share-spam-list, share-profile,
share-translation), typed in by hand or prefilled by the settings window.

Spam wording and translations become one file in a pull request into the submissions branch. Merging it
accepts the submission, and this script closes the ticket then, because GitHub only acts on "Closes #N"
in a pull request into main. Accepting does not ship anything: no install reads that branch. Spam
wording only gets into Feed/spam.json through a deliberate promotion step, because the feed reaches
every channel within hours.

A profile is not a change to TwitchSentry, so nobody has to accept it: once it passes the check it is
committed straight to the profiles branch as <ticket number>.json, a file the Profiles dialog imports
as it is, and the ticket is closed.

Both branches start from a commit of their own and share no history with main, so nothing shared ever
lands on the branch every install reads.

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

# Where each kind that goes through a pull request keeps its files on the submissions branch.
FOLDER = {"spam": "spam", "translation": "translations"}
NO_RESPONSE = "_No response_"

SUBMISSION_BRANCH = "submissions"
PROFILE_BRANCH = "profiles"
# The branch a ticket's pull request comes from. Only this script names a branch so.
TICKET_BRANCH = re.compile(r"^submission/(\d{1,9})$")
PUSH_ATTEMPTS = 5
# The tree with nothing in it. Git knows it without having it stored, so a branch can start from a commit
# that shares nothing with main.
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
BOT_IDENTITY = ["-c", "user.name=github-actions[bot]",
                "-c", "user.email=41898282+github-actions[bot]@users.noreply.github.com"]
SETTING_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,63}$")
# The characters GitHub allows in an account name. The name comes from the event, but it goes into a
# commit message and a Markdown link, so anything else is left out rather than trusted.
GITHUB_LOGIN = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")

# TSSettings' Dictionary<string, double> settings: the Custom stop of each sensitivity slider, a dial's
# setting name to its number. The only settings whose value is an object. tools/profile_filter_parity.py
# holds this list to the window's.
PROFILE_NUMBER_MAPS = ["fgCustomPreset", "mgCustomPreset", "rfCustomPreset", "spamCustomPreset"]

# TSSettings.ProfileExcluded and SecretNameParts in TwitchSentry-GUI.cs. The window's export already
# leaves all of these out; a pasted file that still carries one was edited by hand, or is not an export.
PROFILE_EXCLUDED = [
    "discordWebhookUrl", "discordWebhookName", "discordWebhookAvatarUrl",
    "virusTotalApiKey", "ipqsApiKey",
    "excludedUsers", "excludedGroups", "trustedUsers", "trustedRaiders", "whitelistDomains",
    "autoModWhitelist", "voteExcludedUsers", "voteExcludedGroups", "fgBlockedList",
    "learnerIgnoreTerms", "selfPermitRewardId",
    "useBotAccount", "DarkMode", "guiLanguage", "uiExpertMode", "dismissedHints",
    "settingsSchema", "activeProfile", "updateChannel", "backupFolder", "backupSettings",
    "backupLearned", "backupLanguages", "backupLogs", "backupCache",
    "dryRunEnabled", "dryRunMinutes",
    "spamFeedEnabled",
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
        self.already_shipped = None
        # What another ticket has already put forward: spam entries as list -> entry -> ticket, and for a
        # translation the ticket that says the same thing, or one that says something else about the same text.
        self.already_in = {}
        self.same_as = None
        self.answered_differently = None


def read_json(path, default):
    try:
        with open(path, encoding="utf-8-sig") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def _sets(block):
    block = block if isinstance(block, dict) else {}
    return {name: {normalize(e) for e in (block.get(name) or []) if isinstance(e, str)} for name in SPAM_LISTS}


def listing(block):
    """Entries grouped by list, one `list: entry` per line, in the order the lists are known."""
    return "\n".join("%s: %s" % (name, entry) for name in SPAM_LISTS for entry in block.get(name, []))


def build_spam(issue, values, root, elsewhere=None):
    elsewhere = elsewhere or Elsewhere()
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
    # What releases shipped as built-in defaults. The feed never hands one of those over - a streamer who
    # deleted one would get it back - so a default is no use to the promotion step, however good it is.
    shipped_block = feed.get("shipped") if isinstance(feed.get("shipped"), dict) else {}
    knows_shipped = isinstance(shipped_block.get("lists"), dict)
    shipped = _sets(shipped_block.get("lists"))
    fresh, known, defaults, withdrawn = {}, {}, {}, {}
    for name in SPAM_LISTS:
        for entry in entries.get(name, []):
            if entry in shipped[name]:
                defaults.setdefault(name, []).append(entry)
            elif entry in listed[name] and entry not in retracted[name]:
                known.setdefault(name, []).append(entry)
            else:
                fresh.setdefault(name, []).append(entry)
                if entry in retracted[name]:
                    withdrawn.setdefault(name, []).append(entry)

    # An entry another ticket has already put forward is not offered again: the same wording in two files is
    # two things to judge and one streamer counted twice. It is named in the ticket instead, and the file
    # records that this account saw it too, which is what "more than one streamer sent it" is counted from.
    repeated = {}
    for name in list(fresh):
        for entry in list(fresh[name]):
            ticket = elsewhere.spam.get(name, {}).get(entry)
            if ticket is None or ticket == issue["number"]:
                continue
            fresh[name].remove(entry)
            repeated.setdefault(name, {})[entry] = ticket
        if not fresh[name]:
            del fresh[name]
    result.already_in = repeated

    if not fresh:
        result.nothing_new = known
        result.already_shipped = defaults
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
    if repeated:
        document["seconds"] = {name: sorted(entries) for name, entries in repeated.items()}
    version = version_of(values.get("version"))
    if version:
        document["twitchSentry"] = version
    context = clip(values.get("context"), 1000)
    if context:
        document["context"] = context

    total = sum(len(v) for v in fresh.values())
    result.document = document
    result.path = "%s/%d.json" % (FOLDER["spam"], number)
    result.title = "Spam wording from #%d (%d %s)" % (number, total, "entry" if total == 1 else "entries")

    lines = ["**Spam wording** shared in #%d by %s." % (number, issue["user"]["login"]), ""]
    lines += ["| List | New | Already in the feed | A shipped default |", "|---|---|---|---|"]
    for name in SPAM_LISTS:
        if name in fresh or name in known or name in defaults:
            lines.append("| `%s` | %d | %d | %d |" % (name, len(fresh.get(name, [])), len(known.get(name, [])),
                                                    len(defaults.get(name, []))))
    lines += ["", "New:", fence(listing(fresh))]
    if known:
        lines += ["Already in the feed, so left out of the file:", fence(listing(known))]
    if defaults:
        lines += ["Built-in defaults of a TwitchSentry release, so left out of the file - the feed never hands one over:",
                  fence(listing(defaults))]
    if repeated:
        lines += ["Another ticket has these in hand already, so they are left out of the file - this ticket is a "
                  "second streamer seeing them, which the file records under `seconds`:",
                  fence("\n".join("%s: %s (#%d)" % (name, entry, ticket)
                                  for name in SPAM_LISTS for entry, ticket in sorted(repeated.get(name, {}).items())))]
    if withdrawn:
        lines += ["**Retracted from the feed before** - kept, for you to judge:", fence(listing(withdrawn))]
    if context:
        lines += ["Where it showed up:", fence(context)]
    if knows_shipped:
        lines += ["Checked here: the list names, the rules every install applies to an entry, and the defaults "
                  "releases shipped. **Not checked:** the spam corpus - `tools/check-feed.ps1` runs it when this "
                  "is promoted into the feed."]
    else:
        lines += ["Checked here: the list names and the rules every install applies to an entry. "
                  "**Not checked:** defaults a release already shipped (`Feed/spam.json` has no `shipped` block yet), "
                  "and the spam corpus - `tools/check-feed.ps1` covers both when this is promoted into the feed."]
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
        result.problems.append("`%s` is one of the built-in profiles; give it a name of its own." % printable(name))

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
    version = version_of(profile.get("twitchSentry") if isinstance(profile.get("twitchSentry"), str) else None)
    # The stored file is itself a profile: the marker, the name and the settings are all the window's
    # import reads, and it passes over the rest. So a streamer downloads it and uses it as it is.
    document = {"twitchSentryProfile": 1, "name": name}
    if version:
        document["twitchSentry"] = version
    document["purpose"] = purpose
    document["issue"] = number
    document["submittedBy"] = issue["user"]["login"]
    document["submittedAt"] = issue.get("created_at")
    document["settings"] = settings
    result.document = document
    result.path = "%d.json" % number
    result.title = "Profile \"%s\" from #%d" % (printable(name, 40).replace('"', "'"), number)
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
        if not SETTING_NAME.match(key):
            problems.append("`%s` is not a setting name." % printable(key, 40))
            continue
        if key in PROFILE_EXCLUDED:
            problems.append("It carries `%s`, which a profile never shares." % key)
            continue
        if key in PROFILE_NUMBER_MAPS:
            if not _is_number_map(value):
                problems.append("`%s` holds a value no setting has." % key)
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


def _is_number_map(value):
    """A Custom slider stop as the window writes it: dial names to finite numbers, and nothing else."""
    if not isinstance(value, dict) or len(value) > 64:
        return False
    for name, number in value.items():
        if not SETTING_NAME.match(name) or isinstance(number, bool) or not isinstance(number, (int, float)):
            return False
        if number != number or number in (float("inf"), float("-inf")):
            return False
    return True


def build_translation(issue, values, root, elsewhere=None):
    elsewhere = elsewhere or Elsewhere()
    result = Result("translation")
    index = read_json(os.path.join(root, "Language", "index.json"), [])
    # English is a language file like the others: en.json can word a text differently from the code.
    codes = [str(e.get("code")) for e in index if isinstance(e, dict) and e.get("code")]

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

    # The same text in the same language is one decision, so a second ticket saying the same thing adds nothing.
    # One saying something else does: both wordings belong in front of whoever picks.
    for other in elsewhere.translations:
        if other.get("issue") == issue["number"] or other.get("language") != code or other.get("english") != english:
            continue
        if other.get("suggestion") == suggestion:
            result.same_as = other.get("issue")
            return result
        result.answered_differently = other.get("issue")

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
    result.path = "%s/%d.json" % (FOLDER["translation"], number)
    result.title = "Translation (%s) from #%d" % (code, number)
    lines = ["**A translation fix** for `%s`, shared in #%d by %s." % (code, number, issue["user"]["login"]), "",
             "The English text:", fence(english)]
    if current:
        lines += ["What it says now:", fence(current)]
    lines += ["What it should say:", fence(suggestion)]
    if why:
        lines += ["Why:", fence(why)]
    if result.answered_differently:
        lines += ["**#%d wants something else for the same text.** Both are here to pick from; only one of them "
                  "can end up in the language file." % result.answered_differently, ""]
    lines.append("The English text is %s the published `Language/en.json`%s." % (
        "in" if known else "**not** in",
        "" if known else " - it may belong to a window newer than that file, or be copied inexactly"))
    result.summary = "\n".join(lines)
    return result


BUILDERS = {"spam": build_spam, "profile": build_profile, "translation": build_translation}


class Elsewhere:
    """What other tickets have already put forward, so nothing is proposed twice: spam entries as
    list -> entry -> ticket, and the translation documents as they were written."""

    def __init__(self):
        self.spam = {}
        self.translations = []

    def add(self, document):
        if not isinstance(document, dict) or not isinstance(document.get("issue"), int):
            return
        if document.get("type") == "spam list":
            for name, entries in (document.get("entries") or {}).items():
                for entry in entries if isinstance(entries, list) else []:
                    self.spam.setdefault(name, {}).setdefault(entry, document["issue"])
            # A ticket that only seconded an entry counts as having it in hand too.
            for name, entries in (document.get("seconds") or {}).items():
                for entry in entries if isinstance(entries, list) else []:
                    self.spam.setdefault(name, {}).setdefault(entry, document["issue"])
        elif document.get("type") == "translation":
            self.translations.append(document)


def without_lone_surrogates(text):
    # Valid UTF-8 cannot carry one, but a JSON escape in the event can, and a single one would stop the
    # file from being written at all.
    return "".join(c for c in (text or "") if not 0xD800 <= ord(c) <= 0xDFFF)


def build(kind, issue, root, elsewhere=None):
    values = parse_form(without_lone_surrogates(issue.get("body")), FIELDS[kind])
    missing = [label for key, label in FIELDS[kind] if values[key] is None]
    if missing:
        result = Result(kind)
        result.problems.append("The ticket no longer has the form's parts (missing: %s). "
                               "Open a new one from the form rather than editing the headings."
                               % ", ".join("*%s*" % m for m in missing))
        return result
    if kind == "profile":
        return BUILDERS[kind](issue, values, root)
    return BUILDERS[kind](issue, values, root, elsewhere)


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

def run(args, check=True, cwd=None):
    # UTF-8 whatever the machine's locale says: what `git show` prints is compared with what this script
    # would write, and the front pages carry characters outside ASCII.
    return subprocess.run(args, check=check, text=True, encoding="utf-8", errors="replace", capture_output=True, cwd=cwd)


def write_temp(text):
    handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False)
    with handle:
        handle.write(text)
    return handle.name


def comment(repo, number, text):
    run(["gh", "issue", "comment", str(number), "--repo", repo, "--body-file", write_temp(text)])


def problems_comment(result):
    opening = ("This profile could not be stored yet:" if result.kind == "profile"
               else "This ticket could not be turned into a pull request yet:")
    return "\n".join([opening, ""]
                     + ["- " + p for p in result.problems]
                     + ["", "Edit the ticket to put it right, and it is checked again."])


def stored_comment(address, repo, result):
    raw = "https://raw.githubusercontent.com/%s/%s/%s" % (repo, PROFILE_BRANCH, result.path)
    return "\n".join([
        "Thank you! The profile is stored: %s" % address, "",
        "Anyone can use it from there, you included: download the file (%s) and put it into `Settings/Profiles` "
        "in the TwitchSentry folder, or pick it with *Import* in ☰ → *Profiles*." % raw, "",
        "This ticket is closed now. To share a newer version, share it again from the window.",
    ])


def accepted_comment(kind, number, pull, repo):
    address = "https://github.com/%s/blob/%s/%s/%d.json" % (repo, SUBMISSION_BRANCH, FOLDER[kind], number)
    merged = "#%d" % pull["number"] if isinstance(pull.get("number"), int) else "The pull request"
    next_step = ("The entries are weighed together with what other streamers sent, and the ones that hold up go "
                 "into the spam feed every TwitchSentry install receives." if kind == "spam"
                 else "The fix goes into the language files with the next language update.")
    return "\n".join(["Thank you! %s was merged, so this is accepted: %s" % (merged, address), "", next_step])


def same_as_comment(ticket):
    return ("Thank you - #%d says the same about the same text, and is waiting to be picked up. "
            "Two tickets for one decision is one too many, so this one can be closed.\n\n"
            "If you meant to word it differently, edit this ticket: it is checked again every time." % ticket)


def nothing_new_comment(result):
    lines = ["Thank you - there is nothing here the spam feed could add.", ""]
    if result.already_in:
        lines += ["Another ticket has these in hand already:",
                  fence("\n".join("%s: %s (#%d)" % (name, entry, ticket)
                                  for name in SPAM_LISTS for entry, ticket in sorted(result.already_in.get(name, {}).items())))]
    if result.nothing_new:
        lines += ["Already in the spam feed:", fence(listing(result.nothing_new))]
    if result.already_shipped:
        lines += ["Built-in defaults of a TwitchSentry release. The feed never hands one of those over, "
                  "so a streamer who deleted one keeps it deleted:", fence(listing(result.already_shipped))]
    lines.append("This ticket can be closed.")
    return "\n".join(lines)


def submission_files(ref):
    """The submission files on that ref, as their text. One listing for the whole tree, because every call here
    is a git process and this runs for every ticket."""
    listed = run(["git", "ls-tree", "-r", "--name-only", ref], check=False)
    if listed.returncode != 0:
        return
    folders = tuple(folder + "/" for folder in FOLDER.values())
    for path in (listed.stdout or "").splitlines():
        if not path.startswith(folders) or not path.endswith(".json"):
            continue
        shown = run(["git", "show", "%s:%s" % (ref, path)], check=False)
        if shown.returncode == 0:
            yield shown.stdout


def elsewhere_of(repo, mine):
    """What the other tickets have put forward: what is accepted on the submissions branch, and what waits in
    an open pull request. The ticket's own branch is left out, so an edit is not compared with itself."""
    elsewhere = Elsewhere()

    def collect(ref):
        for text in submission_files(ref):
            try:
                elsewhere.add(json.loads(text))
            except ValueError:
                pass

    if fetch_branch(SUBMISSION_BRANCH):
        collect("origin/" + SUBMISSION_BRANCH)

    listed = run(["gh", "pr", "list", "--repo", repo, "--state", "open", "--base", SUBMISSION_BRANCH,
                  "--json", "headRefName"], check=False)
    try:
        open_branches = [pull.get("headRefName") for pull in json.loads(listed.stdout or "[]")]
    except ValueError:
        open_branches = []
    for branch in open_branches:
        if not branch or branch == mine or not TICKET_BRANCH.match(branch):
            continue
        if fetch_branch(branch):
            collect("origin/" + branch)
    return elsewhere


def publish(result, issue, repo):
    """Opens a pull request into the submissions branch for a checked submission, or brings the open one up
    to date. Returns its address, and whether it is new."""
    number = issue["number"]
    branch = "submission/%d" % number
    content = json.dumps(result.document, ensure_ascii=False, indent=2) + "\n"

    # The branch the pull request goes into. The first submission ever shared starts it, and its front page
    # is written again whenever this script words it differently.
    readme = submissions_readme(repo)
    if commit_to_branch(SUBMISSION_BRANCH, lambda work: write_file(work, "README.md", readme),
                        "Describe the submissions branch", lambda: shown(SUBMISSION_BRANCH, "README.md") == readme):
        # So the pull request's branch starts from the front page just pushed, not from before it.
        fetch_branch(SUBMISSION_BRANCH)

    # An edit that changed nothing about the file must not force-push the branch again.
    if not (fetch_branch(branch) and shown(branch, result.path) == content):
        work = tempfile.mkdtemp(prefix="ts-submission-")
        run(["git", "worktree", "add", "--detach", work, "refs/remotes/origin/%s" % SUBMISSION_BRANCH])
        try:
            write_file(work, result.path, content)
            run(["git", "add", "--all"], cwd=work)
            run(["git"] + BOT_IDENTITY + ["commit", "-m", "Add submission #%d (%s)%s" % (number, result.kind, from_account(issue))],
                cwd=work)
            run(["git", "push", "--force", "origin", "HEAD:refs/heads/%s" % branch], cwd=work)
        finally:
            run(["git", "worktree", "remove", "--force", work], check=False)

    # No "Closes #N": GitHub ignores it in a pull request into any branch but main. close_accepted() does
    # that part once this is merged.
    body = "\n".join(["Merging this accepts the submission and closes #%d." % number, "", result.summary])
    listed = run(["gh", "pr", "list", "--repo", repo, "--head", branch, "--state", "open", "--json", "number,url"])
    existing = json.loads(listed.stdout or "[]")
    if existing:
        run(["gh", "pr", "edit", str(existing[0]["number"]), "--repo", repo,
             "--title", result.title, "--body-file", write_temp(body)])
        return existing[0]["url"], False
    created = run(["gh", "pr", "create", "--repo", repo, "--base", SUBMISSION_BRANCH, "--head", branch,
                   "--title", result.title, "--body-file", write_temp(body)])
    return created.stdout.strip().splitlines()[-1], True


def store_profile(result, issue, repo):
    """Commits a checked profile to the profiles branch. Returns the file's address, and whether anything
    was written."""
    content = json.dumps(result.document, ensure_ascii=False, indent=2) + "\n"
    address = "https://github.com/%s/blob/%s/%s" % (repo, PROFILE_BRANCH, result.path)

    def write(work):
        write_file(work, result.path, content)
        write_file(work, "README.md", profiles_readme(work, repo))

    # GitHub shows a file's last commit message beside it in the branch, so who shared a profile can be
    # read off the file list without opening anything.
    stored = commit_to_branch(PROFILE_BRANCH, write, "Store profile #%d%s" % (issue["number"], from_account(issue)),
                              # An edit that changed nothing about the profile writes nothing.
                              lambda: shown(PROFILE_BRANCH, result.path) == content)
    return address, stored


def commit_to_branch(branch, write, message, unchanged):
    """Commits what write(folder) puts into a checkout of the branch, and says whether it did. Nothing is
    written when unchanged() finds the branch already holding it.

    A branch that does not exist yet starts from a commit with no parent and nothing in it, so it carries
    none of main. The checkout is a worktree of its own, which leaves main's checkout as it is. Another run
    can land a commit between the fetch and the push: a refused push starts over from the branch as it is
    then, and since every ticket owns its own file, starting over loses nobody's."""
    remote = "refs/remotes/origin/%s" % branch
    refused = ""
    for _ in range(PUSH_ATTEMPTS):
        if not fetch_branch(branch):
            # If another run starts the branch first, this push is refused and the next fetch finds theirs.
            start = run(["git"] + BOT_IDENTITY + ["commit-tree", EMPTY_TREE, "-m", "Start the %s branch" % branch])
            started = run(["git", "push", "origin", "%s:refs/heads/%s" % (start.stdout.strip(), branch)], check=False)
            if started.returncode != 0:
                refused = started.stderr or ""
                if refused_by_rules(refused):
                    break
            continue

        if unchanged():
            return False

        work = tempfile.mkdtemp(prefix="ts-%s-" % branch)
        run(["git", "worktree", "add", "--detach", work, remote])
        try:
            write(work)
            run(["git", "add", "--all"], cwd=work)
            run(["git"] + BOT_IDENTITY + ["commit", "-m", message], cwd=work)
            pushed = run(["git", "push", "origin", "HEAD:refs/heads/%s" % branch], cwd=work, check=False)
        finally:
            run(["git", "worktree", "remove", "--force", work], check=False)
        if pushed.returncode == 0:
            return True
        refused = pushed.stderr or ""
        if refused_by_rules(refused):
            break
    # What GitHub said goes into the run's log. "The branch kept moving" was the guess this used to print,
    # and a push the repository rules refuse looks nothing like a lost race.
    raise subprocess.CalledProcessError(1, ["git", "push", "origin", branch],
                                        stderr=refused.strip() or "the push was refused and git gave no reason")


def fetch_branch(branch):
    """Whether origin has the branch. When it does, origin/<branch> is up to date afterwards."""
    return run(["git", "fetch", "origin", "+refs/heads/%s:refs/remotes/origin/%s" % (branch, branch)], check=False).returncode == 0


def shown(branch, path):
    """A file as the fetched branch holds it, or None when it holds no such file."""
    answer = run(["git", "show", "origin/%s:%s" % (branch, path)], check=False)
    return answer.stdout if answer.returncode == 0 else None


def write_file(folder, path, text):
    target = os.path.join(folder, *path.split("/"))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def from_account(issue):
    """The ' from <account>' a commit message ends with. The name comes from the event, so one GitHub would
    never issue is left out rather than trusted."""
    login = (issue.get("user") or {}).get("login") or ""
    return " from " + login if GITHUB_LOGIN.match(login) else ""


def refused_by_rules(stderr):
    """A push GitHub turns away over a ruleset or a protected branch. Trying again changes nothing."""
    text = (stderr or "").lower()
    return "gh013" in text or "rule violation" in text or "protected ref" in text or "protected branch" in text


def profiles_readme(folder, repo):
    """The branch's front page: what the files are, how to use one, and every profile on it, newest first."""
    rows = []
    for file_name in os.listdir(folder):
        match = re.match(r"^(\d+)\.json$", file_name)
        doc = read_json(os.path.join(folder, file_name), None) if match else None
        if isinstance(doc, dict) and isinstance(doc.get("name"), str):
            rows.append((int(match.group(1)), file_name, doc))
    rows.sort(key=lambda row: row[0], reverse=True)

    lines = [
        "# Shared profiles", "",
        "Settings profiles streamers shared from TwitchSentry: how strict to be, one file per profile. Take one, "
        "try it, keep it or go back - your own settings are one *Import* away again.", "",
        "**Use one:** open the file, press *Download raw file*, and drop it into `Settings/Profiles` in your "
        "TwitchSentry folder. It is then in ☰ → *Profiles* in the settings window, which lists every setting it "
        "would change before you pick it.", "",
        "**Share yours:** ☰ → *Share...* in the settings window, *My settings as a profile*. It fills the form in "
        "for you, and once the check passes the profile appears here. This list is public and the name is all "
        "anyone sees before they open the file, so name it after the channel it suits: *Small English chat, strict "
        "on links* tells somebody whether to try it, *test2* tells them nothing. The name is yours to change in "
        "the form before you submit it.", "",
        "**What a profile carries:** the policy - sensitivity, actions, timings, which modules do what. Never a key, "
        "a webhook, an account name or any list naming people or sites; every file here was checked for that, the "
        "same way the settings window checks one you import. What the policy itself does is your call, not ours.", "",
        "Nothing in this branch reaches an installation by itself, and it has no history in common with `main`.", "",
        "| Profile | Shared by | Shared in | Exported from |",
        "|---|---|---|---|",
    ]
    for number, file_name, doc in rows:
        version = doc.get("twitchSentry") if isinstance(doc.get("twitchSentry"), str) else "-"
        login = doc.get("submittedBy") if isinstance(doc.get("submittedBy"), str) else ""
        shared_by = "[%s](https://github.com/%s)" % (login, login) if GITHUB_LOGIN.match(login) else "-"
        lines.append("| [`%s`](%s) | %s | [#%d](https://github.com/%s/issues/%d) | %s |" % (
            printable(doc["name"], 40).replace("|", "/"), file_name, shared_by, number, repo, number,
            printable(version, 20).replace("|", "/")))
    return "\n".join(lines) + "\n"


def submissions_readme(repo):
    """The submissions branch's front page. Nothing on it comes from a ticket, so it only changes when this
    script's wording does."""
    lines = [
        "# Submissions", "",
        "Spam wording and translation fixes streamers shared from TwitchSentry, one file per ticket, waiting to be "
        "taken up. Accepted here is not shipped: nothing in this branch reaches an installation.", "",
        "| Folder | Shared through | Where it goes from here |",
        "|---|---|---|",
        "| `spam/` | ☰ → *Share...*, spam wording from your lists | Weighed against what other streamers sent. "
        "What holds up is published in the [spam feed](https://github.com/%s/blob/main/Feed/README.md), which every "
        "installation receives within hours. |" % repo,
        "| `translations/` | ☰ → *Share...*, a better translation | Into the language files, with the next "
        "language update. |", "",
        "**How a file gets here:** the share form fills a ticket in, the ticket becomes a pull request into this "
        "branch, and merging it takes the submission up and closes the ticket. Editing the ticket updates its pull "
        "request; a ticket with a mistake in it is answered with what to correct instead.", "",
        "**What was checked:** for spam wording, that every entry is one an installation would accept, and that "
        "TwitchSentry does not already carry it. For a translation, that the language exists, and whether the "
        "English text is one the settings window really shows. Whether the wording deserves to reach every channel "
        "is the judgement the merge stands for - that is the whole point of the wait.", "",
        "**Profiles are not collected here.** A profile changes nothing about TwitchSentry, so nobody has to take "
        "it up: it goes straight to the [`profiles` branch](https://github.com/%s/tree/profiles)." % repo, "",
        "This branch has no history in common with `main`, and this page is written by the share workflow.",
    ]
    return "\n".join(lines) + "\n"


def accepted_ticket(pull, repo):
    """The ticket a merged pull request into the submissions branch accepted, or None. Only a branch this
    script pushed counts: a pull request from a fork decides nothing about a ticket, whatever its branch is
    called."""
    head = pull.get("head") or {}
    if pull.get("merged") is not True or (pull.get("base") or {}).get("ref") != SUBMISSION_BRANCH:
        return None
    if ((head.get("repo") or {}).get("full_name") or "").lower() != repo.lower():
        return None
    match = TICKET_BRANCH.match(head.get("ref") or "")
    return int(match.group(1)) if match else None


def close_accepted(pull, repo):
    number = accepted_ticket(pull, repo)
    if number is None:
        print("Not a merged submission - nothing to do.")
        return 0
    viewed = run(["gh", "issue", "view", str(number), "--repo", repo, "--json", "state,labels"])
    ticket = json.loads(viewed.stdout or "{}")
    kind = kind_of(ticket)
    if ticket.get("state") != "OPEN" or kind not in FOLDER:
        print("#%d is not an open spam or translation ticket - left as it is." % number)
        return 0
    comment(repo, number, accepted_comment(kind, number, pull, repo))
    run(["gh", "issue", "close", str(number), "--repo", repo, "--reason", "completed"])
    print("Ticket #%d is accepted and closed." % number)
    return 0


def main():
    with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as f:
        event = json.load(f)
    repo = os.environ["GITHUB_REPOSITORY"]
    if event.get("pull_request") is not None:
        try:
            return close_accepted(event["pull_request"], repo)
        except subprocess.CalledProcessError as ex:
            print("Failed: %s\n%s" % (" ".join(ex.cmd[:3]), (ex.stderr or "").strip()), file=sys.stderr)
            return 1

    issue = event.get("issue") or {}
    kind = kind_of(issue)
    if issue.get("state") != "open" or issue.get("pull_request") or kind is None:
        print("Not an open share ticket - nothing to do.")
        return 0

    root = os.environ.get("GITHUB_WORKSPACE") or os.getcwd()
    number = issue["number"]

    try:
        elsewhere = None if kind == "profile" else elsewhere_of(repo, "submission/%d" % number)
        result = build(kind, issue, root, elsewhere)

        if result.same_as is not None:
            print("Ticket #%d says what #%d already says." % (number, result.same_as))
            comment(repo, number, same_as_comment(result.same_as))
            return 0
        if result.problems:
            print("Ticket #%d has %d problem(s); telling the submitter." % (number, len(result.problems)))
            comment(repo, number, problems_comment(result))
            return 0
        if result.nothing_new is not None:
            print("Ticket #%d holds nothing the feed could add." % number)
            comment(repo, number, nothing_new_comment(result))
            return 0

        if kind == "profile":
            url, stored = store_profile(result, issue, repo)
            print("Ticket #%d is %s" % (number, url))
            if stored:
                comment(repo, number, stored_comment(url, repo, result))
                run(["gh", "issue", "close", str(number), "--repo", repo, "--reason", "completed"])
            return 0

        url, created = publish(result, issue, repo)
        print("Ticket #%d is %s" % (number, url))
        if created:
            comment(repo, number, "Thank you! This is now a pull request: %s\n\n"
                                  "Merging it accepts the submission and closes this ticket. Editing the ticket "
                                  "updates the pull request." % url)
        return 0
    except subprocess.CalledProcessError as ex:
        print("Failed: %s\n%s" % (" ".join(ex.cmd[:3]), (ex.stderr or "").strip()), file=sys.stderr)
        try:
            comment(repo, number, ("Something went wrong storing this profile. " if kind == "profile"
                                   else "Something went wrong turning this ticket into a pull request. ")
                    + "The maintainer can see what in the workflow run.")
        except subprocess.CalledProcessError:
            pass
        return 1


if __name__ == "__main__":
    sys.exit(main())
