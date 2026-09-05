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
  <b><a href="https://github.com/aaskjer/TwitchSentry/releases">Download</a></b> ·
  <a href="Manual.md">Manual</a> ·
  <a href="FAQ.md">FAQ</a> ·
  <a href="https://github.com/aaskjer/TwitchSentry/blob/main/Utilities/Import-String.md">Import String</a>
</p>

---

Spam ruins the vibe. One minute you are reacting to a hilarious donation, the next your chat is full of fake gift links, sketchy URLs and copy-paste scams. TwitchSentry removes them, tells you what it removed and why, and does all of it from one window.

---

# What it does

| Action | Function |
|---|---|
| **[Link Filter](https://github.com/aaskjer/TwitchSentry/blob/main/Manual.md#general-settings)** | Blocks links from viewers you have not trusted, with a whitelist that matches exactly or by wildcard. Always on. |
| **[Spam Scoring](https://github.com/aaskjer/TwitchSentry/blob/main/Manual.md#spam-scoring)** | Reads a message as an advert with parts (somewhere to go, something on offer, a way to redeem it, a signature) and acts when enough parts fit together. Always on. |
| **[Message Filter](https://github.com/aaskjer/TwitchSentry/blob/main/Manual.md#message-filter)** | Watches *how* someone chats: account age, ALL CAPS, emote spam, flooding and repeats. |
| **[Raid Protection](https://github.com/aaskjer/TwitchSentry/blob/main/Manual.md#raid-protection)** | Arms itself after an incoming raid and watches for a swarm of accounts posting the same line. |
| **[Follow Protection](https://github.com/aaskjer/TwitchSentry/blob/main/Manual.md#follow-guard)** | Watches follows. It counts how many different accounts arrive inside a short window and judges each on age, avatar, profile and login. |
| **[Spam Learner](https://github.com/aaskjer/TwitchSentry/blob/main/Manual.md#spam-learner)** | Mines what was actually removed for new keywords, phrases and domain endings, and proposes them for review. |
| **[AutoMod](https://github.com/aaskjer/TwitchSentry/blob/main/Manual.md#automod)** | Answers the messages Twitch's own AutoMod holds back, by level and by category. |
| **[Twitch Warn](https://github.com/aaskjer/TwitchSentry/blob/main/Manual.md#twitch-warn)** | Twitch's warning screen, with escalation steps on top of it — a three-strikes rule, if you want one. |
| **[Permits](https://github.com/aaskjer/TwitchSentry/blob/main/Manual.md#permits)** | A time-limited link exception for a viewer, granted by you, a moderator, or a Channel Points redeem. |
| **[Check Link](https://github.com/aaskjer/TwitchSentry/blob/main/Manual.md#check-link)** | Scans a URL with VirusTotal and IPQualityScore, either automatically or on `!checklink`. |
| **[Voting](https://github.com/aaskjer/TwitchSentry/blob/main/Manual.md#voting)** | Lets chat vote someone out, with roles above VIP permanently unvotable. |
| **[Discord Alerts](https://github.com/aaskjer/TwitchSentry/blob/main/Manual.md#discord-alerts)** | Posts what happened to a webhook, one toggle per kind of action. |

---

## Why not just Twitch's own AutoMod with SmartDetection?

Twitch's AutoMod reads messages for offensive language, and it is good at that. It has nothing to say about:

- typos like `hey.how` or `Super...Bis später`, might holds them back for just being links.
- forty accounts arriving on a raid and posting the same line.
- hundreds of throwaway accounts pushing the follow button to corrupt your statistics.
- the "your channel would look great with a logo" chat that only turns into a sales pitch on the fifth message.
- the messages it *does* hold back, which sit in a queue until a moderator answers them one by one.

TwitchSentry covers all and many more and even answers AutoMod's queue for you, so nobody has to sit in it.

---

# What you need

- **[Streamer.bot](https://streamer.bot)**, connected to your Twitch account. That is the whole dependency.
- Nothing to pay for, no extra bot account, no extra .dll file. Everything lives in files beside your Streamer.bot install.
- (Optional) a free **[VirusTotal](https://www.virustotal.com/gui/join-us)** API key and/or **[IPQualityScore](https://www.ipqualityscore.com/create-account)** one if you want a second opinion. *Only* for the optional [Check Link](Manual.md#check-link) module.

## Try it without anyone getting hurt

Switch on **test mode** from the ☰ menu. While it runs nothing is deleted, timed out or banned: every module posts what it *would* have done instead, so you can point a real chat at your settings and nobody gets punished for helping you test them. It ends on its own after the default 5 minutes and the notice strip counts it down, so your chat is never be left unguarded.

---

## When something goes wrong

*Ooops, the bot banned my best friend?!?* type `!tsundo <@userName>` to revert any last action in general or a specific user! Also every decision is written down and readable in the GUI window itself. The **Action Log** is what happened, the **Violation Log** is the message exactly as it was posted, the **Clean Chat Log** is the ordinary chat that was deliberately left alone, and the **Status Log** is TwitchSentry reporting on itself any errors, a download that failed, an action Twitch refused. [More on the log pages →](Manual.md#results)

## Languages

The settings window ships in English but you can download also: German, Spanish, French and Brazilian Portuguese, switchable from the ☰ menu. What the bot says in chat is yours to write, in whatever language your channel speaks. The translations are made with the help of ai and translators. You think they are bogus and you want to contribute? Feel free to open up a [discussion](https://github.com/aaskjer/TwitchSentry/discussions)! Might want to do your own language? [Adding a translation](Manual.md#languages).

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
