<p align="center">
  <img src="https://github.com/aaskjer/TwitchSentry/blob/main/Utilities/Assets/TwitchSentry-Named-Favicon.png?raw=true" alt="TwitchSentry" width="300" height="300">
</p>


<p align="center"><b>Your smart chat bodyguard. Built for Streamer.bot.</b></p>

<p align="center">
  <img alt="Platform: Twitch" src="https://img.shields.io/badge/platform-Twitch-6441a5">
  <img alt="Tool: Streamer.bot" src="https://img.shields.io/badge/tool-Streamer.bot-0b73ff">
  <a href="https://opensource.org/licenses/MIT"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow"></a>
  <a href="https://creativecommons.org/publicdomain/zero/1.0/"><img alt="Data: CC0 1.0" src="https://img.shields.io/badge/data-CC0_1.0-lightgrey?logo=creativecommons"></a>
  </p><p align="center">
  <img alt="Latest stable release" src="https://img.shields.io/github/v/release/aaskjer/TwitchSentry?label=stable">
  <img alt="Latest pre-release" src="https://img.shields.io/github/v/release/aaskjer/TwitchSentry?include_prereleases&filter=*-beta*&label=pre-release">
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

Spam ruins the vibe. One minute you are reacting to a hilarious donation, the next your chat is full of fake gift links, sketchy URLs and copy-paste scams. TwitchSentry removes them and tells you what went, from whom and why. That is just where it starts.

---

# What it does

