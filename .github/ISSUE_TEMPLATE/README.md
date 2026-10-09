# Issue templates

These are **issue forms** (`.yml`), not the older Markdown templates. Keep it that way: a
`bug_report.md` or `feature_request.md` beside them would show up as a second choice for the same thing.

## The dropdown has to match the settings window

`Which part is it about?` lists exactly what `IssueAreas` in `TwitchSentry-GUI.cs` lists, in the same
order. `tools/check-compile.ps1` fails if the two ever drift, because a reporter coming from the
window and one coming from here have to be able to pick the same answer.

## Labels these expect to exist

The window sends the area along as a label, and **GitHub silently drops a label the repository does
not have**. Create these, or the area survives only as the `**Area:**` line in the body:

- `message-filter` - Message Filter
- `spam` - Spam Scoring and Learner
- `raid-protection` - Raid Protection
- `follow-protection` - Follow Protection
- `lurkbot-filter` - LurkBot Filter
- `word-filter` - Word Filter
- `bot-list` - Shared Bot List
- `links` - Link Filter and Check Link
- `automod` - AutoMod
- `twitch-warn` - Twitch Warn
- `permit` - Permit
- `voting` - Voting
- `chat-commands` - Chat Commands
- `offline-protection` - Offline Protection
- `deck` - Deck Buttons and OBS Dock
- `discord` - Discord Alerts
- `windows-notifications` - Windows Notifications
- `settings-window` - The settings window
- `translations` - A translation

`Not sure` sends no area label. `bug` and `enhancement` are GitHub's own and already there.

## Do not switch blank issues off

`config.yml` keeps `blank_issues_enabled: true` on purpose. The settings window opens
`/issues/new?title=…&body=…&labels=…` with everything typed in; with blank issues off, GitHub
redirects to the chooser and throws all of it away.

## The share forms

`share-spam-list.yml`, `share-profile.yml`, `share-translation.yml` and `share-language.yml` are not
tickets about TwitchSentry. `.github/workflows/community-submissions.yml` turns a spam, translation or
language ticket into a pull request into the `submissions` branch, and commits a profile straight to the
`profiles` branch; the README on each branch says what happens after that. Neither branch shares history
with `main`. They have no *Which part is it about?* dropdown, so `tools/check-compile.ps1` only holds the
forms that ask it (`id: area`) to the window's list.

- **Their labels are what the workflow routes on:** `share: spam list`, `share: profile`,
  `share: translation`, `share: language`. A form applies its own labels for everybody. The `labels=`
  query parameter does not: GitHub ignores it for anyone without permission to label issues, so the area
  labels the ticket window sends only ever arrive on tickets opened by the repository's owner or
  collaborators.
- **The field labels are what the script reads.** Rename one and `.github/scripts/test_submission.py`
  fails until `FIELDS` in `submission.py` says the same.
- **`share-language.yml`'s file field expects a dropped file, not pasted text.** A full language file is
  well past the ~64KB an issue body can hold; `submission.py` reads the attachment link GitHub leaves
  behind instead of the field's text. Pasting the JSON directly still works for a small test file, but
  is not what the form asks for.
