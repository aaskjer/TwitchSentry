# ⚖️ TwitchSentry — Comparison

How TwitchSentry stands next to eight moderation tools streamers commonly use: what each one is, what it protects against, and where TwitchSentry is the weaker choice.

**[Overview](https://github.com/aaskjer/TwitchSentry/tree/main)** · **[Manual](Manual.md)** · **[FAQ](FAQ.md)** · **[Report a problem](https://github.com/aaskjer/TwitchSentry/issues)**

> Compiled in October 2026 from each tool's public documentation. A **–** means the feature was not found there, not necessarily that the tool cannot do it, and a **?** means the documentation leaves it open. This page comes from the TwitchSentry project, so its weak spots are listed on purpose. Something wrong or out of date? [Open an issue](https://github.com/aaskjer/TwitchSentry/issues) and it gets corrected.

---

## At a glance

| Tool | What it is | Runs where | Dependencies | Platforms | Cost |
|---|---|---|---|---|---|
| **TwitchSentry** | a moderation suite, nothing else | locally in Streamer.bot (Windows) ² | Streamer.bot only: no extra DLL, no extra bot account (optional: free VirusTotal and IPQualityScore keys for Check Link) | Twitch ¹ | free, MIT licence |
| **tawmae MOD TOOLS** | a moderation toolkit for Streamer.bot | locally in Streamer.bot (Windows) ² | Streamer.bot, plus `TawmaeUI.dll` in the Streamer.bot folder and Streamer.bot's WebSocket server switched on | Twitch | not stated on its page |
| **Moobot** | all-round chat bot | cloud | nothing to install; make its bot account a moderator | Twitch | free version plus a paid tier |
| **Fossabot** | all-round chat bot, common on large channels | cloud | nothing to install; make its bot account a moderator | Twitch, YouTube, Kick | free |
| **Nightbot** | all-round chat bot, the classic | cloud | nothing to install; make its bot account a moderator | Twitch, YouTube, Trovo, SOOP | free |
| **Sery_Bot** | specialist against hate raids and follow bots | cloud | nothing to install; make it a moderator and authorise it on Twitch | Twitch | free |
| **StreamElements** | chat bot inside an overlay platform | cloud | nothing to install; a StreamElements account, and its bot account as moderator | Twitch, YouTube, Kick | free |
| **Mix It Up** | all-round bot as a desktop app | locally (Windows) | the Mix It Up app | Twitch, YouTube, Kick and more | free |
| **PhantomBot** | open-source bot with a web panel | self-hosted | a PC or server that keeps it running; Java comes bundled on most systems, Docker images exist | Twitch | free |

¹ **Twitch only, on purpose.** TwitchSentry's main opponent is link and scam spam, and on YouTube and Kick a viewer cannot natively post a clickable link (on Kick only when the channel's settings allow it, and limited even then). The problem it is built for barely exists there.

² **Windows first, because Streamer.bot is.** Streamer.bot officially runs on Windows; macOS and Linux are only supported unofficially, so TwitchSentry is built and tested for Windows.

### How moderators manage it

Cloud bots give moderators a web dashboard. TwitchSentry has no dashboard, but moderators can change it at any time all the same, once the broadcaster allows it:

- **Chat commands** for the lists and the moment-to-moment work: `!kwadd`, `!wladd`, `!bwadd` and the other list commands, `!permit`, `!nuke`, `!tsundo`.
- **Streamer.bot Deck buttons** (or Stream Deck keys and the OBS dock) to switch profiles, modules, exemptions and test mode, arm Raid Protection or take the last action back.

---

## Protection, feature by feature

Columns: **TS** TwitchSentry · **taw** tawmae MOD TOOLS · **Moo** Moobot · **Fos** Fossabot · **Ngt** Nightbot · **Sery** Sery_Bot · **SE** StreamElements · **MIU** Mix It Up · **Pha** PhantomBot

| | TS | taw | Moo | Fos | Ngt | Sery | SE | MIU | Pha |
|---|---|---|---|---|---|---|---|---|---|
| Blocked words and phrases | ✓ ³ | ✓ | ✓ | ✓ ⁴ | ✓ | – | ✓ ⁴ | ✓ | ✓ ⁴ |
| Link filter with allow list and permits | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓ | ~ | ✓ |
| Caps, emotes, symbols | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓ | ✓ | ✓ |
| Repetition and flooding | ✓ | – | ✓ | ? | ✓ | – | – | – | ✓ |
| Long messages | ✓ | – | ✓ | ? | – | – | ✓ | – | ✓ |
| Fancy fonts, Zalgo, lookalike letters | ✓ | ~ | ✓ | ✓ | – | – | – | – | – |
| Ads and scams recognised by content, learning | ✓ | ~ ⁵ | – | – | – | – | – | – | – |
| Raid and hate-raid protection | ✓ | ✓ | – | ~ ⁶ | – | ✓ | – | ~ | – |
| Follow-bot protection | ✓ | ✓ | – | – | – | ✓ | – | ~ | – |
| Account age | ✓ | ~ | – | – | – | – | – | ✓ | – |
| Nuke (one action on many messages) | ✓ | – | – | ✓ | – | – | – | – | – |
| Links scanned for malware (VirusTotal, IPQS) | ✓ | – | – | – | – | – | – | – | – |
| AutoMod queue and ban evasion handled | ✓ | – | – | – | – | – | – | – | – |
| Warnings and escalation | ✓ | ✓ | ✓ | ? | ✓ | – | ? | ✓ | ✓ |
| Undo (`!tsundo`) | ✓ | – | – | – | – | – | – | – | – |
| Commands, timers, points, song requests | – | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ✓ |

