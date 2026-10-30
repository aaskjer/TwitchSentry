<p align="center">
  <img src="https://github.com/aaskjer/TwitchSentry/blob/main/Utilities/Assets/TwitchSentry-Favicon.png?raw=true" alt="TwitchSentry" width="180" height="200">
</p>

<h1 align="center">TwitchSentry</h1>

<p align="center">
  <b>Your smart chat bodyguard. Built for Streamer.bot.</b><br>
  Removes scams, spam and bot waves from your Twitch chat and tells you what each message said, who sent it and why it was removed.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-Twitch-6441a5" alt="Platform: Twitch">
  <img src="https://img.shields.io/badge/tool-streamer.bot-0b73ff" alt="Streamer.bot">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow" alt="License: MIT"></a>
  <a href="https://creativecommons.org/publicdomain/zero/1.0/"><img src="https://img.shields.io/badge/data-CC0_1.0-lightgrey?logo=creativecommons" alt="Data: CC0 1.0"></a>
  <img src="https://img.shields.io/github/v/release/aaskjer/TwitchSentry?label=stable" alt="Latest stable release">
  <img src="https://img.shields.io/github/v/release/aaskjer/TwitchSentry?include_prereleases&filter=*-beta*&label=pre-release" alt="Latest pre-release">
  <img src="https://img.shields.io/github/downloads/aaskjer/TwitchSentry/total" alt="Downloads">
  <img src="https://img.shields.io/github/stars/aaskjer/TwitchSentry" alt="Stars">
</p>

<p align="center">
  <a href="https://github.com/aaskjer/TwitchSentry/releases"><b>Download</b></a> &nbsp;·&nbsp;
  <a href="Manual.md"><b>Manual</b></a> &nbsp;·&nbsp;
  <a href="FAQ.md"><b>FAQ</b></a> &nbsp;·&nbsp;
  <a href="Utilities/Comparison.md"><b>Comparison</b></a> &nbsp;·&nbsp;
  <a href="https://github.com/aaskjer/TwitchSentry/blob/main/Utilities/Import-String.md"><b>Import String</b></a>
</p>

---

## 📖 Overview

Fake gift links, sketchy URLs, copy-paste scams: TwitchSentry removes them from your Twitch chat and logs
every decision. It runs entirely inside Streamer.bot, with nothing to pay for and no extra .dll file. The
[Manual](Manual.md) covers every module.

## ✨ Highlights

- 🕵️ **Spam that reads like an advert.** [Spam Scoring](Manual.md#spam-scoring) looks for the parts of an
  advert — somewhere to go, something on offer, a way to redeem it, a signature — and acts when enough of
  them fit together. The [Link Filter](Manual.md#link-filter) blocks links from viewers you have not trusted.
  Both are always on.
- 💬 **How people chat, not just what.** The [Message Filter](Manual.md#message-filter) watches account age,
  ALL CAPS, emote spam, flooding and repeats, and optionally walls of text, ASCII art and Zalgo text. The
  [Word Filter](Manual.md#word-filter) finds your terms through their disguises and stays in
  step with Twitch's Blocked Terms.
- 🌊 **Protection against waves.** [Raid Protection](Manual.md#raid-protection) arms itself after an incoming
  raid and watches for accounts posting the same line. [Hate Raid Protection](Manual.md#hate-raid-protection)
  locks chat down and lifts the lock again. [Follow Wave Protection](Manual.md#follow-wave-protection) judges
  every account in a burst of follows, and the [LurkBot Filter](Manual.md#lurkbot-filter) catches silent
  accounts from known bot waves.
- 🧠 **Learns from your channel and others.** The [Shared Bot List](Manual.md#shared-bot-list) bans accounts
  other TwitchSentry channels identified as bots. The [Spam Learner](Manual.md#spam-learner) mines removed
  messages for new keywords, phrases and domain endings and proposes them for review.
- 🤖 **Clears the AutoMod queue.** TwitchSentry answers the messages Twitch's [AutoMod](Manual.md#automod)
  holds back, so nobody waits there for a moderator. It also catches what AutoMod has nothing to say about:
  raid swarms, follow-bot waves and sales pitches that only show up in the fifth message.
- ⚠️ **Escalation and exceptions.** [Twitch Warn](Manual.md#twitch-warn) escalates from warnings to a timeout,
  ban or restriction. [Permit](Manual.md#permit) grants a time-limited link exception, and
  [Check Link](Manual.md#check-link) scans URLs with VirusTotal and IPQualityScore.
  [Voting](Manual.md#voting) lets chat vote someone out, never anyone above VIP.
- ↩️ **Undo for every module.** `!tsundo` takes back the last action, whichever module took it. Action, spam,
  clean-chat and status logs show what happened and why.
- 🎛️ **Control from anywhere.** [Deck Buttons](Manual.md#deck-buttons) on a Stream Deck, a Streamer.bot Deck or
  the OBS dock switch profiles and modules. [Notifications](Manual.md#notifications) go to Discord, Stoat or
  GameVox webhooks, ntfy or Windows. [Offline Protection](Manual.md#offline-protection) sets chat modes when
  the stream ends. *Work in Progress*
- 🌍 **Five languages.** The window and the chat messages come in English, German, Spanish, French and
  Brazilian Portuguese, with community translations on top. Messages can use the pronouns viewers set on
  pronouns.alejo.io.

---

## Credits

- **Author:** [aaskjer on Twitch](https://twitch.tv/aaskjer) · [aaskjer.github.io](https://aaskjer.github.io/)
- **Built for:** [Streamer.bot](https://streamer.bot) by [nate1280](https://www.patreon.com/c/nate1280/home)
- **Data & services:**
  - [stop-words](https://github.com/Alir3z4/stop-words) by Alir3z4 ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)): ordinary words the Spam Learner leaves alone
  - [Unicode confusables](https://www.unicode.org/reports/tr39/) (© Unicode, Inc., [Unicode License V3](https://www.unicode.org/license.txt)) and [YayText](https://yaytext.com): the lookalike-letter table that reads fancy-font spam as plain letters
  - [IANA](https://www.iana.org/domains/root/db): the top-level domains the link checks recognise
  - [Stop The Bots](https://transparent-aluminium.net): the spam domains and keywords TwitchSentry ships with
  - [pronouns.alejo.io](https://pronouns.alejo.io) by Alejo: viewer pronouns, looked up through Streamer.bot
  - [Reward checker](https://ayrtonalexis.com/reward_checker/reward_check.html) by ayrtonalexis: finds a Channel Points reward's ID for Permit
- **Community:** [TwitchSentry on the Streamer.bot Discord](https://discord.com/channels/834650675224248362/1512133095246270616)
- **Thanks:** [enNemMesS](https://extensions.streamer.bot/u/ennemmess/summary) · [Stoshy89](https://www.twitch.tv/stoshy89) (Tester) · [DutchyRay](https://www.twitch.tv/dutchyray) (Dutch Translation) · YOU ♡
