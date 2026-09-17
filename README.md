# Submissions
What streamers shared from TwitchSentry for the maintainer to accept, one file per ticket. Every ticket from the share forms becomes a pull request into this branch, and merging it accepts the submission and closes the ticket. Accepted is **not** shipped: no install reads this branch.
| Folder | From the form | What happens next |
|---|---|---|
| `spam/` | Share spam wording | Entries that hold up, best of all sent by more than one streamer, are promoted into the [spam feed](https://github.com/aaskjer/TwitchSentry/blob/main/Feed/README.md) with a version bump, after `tools/check-feed.ps1` and the spam corpus. |
| `translations/` | Suggest a better translation | Applied to the language files in the next language update. |

**Profiles do not come here.** Nobody has to accept a profile, so one that passes the check is stored on the [`profiles` branch](https://github.com/aaskjer/TwitchSentry/tree/profiles) straight away.

## How a ticket becomes a file

`.github/workflows/community-submissions.yml` on `main` runs `.github/scripts/submission.py` whenever a ticket from one of the share forms is opened or edited. It reads the form, writes `<folder>/<ticket number>.json` on the branch `submission/<ticket number>`, which starts from this one, and opens a pull request into this branch. Editing the ticket updates the pull request; a ticket with a mistake in it gets a comment saying what to fix instead.

GitHub only closes the ticket a pull request names when the pull request goes into `main`, so the workflow closes it itself once a pull request into this branch is merged. One closed without merging leaves its ticket open.

Pull requests need **Settings → Actions → General → Allow GitHub Actions to create and approve pull requests** switched on.

This branch shares no history with `main`. The workflow wrote this page and writes it again whenever its wording changes, so change it in `submission.py` rather than here.

## What is checked, and what is not

- **Spam wording:** the list names, and the rules every install applies to an entry. Entries already in the feed, and defaults a release already shipped (the feed's `shipped` block), are left out of the file. The spam corpus is left to the promotion step.
- **Translations:** that the language exists, and whether the English text is in the published `Language/en.json`.
