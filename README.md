# Shared profiles

Settings profiles streamers shared from TwitchSentry, one file per ticket. Every file here passed the check the settings window applies when it imports one: it is a profile export, and it carries no key, webhook, token or list of people. Nobody has reviewed the policy inside it.

**To use one:** open the file, press *Download raw file*, and put it into `Settings/Profiles` in your TwitchSentry folder, or pick it with *Import* in ☰ → *Profiles*. The Profiles dialog lists every setting a profile in that folder would change before you pick it.

The share workflow on `main` writes this branch. It shares no history with `main`, and no install reads it.

| Profile | Shared in | Exported from |
|---|---|---|
| [`Test-Profil`](14.json) | [#14](https://github.com/aaskjer/TwitchSentry/issues/14) | v2.1.0 |
