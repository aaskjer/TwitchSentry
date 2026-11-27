# Spam feed

`spam.json` in this folder is the list of new spam wording and detection patterns TwitchSentry hands to
every install. It is published to the [`feed` branch](https://github.com/aaskjer/TwitchSentry/tree/feed)
together with the language files and a `manifest.json` that names each file's SHA256. TwitchSentry looks
there every ten minutes, so a viewer-selling site that turns up next week reaches every channel within
about a quarter of an hour, without anybody importing a new version or opening the settings window.

## What it does on your PC

- **Every file is checked first.** A download whose size or SHA256 differs from the manifest is not
  used; TwitchSentry tries again a few minutes later.
- **Each entry is added to your `Machine Learning/spam.json` once.** It then shows up in the settings
  window like any other entry.
- **Deleting one is final.** The feed never hands the same entry over twice, so an entry you removed
  stays removed, whether you deleted it in the window, by chat command or by restoring a backup.
- **Nothing of yours is touched.** The feed only adds entries. The one exception is a retraction (see
  below), and that only takes back entries the feed itself put there.
- **A list your `spam.json` does not have yet is skipped**, not created. The settings window writes
  its lists on the next save, and the entries arrive after that.
- **Your regex lists stay yours.** `customPatterns` and `voucherPatterns` are never written by the feed.
  The feed's own patterns live apart from them (see below).
- **A new pattern watches before it counts.** For a day it only notes what it would have caught. Then it
  arms itself, or, with *Arm New Patterns Automatically* off, waits for you after 5 such messages. An
  armed pattern adds evidence in one part of an advert and never acts on its own. Arming a pattern or
  turning it off yourself stays as you left it.
- **A broken or suspicious feed is refused.** Your PC keeps the last good copy and logs a warning.

Three files on your PC belong to the feed:

| File | What it is |
|---|---|
| `Cache/spam-feed.json` | The last copy downloaded. Safe to delete; it comes back on the next check. |
| `Machine Learning/spam-feed-state.json` | The record of which entries the feed has already handed over. **Deleting it makes the feed offer every entry again, including the ones you removed.** |
| `Machine Learning/feed-patterns-state.json` | Each pattern's state: watching, waiting for you, armed or off, with what it would have caught. **Deleting it starts every pattern watching again.** |

## The format

```json
{
  "schema": 1,
  "version": 2,
  "updated": "2026-09-13",
  "lists": {
    "spamDomains": ["somesite"],
    "strongKeywords": ["somesite"]
  },
  "retracted": {
    "spamDomains": ["an-entry-that-was-a-mistake"]
  },
  "shipped": {
    "releases": ["v1.0.1", "v2.0.0"],
    "lists": {
      "keywords": ["a-built-in-default"]
    }
  },
  "patterns": [
    { "id": "some-pattern", "regex": "some\\s+site", "category": "destination", "about": "What it catches" }
  ]
}
```

- `schema` is the file format, and installs refuse a schema they do not know. `version` goes up by
  one with every change, and an install never swaps its copy for an older one.
- `lists` is cumulative: everything the feed hands over, not just what is new. An install that was
  offline for a month catches up in one go.
- `retracted` takes an entry back from installs that got it from the feed. An entry a streamer
  marked with `!` stays, because it is theirs now.
- `shipped` names every entry a release shipped as a built-in default, and the releases counted.
  Installs never hand one of these over, even if `lists` carried it by mistake: a streamer who
  deleted a default keeps it deleted. The settings window does not offer them for sharing either,
  and a share ticket that holds one leaves it out.
- The lists: `spamDomains`, `strongKeywords`, `keywords`, `spacedUrlTlds`, `beatRapport`,
  `beatCritique`, `beatSolution`, `beatPitch`, `handoffPhrases`, `serviceOffers`.
- `patterns`: at most 50. `id` is 3 to 40 of `a-z`, `0-9` and `-`. `regex` is at most 200 characters,
  matched case-insensitively with 50 ms per message, and may not match an empty message. `category` is
  the part of an advert it is evidence for: `destination`, `offer`, `instrument`, `tag` or `signature`.
  `about` is optional, at most 200 characters, and shown in the window and the notifications. A pattern
  that disappears from the feed disappears from every install; one whose `regex` or `category` changes
  watches again for a day.

## Publishing

`tools\publish-feed.ps1` publishes `spam.json` and the language files to the `feed` branch, with the
manifest. It runs `check-feed.ps1` first, which replays the spam corpus with every pattern armed and
refuses any pattern that counts in a single clean chat message.

The files go up in one commit and the manifest in a second one that names it (`"commit"`). Installs
download each file from that commit's address, which GitHub's cache cannot answer with an older copy.
The branch is only ever added to, so every commit a manifest named stays reachable.

Each language file is made for one release (`minClient`), because its texts are keyed by the settings
window's English texts. When those texts change, the files made for the release before move to
`Language/<release>/` on the branch, and installs still on that release keep reading them. A
generation older than the one the last stable release reads is removed.
