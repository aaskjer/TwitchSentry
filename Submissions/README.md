# Submissions

What streamers shared from TwitchSentry, one file per ticket. A merged pull request lands a file here, and that means the submission was accepted - **not** that it reached anyone. No install reads this folder.

| Folder | From the form | What happens next |
|---|---|---|
| `spam/` | Share spam wording | Entries that hold up, best of all sent by more than one streamer, are promoted into the [spam feed](../Feed/README.md) with a version bump, after `tools/check-feed.ps1` and the spam corpus. |
| `translations/` | Suggest a better translation | Applied to the language files in the next language update. |

**Profiles do not come here.** A profile changes nothing about TwitchSentry, so there is nothing to accept: once it passes the check it is committed straight to the [`profiles` branch](https://github.com/aaskjer/TwitchSentry/tree/profiles) as `<ticket number>.json`, a file the Profiles dialog imports as it is, and its ticket is closed. That branch shares no history with `main`.

## How a ticket becomes a file

`.github/workflows/community-submissions.yml` runs `.github/scripts/submission.py` whenever a ticket from one of the share forms is opened or edited. For spam wording and translations it reads the form, writes `<folder>/<ticket number>.json` on the branch `submission/<ticket number>`, and opens a pull request that closes the ticket when it is merged. Editing the ticket updates the pull request; a ticket with a mistake in it gets a comment saying what to fix instead.

Pull requests need **Settings → Actions → General → Allow GitHub Actions to create and approve pull requests** switched on. Profiles do not: the workflow's own write access to the repository is all the `profiles` branch takes, and the first profile shared creates it.

## What is checked here, and what is not

- **Spam wording:** the list names, and the rules every install applies to an entry. Entries already in the feed, and defaults a release already shipped (the feed's `shipped` block), are left out of the file. The spam corpus is left to the promotion step.
- **Profiles:** that it is a TwitchSentry profile, and that it carries no key, webhook, token or list of people - the same filter the settings window applies when it imports one. Nobody reviews the policy inside before it is stored.
- **Translations:** that the language exists, and whether the English text is in the published `Language/en.json`.
