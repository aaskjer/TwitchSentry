<p align="center">
  <img src="https://github.com/aaskjer/TwitchSentry/blob/main/Utilities/Assets/TwitchSentry-Named-Favicon.png?raw=true" alt="TwitchSentry" width="300" height="300">
</p>


<p align="center"><b>Your smart chat bodyguard. Built for Streamer.bot.</b></p>

<p align="center">
  <img alt="Platform: Twitch" src="https://img.shields.io/badge/platform-Twitch-6441a5">
  <img alt="Tool: Streamer.bot" src="https://img.shields.io/badge/tool-Streamer.bot-0b73ff">
  <img alt="MIT licence" src="https://img.shields.io/github/license/aaskjer/TwitchSentry">
  <img alt="Latest stable release" src="https://img.shields.io/github/v/release/aaskjer/TwitchSentry?label=stable">
  <img alt="Latest pre-release" src="https://img.shields.io/github/v/release/aaskjer/TwitchSentry?include_prereleases&label=pre-release">
  <img alt="Total downloads" src="https://img.shields.io/github/downloads/aaskjer/TwitchSentry/total">
  <img alt="GitHub stars" src="https://img.shields.io/github/stars/aaskjer/TwitchSentry">
</p>

<p align="center">
  <b><a href="https://github.com/aaskjer/TwitchSentry/releases">Download</a></b> ·
  <a href="Manual.md">Manual</a> ·
  <a href="FAQ.md">FAQ</a> ·
  <a href="https://github.com/aaskjer/TwitchSentry/blob/main/Utilities/Import-String.md">Import String</a>
</p>

---

Spam ruins the vibe. One minute you are reacting to a hilarious donation, the next your chat is full of fake gift links, sketchy URLs and copy-paste scams. TwitchSentry removes them, tells you why it was removed and from whom. Any many more!

---

# What it does

