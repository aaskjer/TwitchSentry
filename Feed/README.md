# Spam feed

`spam.json` in this folder is the list of new spam wording TwitchSentry hands to every install. The
Spam Filter looks at it every three hours, so a viewer-selling site that turns up next week reaches
every channel without anybody importing a new version.

## What it does on your PC

- **Each entry is added to your `Machine Learning/spam.json` once.** It then shows up in the settings
  window like any other entry.
- **Deleting one is final.** The feed never hands the same entry over twice, so an entry you removed
  stays removed, whether you deleted it in the window, by chat command or by restoring a backup.
- **Nothing of yours is touched.** The feed only adds entries. The one exception is a retraction (see
  below), and that only takes back entries the feed itself put there.
- **A list your `spam.json` does not have yet is skipped**, not created. The settings window writes
  its lists on the next save, and the entries arrive after that.
- **Regex lists never come from here.** `customPatterns` and `voucherPatterns` stay yours alone.
- **A broken or suspicious feed is refused.** Your PC keeps the last good copy and logs a warning.

Two files on your PC belong to the feed:

| File | What it is |
|---|---|
| `Cache/spam-feed.json` | The last copy downloaded from here. Safe to delete; it comes back on the next check. |
| `Machine Learning/spam-feed-state.json` | The record of which entries the feed has already handed over. **Deleting it makes the feed offer every entry again, including the ones you removed.** |

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
  }
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

# This is not in the final build yet
