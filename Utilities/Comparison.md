# ⚖️ TwitchSentry — Comparison

Not sure TwitchSentry is the right tool for you, or want to see how it compares with the bots you already know?
Here it stands next to eleven other moderation tools that streamers commonly use.

**[Overview](https://github.com/aaskjer/TwitchSentry/tree/main)** · **[Manual](../Manual.md)** · **[FAQ](../FAQ.md)** · **[Report a problem](https://github.com/aaskjer/TwitchSentry/issues)**

> Compiled in October 2026 from each tool's public documentation, last checked on 17 October 2026. This page comes from the TwitchSentry project, so its weak spots are listed on purpose. Something wrong or out of date? [Open an issue](https://github.com/aaskjer/TwitchSentry/issues) and it gets corrected.

---

## At a glance

| Tool | What it is | Runs where | Dependencies | Platforms | Cost |
|---|---|---|---|---|---|
| **TwitchSentry** | a moderation suite for Streamer.bot | locally in Streamer.bot (Windows) ¹ | Streamer.bot, SB's WebSocket server (optional: a VirusTotal API key, plus an IPQualityScore key) | Twitch | free |
| **tawmae MODERATION TOOLS** | a toolkit for Streamer.bot, successor of MOD TOOLS | locally in Streamer.bot (Windows) ¹ | Streamer.bot, `TawmaeUI.dll`, SB's WebSocket server | Twitch | free |
| **Moobot** | all-round chat bot | cloud | nothing; make its bot account a moderator | Twitch | free, paid tier |
| **Fossabot** | all-round chat bot, common on large channels | cloud | nothing; make its bot account a moderator | Twitch, YouTube, Kick, X | free |
| **Nightbot** | all-round chat bot, the classic | cloud | nothing; make its bot account a moderator | Twitch, YouTube, Trovo, SOOP | free |
| **Sery_Bot** | protection bot against spam bots, hate raids and follow bots, with community extras | cloud | nothing; make its bot account a moderator | Twitch | free |
| **StreamElements** | chat bot inside an overlay platform | cloud | an account on their site; make its bot account a moderator | Twitch, YouTube, Kick | free |
| **Streamlabs Cloudbot** | chat bot inside the Streamlabs platform | cloud | a Streamlabs account; make its bot account a moderator | Twitch, YouTube, Kick, X | free |
| **WizeBot** | all-round chat bot with protection tools | cloud | nothing; make its bot account a moderator | Twitch | free |
| **Bloopbot** | newer chat bot, commands built as visual flows | cloud | nothing; make its bot account a moderator | Twitch, Kick | free, paid tiers |
| **Mix It Up** | all-round bot as a desktop app | locally (Windows) | the Mix It Up app | Twitch, YouTube, Kick and more | free |
| **PhantomBot** | open-source bot with a web panel | self-hosted | a PC or server that keeps it running; Java comes bundled on most systems, Docker images exist | Twitch | free |

> ¹ **Streamer.bot is built for Windows.** It may also run with Linux or Mac, but neither are officially supported.

---

## Overview, feature by feature

Columns: **TS** TwitchSentry · **taw** tawmae MODERATION TOOLS · **Moo** Moobot · **Fos** Fossabot · **Ngt** Nightbot · **Sery** Sery_Bot · **SE** StreamElements · **SL** Streamlabs Cloudbot · **Wize** WizeBot · **Bloop** Bloopbot · **MIU** Mix It Up · **Pha** PhantomBot

| | TS | taw | Moo | Fos | Ngt | Sery | SE | SL | Wize | Bloop | MIU | Pha |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Blocked words and phrases | ✓ ² | ✓ | ✓ | ✓ ³ | ✓ | – | ✓ ³ | ✓ ³ | ✓ | ✓ ³ | ✓ | ✓ ³ |
| Link filter with allow list and permits | ✓ | ✓ | ✓ | ✓ | ✓ | ~ ⁶ | ✓ | ✓ | ✓ | ✓ | ~ | ✓ |
| Caps, emotes, symbols | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓ | ✓ | ? | ✓ | ✓ | ✓ |
| Repetition and flooding | ✓ | – | ✓ | ✓ | ✓ | – | ✓ | – | ? | ✓ | – | ✓ |
| Long messages | ✓ | – | ✓ | ✓ | – | – | ✓ | ✓ | ? | – | – | ✓ |
| Fancy fonts, Zalgo, lookalike letters | ✓ | ~ ¹⁰ | ✓ | ✓ | – | – | ~ ⁸ | ~ ⁸ | ? | ✓ | – | – |
| ASCII art | ✓ | ✓ | ~ ⁹ | – | – | ✓ | – | – | ? | – | – | – |
| Ads and scams recognised by content, learning | ✓ | ~ ⁴ | – | – | – | ✓ ⁷ | – | – | – | ~ ¹¹ | – | – |
| Raid and hate-raid protection | ✓ | ~ ⁵ | – | ~ ⁵ | – | ✓ | – | ~ ⁵ | ~ ⁵ | – | ~ | – |
| Follow-bot protection | ✓ | ✓ | – | – | – | ✓ | – | – | ~ ¹² | ✓ | ~ | – |
| Lurking bots in the viewer list | ✓ | – | – | – | – | – | – | – | – | – | – | – |
| Bot list shared across channels | ✓ | – | ~ ¹³ | – | – | ✓ ⁷ | – | – | ✓ | – | – | – |
| Shield Mode switched for you | ✓ | ~ ⁵ | – | – | – | ✓ | – | – | – | ✓ | – | – |
| Chat modes while offline | ✓ | ✓ | – | – | – | ✓ | – | – | – | – | – | – |
| Account age | ✓ | ~ | – | – | – | – | – | – | – | ✓ | ✓ | – |
| Nuke (one action on many messages) | ✓ | – | ~ ¹⁴ | ✓ | – | – | – | – | – | ✓ | – | – |
| Links scanned for malware (VirusTotal, IPQS) | ✓ | – | – | – | – | – | – | – | – | – | – | – |
| AutoMod queue and ban evasion handled | ✓ | – | – | – | – | – | – | – | – | – | – | – |
| Warnings and escalation | ✓ | ✓ | ✓ | ? | ✓ | – | ✓ | – | ✓ | ✓ | ✓ | ✓ |
| Undo (`!tsundo`) | ✓ | – | – | ~ ¹⁵ | – | – | – | – | – | ~ ¹⁵ | – | – |
| Vote for action | ✓ | – | – | ✓ | – | – | – | – | – | – | – | – |
| Fun Commands, timers, points, song requests | – | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

 **✓** yes · **~** partly · **–** not found · **?** not documented.

> **²** Also catches disguised spellings, and keeps itself in step with Twitch's own Blocked Terms both ways.   
> **³** With regular expressions.   
> **⁴** Sale and scam bots on their first message, through built-in rules.   
> **⁵** Switched on by hand: tawmae from its dock, Fossabot through nukes, Streamlabs as Safe Mode, WizeBot as its emergency mode.   
> **⁶** Removes scam and malicious links; no allow list or permits of your own.   
> **⁷** On from the start: common spam and scam messages, through a known-bot list and pattern detection across its whole network.   
> **⁸** Zalgo only.   
> **⁹** Block characters, through its symbols filter.   
> **¹⁰** Disguised spellings and stretched letters in blocked words and links.   
> **¹¹** An AI moderation step on the Pro plan reads what a message means.   
> **¹²** Finds and removes bot follows afterwards (FollowBots Checker).   
> **¹³** Ban lists you share by hand, as a file or a link.   
> **¹⁴** A newly blocked phrase is also applied to recent messages.   
> **¹⁵** A nuke can be rolled back.   

---

## The compared tools one by one

- **tawmae MODERATION TOOLS** replaced MOD TOOLS in October 2026 and is the closest relative, also built on Streamer.bot. It is stronger when an attack is on: beside queues it can pause channel point rewards, Speaker.bot and browser sources, and one OBS dock holds stream info, filters, polls, rewards, custom commands, a chat log and a list of suspicious users. Its spam filters are simpler, its hate raid protection is switched on by hand, and it needs an extra DLL.
- **Moobot** has the most polished classic filters: twelve of them, intensity presets from Lenient to Strict, and warnings a viewer has to acknowledge. A batch tool bans, blocks or flags long lists of accounts, and those lists can be shared by link. Nothing documented against follow bots or raids.
- **Fossabot** stays solid even on very large channels. Blocked terms with lookalike handling and regex nukes are its strong points, beside filters for links, caps, symbols, emotes, repeated messages and message height. A nuke can be rolled back, `!votekick` lets chat vote someone out, audit logs show what each moderator did, and custom roles decide who may do what. Nothing documented against follow bots or raids.
- **Nightbot** is simple and dependable, with six basic filters. Enough for a small, calm chat.
- **Sery_Bot** is protection first, used by more than 250,000 streamers since 2018, and its protection is on from the moment it joins: it removes spam bots, scam and malicious links and suspect ASCII art, stops hate raids, and silently blocks follow bots and removes their follows. `!offlinelock` switches Shield Mode on after the stream; lurker bots it leaves to you. Behind it sit a known-bot list and pattern detection across its whole network, which no tool running on one PC can match.
- **StreamElements** has ten filters: banned words (groups, regex), caps, emotes, links (allow and block lists, `!permit`), one-man spam, paragraph length, repetition, symbols, Zalgo and even a language filter, with warnings and longer timeouts for repeat offenders. Nothing documented against follow bots or raids; moderation is one part of a bigger platform.
- **Streamlabs Cloudbot** comes with Streamlabs and has seven mod tools: caps, symbols, links (allow and block lists, `!permit`), words (a default slur filter plus your own, regex), paragraphs, emotes and Zalgo, set all at once through presets from Minimum to Maximum. Against a hate raid there is Safe Mode, switched on by hand: it clears chat and the alert queue and puts chat into emote-, follower- and sub-only mode. Nothing documented against follow bots.
- **WizeBot** is an all-round cloud bot that, by its own count, more than a million streamers use. On the protection side it lists anti-spam filters, banned words, link control with `!permit`, warning levels, ban lists shared within communities of channels, a FollowBots Checker that finds and removes bot follows, and an emergency mode for malicious raids, switched on by hand. Its documentation does not break the spam filters down, hence the question marks.
- **Bloopbot** is a newer cloud bot for Twitch and Kick whose commands are built as flows. Its six filters (blocked words with regex, links, caps, symbols, emotes, repetition) see through spaced-out and lookalike letters, nukes can be rolled back, and a follow-bot pack switches Shield Mode on when a burst of follows comes mostly from accounts less than a week old. An AI moderation step comes with its Pro plan.
- **Mix It Up** runs locally like TwitchSentry, but across several platforms, with strikes, a minimum account age and a community word list. Its content filters are fairly basic.
- **PhantomBot** is open source with a web panel and twelve filters, including a spam tracker and fake-purge detection. Its latest GitHub release is v3.23.0.3 from 16 October 2026.

**Not in the table:** Firebot, an open-source desktop bot, names chat moderation among its features but does not document it. BotRix is built around Kick first and documents no filters. Twitch's own AutoMod, Blocked Terms, Shield Mode and suspicious-user detection are on every channel already; the tools above work on top of them.

---

## Where TwitchSentry falls short

- **No protection while the PC is off.** Unless TwitchSentry runs on a server, nothing removes spam or blocks bots while your PC is off. Offline Protection can leave the chat in emote-only or sub-only mode when the stream ends, and those modes stay on after the PC is shut down. Cloud bots protect around the clock, offline chat included.
- **No all-round features.** No timers, points, song requests or other fun features, so most channels probably run a second bot next to it for those.
- **A smaller network.** TwitchSentry depends on its community: the Shared Bot List and the spam feed only know what TwitchSentry installs report, and that is far fewer channels than Sery_Bot, WizeBot, Fossabot or Moobot see every day.
- **A one-person project built with heavy AI help.** AI-written code tends to contain mistakes, and even with extensive testing some can slip through.

## Where TwitchSentry leads

- **It recognises spam by how it is built, not just by a word list**, so it keeps catching spam even when the wording changes from one wave to the next.
- **The Spam Learner learns from what was removed** and reads spam lists that arrive through a community feed.
- **Bots are shared between channels.** The Shared Bot List bans accounts that at least two channels reported, and only the account leaves the PC, never a chat message or the channel.
- **Lurking bots are found too.** The LurkBot Filter looks up silent accounts in the viewer list that have a bot wave's shape, which Sery_Bot leaves to the streamer.
- **Hate raids lock themselves down.** Hate Raid Protection switches Shield Mode on, clears the chat and can ban the whole wave as one `!tsundo` entry, then lifts itself after a quiet spell.
- **Links can be checked for malware**, as an option, with VirusTotal and IPQualityScore.
- **It answers AutoMod's queue and acts on ban evasion.** Unban requests arrive in Discord with the account's history from the logs beside them.
- **It builds on Twitch's own warning system**, with escalation steps such as a three-strikes rule that ends in a restriction, a timeout or a ban.
- **Every timeout, ban and restriction can be taken back** with `!tsundo`, whole nukes included.
- **Around it:** a handy test mode, Discord alerts, Windows notifications, shareable profiles, backup, restore and profile import, with no extra bot account and no external .dll needed.
- **Streamer.bot Deck, Elgato Stream Deck and OBS dock support** to switch profiles, modules, exemptions and test mode, arm Raid or Follow Wave Protection, start a hate raid lockdown or take the last action back.
- **Chat can vote.** Viewers can get a rule breaker timed out or banned together, with every viewer counted once.


## Bottom line

- **For deep spam and scam protection**, *TwitchSentry is the tool to go for*. A cloud bot such as Fossabot or Nightbot adds the features it lacks.
- **For a single bot that does a bit of everything**, Moobot or Fossabot is the most rounded choice.
- **For several platforms at once**, Mix It Up on the PC, Streamlabs Cloudbot or Fossabot in the cloud.

---

### Sources

- [tawmae MODERATION TOOLS](https://tawmae.xyz/moderation-tools), [MOD TOOLS (deprecated)](https://tawmae.xyz/mod-tools)
- [Moobot message filters](https://moo.bot/docs/twitch-chat-auto-mod-bot-message-filters), [batch banning, blocking and flagging](https://moo.bot/docs/banning-blocking-and-flagging-large-numbers-of-twitch-users)
- [Fossabot](https://fossabot.com/), [docs](https://fossabot.com/docs), [nukes](https://fossabot.com/docs/nukes), [lookalikes](https://fossabot.com/docs/lookalikes), [!votekick](https://fossabot.com/docs/commands/default/votekick), [filter list in Bloopbot's migration guide](https://bloopbot.com/docs/coming-from-fossabot)
- [Nightbot filters](https://docs.nightbot.tv/commands/filters), [Nightbot setup](https://docs.nightbot.tv/setup)
- [Sery_Bot docs](https://docs.sery.bot/), [understanding protection](https://docs.sery.bot/understanding-protection/), [spam protection](https://docs.sery.bot/commands/spam/), [all commands](https://docs.sery.bot/commands/all-commands-az/), [FAQ](https://docs.sery.bot/faq/)
- [StreamElements spam filters](https://docs.streamelements.com/chatbot/filters), [on Kick](https://support.streamelements.com/hc/en-us/articles/25794373983122-StreamElements-Chatbot-on-Kick), [on YouTube](https://support.streamelements.com/hc/en-us/articles/18486326016402-StreamElements-Chatbot-on-YouTube)
- [Streamlabs Cloudbot](https://streamlabs.com/cloudbot), [mod tools](https://streamlabs.com/content-hub/post/mod-tools-cloudbot-101), [Safe Mode](https://streamlabs.com/content-hub/post/introducing-safe-mode)
- [WizeBot features](https://wizebot.tv/en/services), [commands](https://support.wizebot.tv/docs/commands)
- [Bloopbot moderation](https://bloopbot.com/docs/moderation), [plans](https://bloopbot.com/docs/what-your-plan-includes)
- [Mix It Up moderation](https://mixitup.bot/docs/moderation)
- [PhantomBot chat moderator](https://github.com/PhantomBot/PhantomBot/blob/master/javascript-source/core/chatModerator.js), [releases](https://github.com/PhantomBot/PhantomBot/releases), [requirements](https://github.com/PhantomBot/PhantomBot#readme)
- [Firebot](https://firebot.app/), [BotRix](https://botrix.live/)
