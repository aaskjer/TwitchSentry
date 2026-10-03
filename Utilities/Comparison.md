# ⚖️ TwitchSentry — Comparison

Not sure if TwitchSentry is the right tool for you? Might want to compare it to other common bots?
This is how TwitchSentry stands next to eight other moderation tools streamers commonly use.

**[Overview](https://github.com/aaskjer/TwitchSentry/tree/main)** · **[Manual](Manual.md)** · **[FAQ](FAQ.md)** · **[Report a problem](https://github.com/aaskjer/TwitchSentry/issues)**

> Compiled in October 2026 from each tool's public documentation. This page comes from the TwitchSentry project, so its weak spots are listed on purpose. Something wrong or out of date? [Open an issue](https://github.com/aaskjer/TwitchSentry/issues) and it gets corrected.

---

## At a glance

| Tool | What it is | Runs where | Dependencies | Platforms | Cost |
|---|---|---|---|---|---|
| **TwitchSentry** | a moderation suite, nothing else | locally in Streamer.bot (Windows) ¹ | Streamer.bot only: no extra DLL, no extra bot account (optional: free VirusTotal and IPQualityScore keys for Check Link) | Twitch | free, MIT licence |
| **tawmae MOD TOOLS** | a moderation toolkit for Streamer.bot | locally in Streamer.bot (Windows) ¹ | Streamer.bot, plus `TawmaeUI.dll` in the Streamer.bot folder and Streamer.bot's WebSocket server switched on | Twitch | free |
| **Moobot** | all-round chat bot | cloud | nothing to install; make its bot account a moderator | Twitch | free version plus a paid tier |
| **Fossabot** | all-round chat bot, common on large channels | cloud | nothing to install; make its bot account a moderator | Twitch, YouTube, Kick, X | free |
| **Nightbot** | all-round chat bot, the classic | cloud | nothing to install; make its bot account a moderator | Twitch, YouTube, Trovo, SOOP | free |
| **Sery_Bot** | protection bot against spam bots, hate raids and follow bots, with community extras | cloud | nothing to install; make it a moderator and authorise it on Twitch | Twitch | free |
| **StreamElements** | chat bot inside an overlay platform | cloud | nothing to install; a StreamElements account, and its bot account as moderator | Twitch, YouTube, Kick | free |
| **Mix It Up** | all-round bot as a desktop app | locally (Windows) | the Mix It Up app | Twitch, YouTube, Kick and more | free |
| **PhantomBot** | open-source bot with a web panel | self-hosted | a PC or server that keeps it running; Java comes bundled on most systems, Docker images exist | Twitch | free |

> ¹ **Streamer.bot is built for Windows.** The Project may run alike with Linux or Mac but they aren't officially supported.

---

## Overview, feature by feature

Columns: **TS** TwitchSentry · **taw** tawmae MOD TOOLS · **Moo** Moobot · **Fos** Fossabot · **Ngt** Nightbot · **Sery** Sery_Bot · **SE** StreamElements · **MIU** Mix It Up · **Pha** PhantomBot

| | TS | taw | Moo | Fos | Ngt | Sery | SE | MIU | Pha |
|---|---|---|---|---|---|---|---|---|---|
| Blocked words and phrases | ✓ ² | ✓ | ✓ | ✓ ³ | ✓ | – | ✓ ³ | ✓ | ✓ ³ |
| Link filter with allow list and permits | ✓ | ✓ | ✓ | ✓ | ✓ | ~ ⁶ | ✓ | ~ | ✓ |
| Caps, emotes, symbols | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓ | ✓ | ✓ |
| Repetition and flooding | ✓ | – | ✓ | ✓ | ✓ | – | ✓ | – | ✓ |
| Long messages | ✓ | – | ✓ | ✓ | – | – | ✓ | – | ✓ |
| Fancy fonts, Zalgo, lookalike letters | ✓ | – | ✓ | ✓ | – | – | ~ ⁸ | – | – |
| ASCII art | ✓ | ✓ | ~ ⁹ | – | – | ✓ | – | – | – |
| Ads and scams recognised by content, learning | ✓ | ~ ⁴ | – | – | – | ✓ ⁷ | – | – | – |
| Raid and hate-raid protection | ✓ | ✓ | – | ~ ⁵ | – | ✓ | – | ~ | – |
| Follow-bot protection | ✓ | ✓ | – | – | – | ✓ | – | ~ | – |
| Shield Mode switched for you | ✓ | – | – | – | – | ✓ | – | – | – |
| Account age | ✓ | ~ | – | – | – | – | – | ✓ | – |
| Nuke (one action on many messages) | ✓ | – | – | ✓ | – | – | – | – | – |
| Links scanned for malware (VirusTotal, IPQS) | ✓ | – | – | – | – | – | – | – | – |
| AutoMod queue and ban evasion handled | ✓ | – | – | – | – | – | – | – | – |
| Warnings and escalation | ✓ | ✓ | ✓ | ? | ✓ | – | ✓ | ✓ | ✓ |
| Undo (`!tsundo`) | ✓ | – | – | – | – | – | – | – | – |
| Vote for action | ✓ | – | – | – | – | – | – | – | – |
| Fun Commands, timers, points, song requests | – | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

 **✓** yes · **~** partly · **–** not found · **?** not documented.

> **²** Also catches disguised spellings, and keeps itself in step with Twitch's own Blocked Terms both ways.   
> **³** With regular expressions.   
> **⁴** Aimed at "Cheap Viewers" and Discord recruitment bots.   
> **⁵** By hand, through nukes.   
> **⁶** Removes scam and malicious links; no allow list or permits of your own.   
> **⁷** On from the start: common spam and scam messages, through a known-bot list and pattern detection across its whole network.   
> **⁸** Zalgo only.   
> **⁹** Block characters, through its symbols filter.   

---

## The compared tools one by one

- **tawmae MOD TOOLS** is the closest relative, also built on Streamer.bot. It is stronger when an attack is on: it can pause channel point rewards, action queues and TTS, and it brings a lot of moderator commands (title, game, OBS, polls, predictions, pinning) plus OBS docks for a chat log and suspicious users. Its spam filters are simpler, and it needs an extra DLL.
- **Moobot** has the most polished classic filters: twelve of them, intensity presets from Lenient to Strict, and warnings a viewer has to acknowledge. Nothing documented against follow bots or raids.
- **Fossabot** stays solid even on very large channels. Blocked terms with lookalike handling and regex nukes are its strong points, beside filters for links, caps, symbols, emotes, repeated messages and message height. Audit logs show what each moderator did, and custom roles decide who may do what. Nothing documented against follow bots or raids.
- **Nightbot** is simple and dependable, with six basic filters. Enough for a small, calm chat.
- **Sery_Bot** is protection first, used by more than 250,000 streamers since 2018, and its protection is on from the moment it joins: it removes spam bots, scam and malicious links and suspect ASCII art, stops hate raids, and silently blocks follow bots and removes their follows. Behind it sit a known-bot list and pattern detection across its whole network, which no tool running on one PC can match.
- **StreamElements** has ten filters: banned words (groups, regex), caps, emotes, links (allow and block lists, `!permit`), one-man spam, paragraph length, repetition, symbols, Zalgo and even a language filter, with warnings and longer timeouts for repeat offenders. Nothing documented against follow bots or raids; moderation is one part of a bigger platform.
- **Mix It Up** runs locally like TwitchSentry, but across several platforms, with strikes, a minimum account age and a community word list. Its content filters are fairly basic.
- **PhantomBot** is open source with a web panel and twelve filters, including a spam tracker and fake-purge detection. Its latest GitHub release is v3.22.0.1 from October 2024.

---

## Where TwitchSentry falls short

- **No protection as long as the PC is turned off.** If TwitchSentry is not running specifically on a server, there is no way to automatically protect yourself from attacks offline. Cloud bots provide round-the-clock protection, including offline chat.
- **No all-round features.** No timers, points, song requests or other fun features, so most channels likely run a second bot next to it for those.
- **A smaller network.** TwitchSentry needs active contribution by the community, so spam feed sees far less than Sery_Bot, Fossabot or Moobot which see across thousands of channels.
- **One-man project with strong AI support.** AI tends to cause errors, and despite extensive testing, there is always room for error.

## Where TwitchSentry leads

- **It recognises spam by how it is built, not just by a word list.** The Spam Learner learns from what was removed, and spam lists arrive through a community feed.
- **Links are checked for malware** as optional feature with VirusTotal and IPQualityScore.
- **It answers AutoMod's queue and acts on ban evasion.** Unban requests arrive in Discord with the account's history from the logs beside them.
- **Utilizes Twitch's own warning system** features escalation steps, like a 3-strikes rule up to a restriction or timeout/ban.
- **Every timeout, ban and restriction can be taken back** with `!tsundo`, whole nukes included.
- **Around it:** a handy test mode, Discord alerts, Windows notifications, shareable profiles, backup&import features, no extra bot account and no external .DLL needed.
- **Streamer.bot Deck, Elgato StreamDeck and OBS Dock support** to switch profiles, modules, exemptions and test mode, arm Raid Protection or take the last action back.
- **Users vote actions** and makes them able to punish other users by working together with unique votes


## Bottom line

- **For deep spam and scam protection**, *TwitchSentry is the tool to go*. A cloud bot (Fossabot or Nightbot) complements it with their features.
- **For a single bot that does a bit of everything**, Moobot or Fossabot is the most rounded choice.
- **For several platforms at once**, Mix It Up.

---

### Sources

- [tawmae MOD TOOLS](https://tawmae.xyz/mod-tools)
- [Moobot message filters](https://moo.bot/docs/twitch-chat-auto-mod-bot-message-filters)
- [Fossabot](https://fossabot.com/), [docs](https://docs.fossabot.com/), [nukes](https://docs.fossabot.com/nukes/), [lookalikes](https://docs.fossabot.com/lookalikes), [filter list in Bloopbot's migration guide](https://bloopbot.com/docs/coming-from-fossabot)
- [Nightbot filters](https://docs.nightbot.tv/commands/filters), [Nightbot setup](https://docs.nightbot.tv/setup)
- [Sery_Bot docs](https://docs.sery.bot/), [understanding protection](https://docs.sery.bot/understanding-protection/), [spam protection](https://docs.sery.bot/commands/spam/), [all commands](https://docs.sery.bot/commands/all-commands-az/), [FAQ](https://docs.sery.bot/faq/)
- [StreamElements spam filters](https://docs.streamelements.com/chatbot/filters), [on Kick](https://support.streamelements.com/hc/en-us/articles/25794373983122-StreamElements-Chatbot-on-Kick), [on YouTube](https://support.streamelements.com/hc/en-us/articles/18486326016402-StreamElements-Chatbot-on-YouTube)
- [Mix It Up moderation](https://mixitup.bot/docs/moderation)
- [PhantomBot chat moderator](https://github.com/PhantomBot/PhantomBot/blob/master/javascript-source/core/chatModerator.js), [releases](https://github.com/PhantomBot/PhantomBot/releases), [requirements](https://github.com/PhantomBot/PhantomBot#readme)
