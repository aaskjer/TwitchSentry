# Submissions

Spam wording, translation fixes and complete language files streamers shared from TwitchSentry, waiting to be taken up. Accepted here is not shipped: nothing in this branch reaches an installation.

| Folder | Shared through | Where it goes from here |
|---|---|---|
| `spam/` | ☰ → *Share With Others...*, spam wording from your lists | Weighed against what other streamers sent. What holds up is published in the [spam feed](https://github.com/aaskjer/TwitchSentry/blob/main/Feed/README.md), which every installation receives within hours. |
| `translations/<code>/` | ☰ → *Report...*, *A translation* | One file per ticket, a folder per language. Published into `Language/` on `main` together with the other fixes for that language. |
| `languages/<code>.json`, `languages/chat/<code>.json` | ☰ → *Share With Others...*, a complete translation file | One file per language, the newest accepted one. Published into `Language/` on `main`. |

**Published** means a pull request into `main` that brings the accepted text into the language files every installation downloads. It mentions the tickets it carries, and merging it is what makes them available.

**How a file gets here:** the share form fills a ticket in, the ticket becomes a pull request into this branch, and merging it takes the submission up and closes the ticket. Editing the ticket updates its pull request; a ticket with a mistake in it is answered with what to correct instead.

**Examples:** a file that opens with an `__example` field is test data from trying the share forms out, kept as an example. It is not a submission, and nothing takes it up.

**What was checked:** for spam wording, that every entry is one an installation would accept, and that TwitchSentry does not already carry it. For a translation, that the language exists, and whether the English text is one the settings window really shows. For a complete language file, that it parses and carries enough text to be one - not whether the wording is any good. Whether wording deserves to reach every channel is the judgement the merge stands for - that is the whole point of the wait.

**Profiles are not collected here.** A profile changes nothing about TwitchSentry, so nobody has to take it up: it goes straight to the [`profiles` branch](https://github.com/aaskjer/TwitchSentry/tree/profiles).

This branch has no history in common with `main`, and this page is written by the share workflow.
