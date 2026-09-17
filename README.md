# Submissions

What streamers shared from TwitchSentry for the maintainer to accept, one file per ticket. Every ticket from the share forms becomes a pull request into this branch, and merging it accepts the submission and closes the ticket. Accepted is **not** shipped: no install reads this branch.

| Folder | From the form | What happens next |
|---|---|---|
| `spam/` | Share spam wording | Entries that hold up, best of all sent by more than one streamer, are promoted into the [spam feed](https://github.com/aaskjer/TwitchSentry/blob/main/Feed/README.md) with a version bump, after `tools/check-feed.ps1` and the spam corpus. |
| `translations/` | Suggest a better translation | Applied to the language files in the next language update. |

**Profiles do not come here.** Nobody has to accept a profile, so one that passes the check is stored on the [`profiles` branch](https://github.com/aaskjer/TwitchSentry/tree/profiles) straight away.