| Action | Function |
|---|---|
| **[Link Filter](#general-settings)** | Blocks links from viewers you have not trusted, with a whitelist that matches exactly or by wildcard. Always on. |
| **[Spam Scoring](#spam-scoring)** | Reads a message as an advert with parts — somewhere to go, something on offer, a way to redeem it, a signature — and acts when enough parts fit together. Always on. |
| **[Message Filter](#message-filter)** | Watches *how* someone and *who* chats: account age, ALL CAPS, emote spam, flooding and repeats. |
| **[Raid Protection](#raid-protection)** | Arms itself after an incoming raid and watches for a swarm of accounts posting the same line. |
| **[Follow Protection](#follow-protection)** | Watches follows. It counts how many different accounts arrive inside a short window and judges each on age, avatar, profile and login. |
| **[Spam Learner](#spam-learner)** | Mines what was actually removed for new keywords, phrases and domain endings, and proposes them for review. |
| **[AutoMod](#automod)** | Answers the messages Twitch's own AutoMod holds back, so nobody has to sit in the queue. |
| **[Twitch Warn](#twitch-warn)** | Twitch's warning screen with escalation on top: warnings, a final warning, then a timeout, a ban or a restriction. Your moderators' own warnings can count too. |
| **[Permits](#permits)** | A time-limited link exception for one viewer, granted by you, a moderator, or a Channel Points redeem. |
| **[Check Link](#check-link)** | Scans a URL with VirusTotal and IPQualityScore, either automatically or on `!checklink`. |
| **[Voting](#voting)** | Lets chat vote someone out, with roles above VIP permanently unvotable. |
| **[Discord Alerts](#discord-alerts)** | Posts everything that happened to a webhook to discord. |
| **[Windows Notifications](#windows-notifications)** | A Windows notification for a new TwitchSentry releases and various deck button actions. |
| **[Deck Buttons](#deck-buttons)** | Switches profiles, modules, exemptions and test mode, arms Raid Protection or takes the last action back, from a Stream Deck key or a Streamer.bot Deck button. |

---

## Why not just Twitch's own AutoMod with SmartDetection?

Twitch's AutoMod reads messages for offensive language, and it is good at that. It has nothing to say about:

- typos like `hey.how` or `Super...Bis später`, which it may hold back for nothing more than looking like a link.
- forty accounts arriving on a raid and posting the same line.
- hundreds of throwaway accounts pushing the follow button to corrupt your statistics.
- the "your channel would look great with a logo" chat that only turns into a sales pitch on the fifth message.
- the messages it *does* hold back, which sit in a queue until a moderator answers them one by one.

TwitchSentry covers all of those and more, and answers AutoMod's queue for you so nothing sits in it waiting on a moderator.

---

# What you need

- **[Streamer.bot](https://streamer.bot)**, connected to your Twitch account. That is the whole dependency.
- Nothing to pay for, no extra bot account, no extra .dll file. Everything lives inside streamer.bot and files beside your Streamer.bot install TwitchSentry creates itself.
- (Optional) a free **[VirusTotal](https://www.virustotal.com/gui/join-us)** API key and/or **[IPQualityScore](https://www.ipqualityscore.com/create-account)** one if you want a second opinion. *Only* for the optional [Check Link](Manual.md#check-link) module.

## Decide how strict, in one click

**Profiles**, at the top of the ☰ menu. Five of them — Relaxed, Balanced, Strict, Under Attack, Just Chatting — and picking one sets the message, raid, follow and spam sides together instead of forty settings one at a time. A fresh install already sits at Balanced, so it is the way back rather than a change. Save your own tuning under a name and it joins the list, or share it for others to import. [More →](Manual.md#profiles)

## Block lists that keep up

New viewer-selling sites and bot wording are published once, to the spam feed in this repository, and reach every install within a few hours. An entry you delete stays deleted. Found one yourself? **Share With Others...** in the ☰ menu sends it in for review, and once accepted it reaches everyone else. [More →](Manual.md#known-patterns)

---

## Try it without anyone getting hurt

Switch on **test mode** from the ☰ menu. While it runs nothing is deleted, timed out or banned: every module posts what it *would* have done instead, so you can point a real chat at your settings and nobody gets punished for helping you test them. It ends on its own after five minutes and the notice strip counts it down, so a chat is never left unguarded because somebody forgot to switch it back.

---

## When something goes wrong

*Ooops, the bot banned my best friend?!?* — `!tsundo` takes back the last action, whichever module took it, and `!tsundo @name` reaches that viewer's most recent one. Every decision is also written down and readable in the window itself. The **Action Log** is what happened, the **Violation Log** is the message exactly as it was posted, the **Clean Chat Log** is the ordinary chat that was deliberately left alone, and the **Status Log** is TwitchSentry reporting on itself any errors, a download that failed, an action Twitch refused. [More on the log pages →](Manual.md#results)

Found a bug or have an idea? **Report...** in the ☰ menu opens a pre-filled GitHub issue, your setup included.

## Languages

The settings window ships in English but you can download also: German, Spanish, French and Brazilian Portuguese, plus languages contributed by the community, switchable from the ☰ menu. What the bot says in chat is yours to write, in whatever language your channel speaks, and it can speak of a viewer by the pronouns they set on [pronouns.alejo.io](https://pronouns.alejo.io). The translations are made with AI help and human review. If a text reads badly, **Report...** in the ☰ menu → *A translation* sends in a better wording. Want your own language in there? **Share With Others...** takes a complete translation file: [Adding a translation](Manual.md#languages).

## Updates

The settings window checks for new releases whenever it opens and says so at the top, betas included. Rather wait for stable releases? **Ignore Betas** on the notice.

---

# Credits

[aaskjer on Twitch](https://twitch.tv/aaskjer) · [TwitchSentry on the Streamer.bot Discord](https://discord.com/channels/834650675224248362/1512133095246270616) · [Streamer.bot](https://streamer.bot) by [nate1280](https://www.patreon.com/c/nate1280/home) · [enNemMesS](https://extensions.streamer.bot/u/ennemmess/summary) · YOU ♡
