# TwitchSentry live data

What every [TwitchSentry](https://github.com/aaskjer/TwitchSentry) install downloads by itself, every ten minutes:
the spam feed and the language files. Nothing here needs to be imported or copied by hand.

| File | What it is |
|---|---|
| `manifest.json` | Every file below with its `version`, `sha256`, `size` and, for language files, `minClient`: the oldest release that can read it. `commit` names the commit that holds those very files. |
| `spam.json` | The spam feed: new spam wording and detection patterns. Its format is described in [Feed/README.md](https://github.com/aaskjer/TwitchSentry/blob/main/Feed/README.md). |
| `Language/<code>.json` | The settings window's texts, one file per language, made for the newest release. |
| `Language/Chat/<code>.json` | The chat messages TwitchSentry sends, one file per language. |
| `Language/<release>/...` | The same files as they were for an earlier release, kept for the installs still on it. |
| `Language/index.json`, `Language/Chat/index.json` | The published languages with their names and translators, for the settings window's language list. |

## How an install uses it

- **The manifest comes first.** An install downloads a file only from the commit the manifest names, and only uses
  it when its size and SHA256 match the manifest. Anything else is left alone and tried again a few minutes later.
- **Each language file is made for one release.** Its texts are keyed by the settings window's English texts, so a
  file made for a later release would lose translations in an earlier one. An install takes, per language, the file
  whose `minClient` is the newest one it has reached. When the texts change, the files made for the release before
  move into `Language/<release>/`. Files older than what the last stable release reads are removed.
- **A version never goes back.** An install keeps a file that is newer than the published one.

## How it gets here

Translations reach this branch after they are accepted on `main`. To share one, use ☰ → *Share With Others...* in
the settings window.
