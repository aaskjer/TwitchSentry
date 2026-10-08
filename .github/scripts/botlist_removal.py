#!/usr/bin/env python3
"""Takes the accounts a removal ticket names off the shared bot list, through the relay, and says so on the ticket.

Run by .github/workflows/botlist-removal.yml. The ticket is read from the event file; everything in it is
untrusted, and only names that are Twitch logins ever reach the relay or a comment.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
import urllib.error
import urllib.request

RELAY_URL = "https://botlist.twitchsentry.workers.dev/v1/remove"
LABEL = "botlist: removal"
FIELDS = [("accounts", "Accounts"), ("why", "Why is it not a bot?")]
NO_RESPONSE = "_No response_"
MAX_NAMES = 50
LOGIN = re.compile(r"^[a-z0-9_]{1,25}$")
GITHUB_LOGIN = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")


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


def names_of(text):
    """Logins in the order given, each once; an @ or a channel address comes off. The rest is returned as unreadable."""
    names, unreadable = [], []
    for raw in re.split(r"[\s,;]+", text or ""):
        word = raw.strip().strip("`")
        if not word:
            continue
        lowered = word.lower()
        at = lowered.find("twitch.tv/")
        if at >= 0:
            lowered = re.split(r"[/?#]", lowered[at + len("twitch.tv/"):])[0]
        name = lowered.lstrip("@")
        if not name:
            continue
        if LOGIN.match(name):
            if name not in names:
                names.append(name)
        elif word not in unreadable:
            unreadable.append(word)
    return names, unreadable


def printable(text, limit=40):
    """For quoting a piece of the ticket back: no control characters, no backticks."""
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


def ask_relay(names, number, by, key, url=RELAY_URL):
    """The relay's status and answer; status 0 when it could not be reached at all."""
    payload = json.dumps({"names": names, "issue": number, "by": by}).encode("utf-8")
    request = urllib.request.Request(url, data=payload, method="POST", headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + key,
        "User-Agent": "TwitchSentry-BotList-Removal",
    })
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.status, json.loads(response.read().decode("utf-8") or "null")
    except urllib.error.HTTPError as ex:
        try:
            return ex.code, json.loads(ex.read().decode("utf-8") or "null")
        except ValueError:
            return ex.code, None
    except (urllib.error.URLError, OSError, ValueError):
        return 0, None


def codes(names):
    return ", ".join("`%s`" % printable(n) for n in names)


def answer(result, unreadable):
    """The comment for a removal the relay carried out."""
    removed = [a.get("login") or a.get("id") for a in result.get("removed") or []]
    cleared = [a.get("login") or a.get("id") for a in result.get("cleared") or []]
    unlisted = list(result.get("unlisted") or [])
    lines = []
    if removed:
        lines.append("Taken off the shared bot list: %s. Every TwitchSentry installation that banned %s through the list "
                     "lifts that ban within minutes, and the channels that reported %s are not counted for %s again."
                     % (codes(removed), "it" if len(removed) == 1 else "them", "it" if len(removed) == 1 else "them",
                        "it" if len(removed) == 1 else "them"))
    if cleared:
        lines.append("Reported but not on the list yet: %s. Those reports are dropped, so %s will not be listed from them."
                     % (codes(cleared), "it" if len(cleared) == 1 else "they"))
    if unlisted:
        lines.append("Not on the list at all: %s." % codes(unlisted))
    if unreadable:
        lines.append("Not Twitch names, so left alone: %s." % codes(unreadable))
    if (removed or cleared) and not result.get("committed"):
        lines.append("The list on GitHub is written again within a few minutes.")
    return "\n\n".join(lines)


def run(args):
    return subprocess.run(args, check=True, text=True, encoding="utf-8", errors="replace", capture_output=True)


def write_temp(text):
    handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False)
    with handle:
        handle.write(text)
    return handle.name


def comment(repo, number, text, gh=run):
    gh(["gh", "issue", "comment", str(number), "--repo", repo, "--body-file", write_temp(text)])


def close(repo, number, gh=run):
    gh(["gh", "issue", "close", str(number), "--repo", repo, "--reason", "completed"])


def handle(event, repo, key, relay=ask_relay, gh=run):
    """0 when the ticket was dealt with or is not one of ours, 1 when it has to be tried again."""
    issue = event.get("issue") or {}
    labels = [l.get("name") for l in issue.get("labels") or []]
    if issue.get("state") != "open" or issue.get("pull_request") or LABEL not in labels:
        print("Not an open removal ticket - nothing to do.")
        return 0
    number = issue["number"]
    key = (key or "").strip()
    if not key:
        print("BOTLIST_REMOVAL_KEY is not set for this repository - nothing can be removed.", file=sys.stderr)
        return 1

    values = parse_form(issue.get("body"), FIELDS)
    names, unreadable = names_of(values.get("accounts"))
    if not names:
        comment(repo, number, "No Twitch name could be read in this ticket%s. Edit it to name the accounts, one per line, "
                              "and it is read again." % (" (" + codes(unreadable[:5]) + ")" if unreadable else ""), gh)
        return 0
    if len(names) > MAX_NAMES:
        comment(repo, number, "This ticket names %d accounts; at most %d go into one. Edit it down, or split it into "
                              "several tickets." % (len(names), MAX_NAMES), gh)
        return 0

    login = (issue.get("user") or {}).get("login") or ""
    status, result = relay(names, number, login if GITHUB_LOGIN.match(login) else None, key)
    if status != 200 or not isinstance(result, dict) or not result.get("ok"):
        print("The relay answered %s: %s" % (status, json.dumps(result)[:300]), file=sys.stderr)
        comment(repo, number, "Nothing was removed yet: the bot list did not take the request just now. It is tried "
                              "again as soon as the ticket is edited.", gh)
        return 1

    print("Ticket #%d: removed %d, cleared %d, not listed %d." % (
        number, len(result.get("removed") or []), len(result.get("cleared") or []), len(result.get("unlisted") or [])))
    comment(repo, number, answer(result, unreadable), gh)
    close(repo, number, gh)
    return 0


def main():
    with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as f:
        event = json.load(f)
    try:
        return handle(event, os.environ["GITHUB_REPOSITORY"], os.environ.get("BOTLIST_REMOVAL_KEY", ""))
    except subprocess.CalledProcessError as ex:
        print("Failed: %s\n%s" % (" ".join(ex.cmd[:3]), (ex.stderr or "").strip()), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