| Action | Function |
|---|---|
| **[Link Filter](Manual.md#link-filter)** | Blocks links from viewers you have not trusted, with a whitelist that matches exactly or by wildcard. Always on. |
| **[Spam Scoring](Manual.md#spam-scoring)** | Reads a message as an advert with parts — somewhere to go, something on offer, a way to redeem it, a signature — and acts when enough parts fit together. Always on. |
| **[Message Filter](Manual.md#message-filter)** | Watches *who* is chatting and *how*: account age, ALL CAPS, emote spam, flooding and repeats, and if you want them, repeated words, symbol spam, walls of text, mass mentions, ASCII art and Zalgo text. |
| **[Raid Protection](Manual.md#raid-protection)** | Arms itself after an incoming raid and watches for a swarm of accounts posting the same line. |
| **[Hate Raid Protection](Manual.md#hate-raid-protection)** | Recognises a hate raid by several signals at once, with or without a Twitch raid, locks the chat down and lifts itself again. |
| **[Follow Wave Protection](Manual.md#follow-wave-protection)** | Counts how many different accounts follow inside a short window and judges each one on age, avatar, profile and login. |
| **[LurkBot Filter](Manual.md#lurkbot-filter)** | Watches who sits in chat without writing, and reports or bans accounts from a known bot wave. |
| **[Word Filter](Manual.md#word-filter)** | Your own list of words and phrases, found through their disguises, kept in step with Twitch's Blocked Terms, and `!nuke` for the wave no list knows yet. |
| **[Shared Bot List](Manual.md#shared-bot-list)** | Bans the accounts other TwitchSentry channels identified as bots, from a shared list on GitHub, and reports the bots your channel is sure of. |
| **[Spam Learner](Manual.md#spam-learner)** | Mines what was actually removed for new keywords, phrases and domain endings, and proposes them for review. |
| **[AutoMod](Manual.md#automod)** | Answers the messages Twitch's own AutoMod holds back, so nobody has to sit in the queue. |
| **[Twitch Warn](Manual.md#twitch-warn)** | Twitch's warning screen with escalation on top: warnings, a final warning, then a timeout, a ban or a restriction. Your moderators' own warnings can count too. |
| **[Permit](Manual.md#permit)** | A time-limited link exception for one viewer, granted by you, a moderator, or a Channel Points redeem. |
| **[Check Link](Manual.md#check-link)** | Scans a URL with VirusTotal and IPQualityScore, either automatically or on `!checklink`. |
| **[Voting](Manual.md#voting)** | Lets chat vote someone out. Roles above VIP can never be voted out. |
| **[Notifications](Manual.md#notifications)** | Posts what happened to a Discord, Stoat or GameVox webhook and, if you like, shows it with ntfy on your phone or as a Windows notification too, along with new TwitchSentry releases and what your deck buttons did. |
| **[Offline Protection](Manual.md#offline-protection)** | Puts chat into the modes you pick when the stream ends and lifts them when you go live. |
| **[Deck Buttons](Manual.md#deck-buttons)** | Switches profiles, modules, exemptions, Always Allowed links, AutoMod's answer and test mode, arms Raid Protection or takes the last action back, from a Stream Deck key, a Streamer.bot Deck button or the [OBS dock](Manual.md#the-obs-dock). A key can show what it switched. |

---

## Why not just Twitch's own AutoMod with SmartDetection?

Twitch's AutoMod reads messages for offensive language, and it is good at that. It has nothing to say about:

- typos like `hey.how` or `Super.Bis später`, which it may hold back for nothing more than looking like a link.
- forty accounts arriving on a raid and posting the same line.
- hundreds of throwaway accounts pushing the follow button to corrupt your statistics.
- the "your channel would look great with a logo" chat that only turns into a sales pitch on the fifth message.
- the messages it *does* hold back, which sit in a queue until a moderator answers them one by one.

TwitchSentry covers all of these, and it works through AutoMod's queue for you, so nothing waits there for a moderator.

---

## When something goes wrong

*Ooops, the bot banned my best friend?!?* — `!tsundo` takes back the last action, whichever module took it, and `!tsundo @name` reaches that viewer's most recent one. Every decision is also written down and readable in the window itself. The **Action Log** is what happened and to which message, the **Spam Log** is what the Spam Filter and the Link Filter removed, exactly as it was posted, the **Clean Chat Log** is the ordinary chat that was deliberately left alone, and the **Status Log** is where TwitchSentry reports on itself: errors, a download that failed, an action Twitch refused. [More on the log pages →](Manual.md#results)

Found a bug or have an idea? **Report...** in the ☰ menu opens a pre-filled GitHub issue, your setup included.

## Languages

The settings window ships in English. German, Spanish, French and Brazilian Portuguese are one download away in the ☰ menu, along with languages contributed by the community. What the bot says in chat comes in the same five languages, chosen on its own tab, and every message stays yours to rewrite in whatever language your channel speaks; it can refer to a viewer by the pronouns they set on [pronouns.alejo.io](https://pronouns.alejo.io). The translations are made with AI help and human review. If a text reads badly, **Report...** in the ☰ menu → *A translation* sends in a better wording. Want your own language in there? **Share With Others...** takes a complete translation file, for the window or the chat messages: [Adding a translation](Manual.md#languages).

---

# What you need

- **[Streamer.bot](https://streamer.bot)**, connected to your Twitch account. That is the whole dependency.
- Nothing to pay for and no extra .dll file. Everything runs inside Streamer.bot, plus a few files TwitchSentry creates next to your Streamer.bot install.
- Optional: a free **[VirusTotal](https://www.virustotal.com/gui/join-us)** API key, and an **[IPQualityScore](https://www.ipqualityscore.com/create-account)** key on top if you want a second opinion. Only the optional [Check Link](Manual.md#check-link) module uses them.
- Not sure TwitchSentry is the right tool for you? Here is a fair **[Comparison](Utilities/Comparison.md)** with other moderation tools.

---

# Credits

[Streamer.bot](https://streamer.bot) by [nate1280](https://www.patreon.com/c/nate1280/home) · [enNemMesS](https://extensions.streamer.bot/u/ennemmess/summary) · [Stoshy89 (Tester)](https://www.twitch.tv/stoshy89) · [DutchyRay (Dutch Translation)](https://www.twitch.tv/dutchyray) · YOU ♡

## Data and services

- [stop-words](https://github.com/Alir3z4/stop-words) by Alir3z4 ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)): the Spam Learner downloads these lists to leave ordinary words alone.
- [Unicode confusables](https://www.unicode.org/reports/tr39/) (© Unicode, Inc., [Unicode License V3](https://www.unicode.org/license.txt)) and [YayText](https://yaytext.com): the lookalike-letter table that reads fancy-font spam as plain letters is built from them.
- [IANA](https://www.iana.org/domains/root/db): the list of top-level domains the link checks recognise.
- [Stop The Bots](https://transparent-aluminium.net): the spam domains and keywords TwitchSentry ships with.
- [pronouns.alejo.io](https://pronouns.alejo.io) by Alejo: viewer pronouns, looked up through Streamer.bot.
- [Reward checker](https://ayrtonalexis.com/reward_checker/reward_check.html) by ayrtonalexis: finds a Channel Points reward's ID for Permit.

## Socials
[aaskjer on Twitch](https://twitch.tv/aaskjer) · [TwitchSentry on the Streamer.bot Discord](https://discord.com/channels/834650675224248362/1512133095246270616)
