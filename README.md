# TwitchSentry Bot List Relay

The Cloudflare Worker behind the public [`botlist`](https://github.com/aaskjer/TwitchSentry/tree/botlist) branch.
TwitchSentry installations report accounts they identified as bots here; every two minutes the Worker checks
new accounts with Twitch and writes the branch as one commit. Nothing in TwitchSentry itself holds a credential:
the GitHub and Twitch keys live only in this Worker's secrets.

## Endpoints

| Route | Who | What |
|---|---|---|
| `POST /v1/report` | installations | `{install, version, reports: [{category, id, login, reason}]}`, up to 50 |
| `POST /v1/retract` | installations | `{install, version, retract: [{id, category?}]}`: an action the streamer undid |
| `POST /v1/remove` | the removal workflow | `{names, issue, by}` with `Authorization: Bearer <REMOVAL_KEY>`; written to the branch before it answers |
| `GET /v1/health` | anyone | version, last commit, counts, which secrets are set |

`category` is `spam`, `lurkbot` or `botwave`; `install` is a random version 4 UUID an installation keeps.

## Rules

- **Independent means another network.** Each installation counts once per account, with the network it first
  reported from (IPv4 /24, IPv6 /48). Addresses and install ids are stored only as salted hashes.
- One report lists an account; installations ban from `banFrom` (2) reports; the `.txt` files hold only those.
- Twitch decides who may be listed at all: partners, affiliates, staff and well-known service bots never are.
  Accounts are checked again weekly, so renames follow and deleted accounts leave.
- **A removal is final for its reporters.** The installations that reported a removed account are never counted
  for it again, and it needs three fresh networks to return.
- Reports expire after a year; `changes.json` keeps a week.
- Limits per hour: 120 requests and 3000 items per network, 2000 items per installation.

## Setup

1. Cloudflare: *Workers & Pages -> Create -> Import a repository*, this repository, branch `relay`, Worker name
   `botlist`. Cloudflare builds and deploys every push to this branch.
2. Secrets under *Settings -> Variables and Secrets*:
   - `GITHUB_TOKEN`: a classic token with `public_repo` from an account with write access but no bypass of
     `main`'s ruleset, so the Worker can write `botlist` and never `main`.
   - `TWITCH_CLIENT_ID`, `TWITCH_CLIENT_SECRET`: a Twitch application (dev.twitch.tv), used for Get Users only.
   - `REMOVAL_KEY`: a long random string; the same value is the removal workflow's Actions secret.
   - `HASH_SALT`: a long random string. **Never change it**: every network and installation would count anew.
3. The D1 database `twitchsentry-botlist` is bound as `DB`; the tables create themselves on first use.

## Tests

`npm test` runs the rules and the real Worker under `wrangler dev` against a fake GitHub and Twitch.
In the TwitchSentry folder, `tools/run-relay-tests.ps1 -NodeDir <folder with node.exe>` does the same.
