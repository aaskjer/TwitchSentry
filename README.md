# TwitchSentry Bot List

Twitch accounts that [TwitchSentry](https://github.com/aaskjer/TwitchSentry) installations identified as bots, in three lists:

| List | What put an account there |
|---|---|
| `spam.json` / `spam.txt` | Spam Filter: a decisive hit (known spam domain, spam keyword, conversation scam, ...) |
| `lurkbots.json` / `lurkbots.txt` | LurkBot Filter: a bot-shaped name created on a known bot day, or with others the same day |
| `botwaves.json` / `botwaves.txt` | Follow Protection follow waves and Raid Protection spam swarms |

This branch is written automatically every few minutes and holds nothing else. Use it freely: the data is
dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).

## Was an account listed by mistake?

[Request its removal](https://github.com/aaskjer/TwitchSentry/issues/new?template=botlist-removal.yml). It comes off the list as soon as the request is read, every TwitchSentry
installation that banned it through this list lifts that ban, and the installations that reported it are
not counted for it again.

## Reading the lists

- `*.txt`: one login per line, only accounts at least **2 independent channels** reported.
  This is the list to import into a ban tool.
- `*.json`: every listed account, with `reports` (independent channels), `first`/`last` report day
  and `reasons`. One report is enough to appear here; TwitchSentry only bans from `banFrom` reports.
  Twitch ids are stable, logins are refreshed when an account renames.
- `index.json`: the current `version` and counts. Poll this file; the others only change with it.
  GitHub serves raw files with a five-minute cache, so polling faster gains nothing.
- `changes.json`: every change since version `since`, oldest first (`add`, `update`, `remove` with
  `why`: `removed` on request, `gone` from Twitch, `protected`, `dropped` when its reports were
  retracted or expired). A reader at `since` or later can catch up from this file alone.
- `removed.json`: ids removed on request in the last 365 days.

Partners, affiliates, Twitch staff and well-known service bots are never listed. Neither the reporting
channels nor any chat message are published.
