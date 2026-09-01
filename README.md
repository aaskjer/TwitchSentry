<p align="center">
  <img src="Utilities/Assets/TwitchSentry-full.png" alt="TwitchSentry" width="200" height="200">
</p>


<p align="center"><b>Your smart chat bodyguard. Built for Streamer.bot.</b></p>

<p align="center">
  <img alt="Platform: Twitch" src="https://img.shields.io/badge/platform-Twitch-6441a5">
  <img alt="Tool: Streamer.bot" src="https://img.shields.io/badge/tool-Streamer.bot-0b73ff">
  <img alt="MIT licence" src="https://img.shields.io/github/license/aaskjer/TwitchSentry">
  <img alt="Latest release" src="https://img.shields.io/github/v/release/aaskjer/TwitchSentry">
  <img alt="Total downloads" src="https://img.shields.io/github/downloads/aaskjer/TwitchSentry/total">
</p>

<p align="center">
  <b><a href="#install-in-three-steps">Install</a></b> ·
  <a href="Manual.md">Manual</a> ·
  <a href="FAQ.md">FAQ</a> ·
  <a href="https://github.com/aaskjer/TwitchSentry/releases">Download</a>
</p>

---

Spam ruins the vibe. One minute you are reacting to a hilarious donation, the next your chat is full of fake gift links, sketchy URLs and copy-paste scams. TwitchSentry removes them, tells you what it removed and why, and does all of it from one window.

---

# What it does

| | |
|---|---|
| **[Link Filter](Manual.md#general-settings)** | Blocks links from viewers you have not trusted, with a whitelist that matches exactly or by wildcard. Always on. |
| **[Spam Scoring](Manual.md#spam-scoring)** | Reads a message as an advert with parts (somewhere to go, something on offer, a way to redeem it, a signature) and acts when enough parts fit together. Always on. |
| **[Message Filter](Manual.md#message-filter)** | Watches *how* someone chats: account age, ALL CAPS, emote spam, flooding and repeats. |
| **[Raid Protection](Manual.md#raid-protection)** | Arms itself after an incoming raid and watches for a swarm of accounts posting the same line. |
| **[Spam Learner](Manual.md#spam-learner)** | Mines what was actually removed for new keywords, phrases and domain endings, and proposes them for review. |
| **[AutoMod](Manual.md#automod)** | Answers the messages Twitch's own AutoMod holds back, by level and by category. |
| **[Twitch Warn](Manual.md#twitch-warn)** | Twitch's warning screen, with escalation steps on top of it — a three-strikes rule, if you want one. |
| **[Permits](Manual.md#permits)** | A time-limited link exception for a viewer, granted by you, a moderator, or a Channel Points redeem. |
| **[Check Link](Manual.md#check-link)** | Scans a URL with VirusTotal and IPQualityScore, either automatically or on `!checklink`. |
| **[Voting](Manual.md#voting)** | Lets chat vote someone out, with roles above VIP permanently unvotable. |
| **[Discord Alerts](https://github.com/aaskjer/TwitchSentry/blob/main/Manual.md#discord-alerts)** | Posts what happened to a webhook, one toggle per kind of action. |

---

## Why not just Twitch's own AutoMod with SmartDetection?

Twitch's AutoMod reads messages for offensive language, and it is good at that. It has nothing to say about:

- a link to a fake gift card, dropped by an account that was made five minutes ago
- forty accounts arriving on a raid and posting the same line
- the "your channel would look great with a logo" chat that only turns into a sales pitch on the fifth message
- the messages it *does* hold back, which sit in a queue until a moderator answers them one by one

TwitchSentry covers all four — and answers AutoMod's queue for you, so nobody has to sit in it.

---

# What you need

- **[Streamer.bot](https://streamer.bot)**, connected to your Twitch account. That is the whole dependency.
- Nothing to pay for, no extra bot account, no extra .dll file. Everything lives in files beside your Streamer.bot install.
- A free **[VirusTotal](https://www.virustotal.com/gui/join-us)** API key — and an **[IPQualityScore](https://www.ipqualityscore.com/create-account)** one if you want a second opinion — but *only* for the optional [Check Link](Manual.md#check-link) module. Every other module works without either.

## Try it without anyone getting hurt

Switch on **test mode** from the ☰ menu. While it runs nothing is deleted, timed out or banned: every module posts what it *would* have done instead, so you can point a real chat at your settings and nobody gets punished for helping you test them. It ends on its own after five minutes and the notice strip counts it down, so a chat can never be left unguarded because somebody forgot to switch it back.

---

## When something looks wrong

Every decision is written down and readable in the window itself. The **Action Log** is what happened, the **Violation Log** is the message exactly as it was posted, the **Clean Chat Log** is the ordinary chat that was deliberately left alone, and the **Status Log** is TwitchSentry reporting on itself — an API key still on its placeholder, a download that failed, an action Twitch refused. That last one is the page to open when something quietly did *not* happen. [More on the log pages →](Manual.md#results)

## Languages

The settings window ships in English, German, Spanish, French and Brazilian Portuguese, switchable from the ☰ menu. What the bot says in chat is yours to write, in whatever language your channel speaks. [Adding a translation](Manual.md#languages) is a matter of copying one JSON file and replacing the values.

---

## Documentation

| | |
|---|---|
| **[Manual](Manual.md)** | Every page of the settings window, and what each module decides |
| **[FAQ](FAQ.md)** | The questions that come up most |
| **[Changelog](CHANGELOG.md)** | What changed in each release |
| **[Issues](https://github.com/aaskjer/TwitchSentry/issues)** | Anything that looks wrong, or a feature you are missing |

## Credits

[aaskjer on Twitch](https://twitch.tv/aaskjer) · [TwitchSentry on the Streamer.bot Discord](https://discord.com/channels/834650675224248362/1512133095246270616) · [Streamer.bot](https://streamer.bot) by [nate1280](https://www.patreon.com/c/nate1280/home) · [enNemMesS](https://extensions.streamer.bot/u/ennemmess/summary) · YOU ♡