✓ yes · ~ partly · – not found · ? not documented

³ Also catches disguised spellings, and keeps itself in step with Twitch's own Blocked Terms both ways.
⁴ With regular expressions.
⁵ Aimed at "Cheap Viewers" and Discord recruitment bots.
⁶ By hand, through nukes.

---

## The tools one by one

- **tawmae MOD TOOLS** is the closest relative, also built on Streamer.bot. It is stronger when an attack is on: it can pause channel point rewards, action queues and TTS, and it brings a lot of moderator commands (title, game, OBS, polls, predictions, pinning) plus OBS docks for a chat log and suspicious users. Its spam filters are simpler, and it needs an extra DLL.
- **Moobot** has the most polished classic filters: twelve of them, intensity presets from Lenient to Strict, and warnings a viewer has to acknowledge. Nothing documented against follow bots or raids.
- **Fossabot** stays solid even on very large channels. Blocked terms with lookalike handling and regex nukes are its strong points; otherwise a classic filter bot.
- **Nightbot** is simple and dependable, with six basic filters. Enough for a small, calm chat.
- **Sery_Bot** does hate raids and follow bots only, but with a network effect: its list of known bots comes from more than 100,000 channels, which no tool running on one PC can match. No chat filters.
- **StreamElements** has solid basic filters (word groups with regex); moderation is a side feature of the platform.
- **Mix It Up** runs locally like TwitchSentry, but across several platforms, with strikes, a minimum account age and a community word list. Its content filters are fairly basic.
- **PhantomBot** is open source with a web panel and twelve filters, including a spam tracker and fake-purge detection. Its latest GitHub release is v3.22.0.1 from October 2024.

---

## Where TwitchSentry falls short

- **No protection while the PC is off.** Streamer.bot has to be running. Cloud bots protect around the clock, the offline chat included.
- **No all-round features.** No commands, timers, points or song requests, so most channels run a second bot next to it for those.
- **A smaller network.** The community spam feed sees far less than Sery_Bot, Fossabot or Moobot see across thousands of channels.
- **More to set up than a cloud bot.** The depth comes with many settings; the five built-in profiles set them all in one click.

## Where TwitchSentry leads

- **It recognises an advert by how it is built, not just by a word list.** The Spam Learner learns from what was removed, and spam lists arrive through a community feed.
- **Links are checked for malware** with VirusTotal and IPQualityScore.
- **It answers AutoMod's queue and acts on ban evasion.** Unban requests arrive in Discord with the account's history from the logs beside them.
- **Twitch's own warnings are an escalation step**, up to a restriction or a ban.
- **Every timeout, ban and restriction can be taken back** with `!tsundo`, a whole nuke included.
- **Around it:** a test mode, Discord alerts, Windows notifications, deck buttons and an OBS dock. No extra bot account and no DLL.

## Bottom line

No tool leads in everything.

- **For deep spam and scam protection**, TwitchSentry is the strongest here. A cloud bot (Fossabot or Nightbot) complements it for commands and for the hours the PC is off, and Sery_Bot adds its network-wide bot list.
- **For a single bot that does a bit of everything**, Moobot or Fossabot is the most rounded choice.
- **For several platforms at once**, Mix It Up.

---

### Sources

- [tawmae MOD TOOLS](https://tawmae.xyz/mod-tools)
- [Moobot message filters](https://moo.bot/docs/twitch-chat-auto-mod-bot-message-filters)
- [Fossabot docs](https://docs.fossabot.com/), [nukes](https://docs.fossabot.com/nukes/), [lookalikes](https://docs.fossabot.com/lookalikes)
- [Nightbot filters](https://docs.nightbot.tv/commands/filters), [Nightbot setup](https://docs.nightbot.tv/setup)
- [Sery_Bot](https://serycodes.carrd.co/)
- [StreamElements spam filters](https://docs.streamelements.com/chatbot/filters), [on Kick](https://support.streamelements.com/hc/en-us/articles/25794373983122-StreamElements-Chatbot-on-Kick), [on YouTube](https://support.streamelements.com/hc/en-us/articles/18486326016402-StreamElements-Chatbot-on-YouTube)
- [Mix It Up moderation](https://mixitup.bot/docs/moderation)
- [PhantomBot chat moderator](https://github.com/PhantomBot/PhantomBot/blob/master/javascript-source/core/chatModerator.js), [releases](https://github.com/PhantomBot/PhantomBot/releases), [requirements](https://github.com/PhantomBot/PhantomBot#readme)
