# ❓ TwitchSentry — FAQ

---

## ⚙️ General

**Q: The settings window won't open or shows an error.**

Since Streamer.bot 1.0.5, an import can leave broken .NET reference paths. Open every `NO TOUCHY!` sub-action, open `Execute Code`, click `Find Refs`, then `OK`.

If one of TwitchSentry's own files (`configs.json`, `messages.json`, `spam.json`) can't be read, the window says which one before it opens and offers to restore it from a backup, let you fix it by hand, or start on the defaults (the damaged file is kept as `.bak`).

If the window opens, the **Status Log** page under Results usually names the problem. Still stuck? [Open an issue](https://github.com/aaskjer/TwitchSentry/issues).

---

**Q: I saved settings but nothing changed.**

Make sure Streamer.bot does **not** run as administrator, and not from inside a .zip or a cloud-synced folder. If it keeps happening, [report it](https://github.com/aaskjer/TwitchSentry/issues).

---

**Q: How do I reset to defaults?**

☰ → **Reset Everything** rewrites `configs.json` and `messages.json` with the defaults, after asking. **Reset current page** only resets the page you are on, and nothing is written until you press **Save**.

---

**Q: How do I try my settings without punishing anyone?**

☰ → **Test Mode**. Nothing is deleted, timed out or banned and no chat mode is switched on; every module posts what it *would* have done instead. It switches itself off after **Test Duration (Minutes)** on General Settings (5 by default), counted down in the notice strip.

---

**Q: What is Expert Mode?**

Message Filter, Raid Protection, Follow Protection and Spam Scoring each start with a **sensitivity slider** that sets the numbers behind it. ☰ → **Expert Mode** shows those numbers for tuning by hand, plus a *Custom* step on the slider that keeps your own values. Switching it on changes no setting.

---

**Q: Can I get rid of a notice at the top of the window?**

Its **✕** hides it for good. ☰ → **Show hidden notices again** brings them all back.

---

**Q: Where is the longer explanation of a setting?**

The **?** in a card's corner opens the **Manual** page (under Help) at that card's section, and **← Back to …** takes you back. Installing, the deck buttons and where the files live are in the [online Manual](Manual.md).

---

## 🧭 Commands

Commands are never scanned as ordinary chat. **Allow Chat Commands** and **Allow Whisper Commands** on General Settings decide where they are accepted. `!tsundo` in chat works even with **Allow Chat Commands** off: that switch is about editing the lists.

| Command | Who | What it does |
|---|---|---|
| `!tsundo` | Moderators | Takes back TwitchSentry's last timeout, ban, restriction, monitoring or follow block, whichever module did it |
| `!tsundo @user` | Moderators | Takes back the last one for that viewer |
| `!permit @user [seconds]` | Moderators | Grants a temporary link permit |
| `!endpermit [@user]` | Moderators | Ends that viewer's permit, or all of them |
| `!checklink <url>` / `!linkcheck <url>` | Anyone | Scans a link with Check Link *(anyone)* |
| `!vote @user` | Anyone | Starts or joins a vote-kick *(anyone)* |
| `!endvote` | Moderators | Ends the running vote early |
| `!wladd` / `!wlremove` / `!wllist` | Moderators | Whitelisted Domains |
| `!amadd` / `!amremove` / `!amlist` | Moderators | AutoMod Whitelist |
| `!euadd` / `!euremove` / `!eulist` | Moderators | Excluded Users |
| `!egadd` / `!egremove` / `!eglist` | Moderators | Excluded Groups |
| `!veuadd` / `!veuremove` / `!veulist` | Moderators | Vote-Excluded Users |
| `!vegadd` / `!vegremove` / `!veglist` | Moderators | Vote-Excluded Groups |
| `!kwadd` / `!kwremove` / `!kwlist` | Moderators | Spam Keywords |
| `!tldadd` / `!tldremove` / `!tldlist` | Moderators | Spaced-URL TLDs |

---

**Q: How far back does `!tsundo` reach?**

The last 25 actions from the last 12 hours. If Twitch refuses the undo, the entry stays so you can try again. A deck button can do the same (`tsUndo`).

---

## 🎛️ Deck Buttons

**Q: Can I switch things from a Stream Deck or a Streamer.bot Deck?**

Yes. A key runs the **`[TS] - Deck`** action with an argument: `tsProfile` (switch profile), `tsModule` (module on/off), `tsExempt` (Followers/Subscribers/VIPs), `tsTestMode`, `tsRaid` (arm Raid Protection now) or `tsUndo`. One key can carry several, e.g. `Under Attack` plus `arm` as a panic button. Setup and examples: [Manual → Deck buttons](Manual.md#deck-buttons).

---

**Q: Does the settings window notice a key press?**

Yes. Within a couple of seconds its notice strip says so and offers **Reload**. Saving without reloading keeps what the key changed.

---

## ⚖️ Profiles

**Q: What is the difference between a profile and a backup?**

A backup (**Backup & Restore**, under Help) is everything: settings, chat replies, learned spam data, logs. A profile (☰ → **Profiles...**) is only the policy, how strict this channel is. 261 of the 297 settings in `configs.json` travel in a profile; your Discord webhook, API keys, whitelist, every list naming people and install-specific settings stay out. That is why a profile can be shared and a backup can't.

---

**Q: I picked Under Attack. How do I get back?**

☰ → **Profiles...** → **Balanced**. All built-in profiles name the same settings, so Balanced undoes everything Under Attack turned on. Settings no built-in profile mentions keep your value.

---

**Q: What does *(modified)* in the title bar mean?**

The settings the current profile names no longer match it. A **built-in profile** names 34 settings (the four sensitivity sliders, the 23 dials behind them and seven switches), so only those count. A **saved profile** names all 261, so almost any change counts.

---

**Q: Can I keep my own profiles?**

Yes: **Save Current Settings** in the Profiles dialog writes them to `TwitchSentry/Settings/Profiles` under a name you choose (the five built-in names are reserved). **✎** renames one, **↺** overwrites it with what you are running now, and a file dropped into that folder shows up in the list. Nothing in the window deletes a profile file. Each profile shows *would change N settings* with every change listed before you pick it.

---

**Q: I imported someone's profile and my whitelist didn't change. Broken?**

No. A profile carries how strict to be, never who is exempt. Your whitelist, excluded and trusted users, AutoMod allow list and Follow Protection block list stay yours.

---

**Q: Is it safe to share a profile publicly?**

Yes. No webhook URL or API key is ever written into one, and the same filter runs on import, so a hand-edited file can't put a webhook into your settings either. Settings your version doesn't know are ignored, and a file that isn't a profile is refused. ☰ → **Share With Others...** shares a profile through GitHub so others can import it.

---

## 💬 Message Filter

**Q: What does it check?**

*How* someone chats: account age, caps and repeated characters, emote spam, and flooding or repeated messages. Each check has its own switch (**Account Check**, **Caps Check**, **Emote Check**, **Flood Check**); untick all four to switch the filter off.

One signal is not enough, because people shout and spam emotes when something good happens: it takes two on the same message, or one that is hard to do by accident. A repeated message is enough on its own. A young account only makes the other signals weigh more, and regulars need more against them than strangers. **Require Two Signals** and **Act On Account Age Alone** under Expert Tuning change that balance.

---

**Q: Can a command be flagged as a violation?**

A moderator's or the broadcaster's never: they are exempt from every filter. A viewer's `!checklink <link>` is left to Check Link while Check Link is on, and only a malicious result removes it. Any other message is checked whatever word it starts with, so a command in front of a link is not a way past the filters.

---

**Q: What is Escalation?**

A chat-wide safety net: when enough *different* users trigger violations in a short time, a Twitch chat mode (slow, follower-only, emote-only or sub-only) is switched on and lifted again once things calm down. The mode depends on the kind of wave, and the **What actually happens** table shows the order live from your ticks. Emote-only and sub-only are opt-in.

---

## 🚫 Spam Scoring

**Q: What does it catch?**

Keywords, custom patterns, disguised links (`twitch. tv`), lookalike characters, @mentions of accounts that don't exist, and voucher codes. None of them is a verdict alone: a message has to look like an **advert**, with at least two parts out of somewhere to go (Destination), something for sale (Offer), a way to redeem it (Instrument), a bot's random `@handle` (Tag) and wording seen in spam before (Signature). The sensitivity slider shifts that balance; **Require Two Parts** is a separate decision and keeps its own switch.

---

**Q: What is the conversation scam?**

The "sales chat": friendly questions, then "your channel looks empty", then a suggestion (logo, overlay, VTuber model), then the pitch ("I work with streamers..."). No single message is spam, so TwitchSentry tracks the four stages per account over 45 minutes. Three in order, with the pitch last, closes it; regulars need all four. Its own action: **Report Only**, **Timeout** (a day by default) or **Ban**.

---

**Q: Where do the block lists come from, and do they update?**

From the Spam Learner, the public Stop The Bots list, and the **spam feed**: with **Receive New Entries** on (Known Patterns page), new entries arrive every three hours. Each arrives once, so an entry you delete stays deleted, and the feed only touches the plain-text lists, never your custom or voucher patterns. **Share With Other Streamers...** on the same card offers your own entries for everyone.

---

**Q: Can I add my own patterns?**

Yes, on **Known Patterns**: keywords, strong keywords, domains, TLDs, custom patterns and voucher patterns.

---

## 🧠 Spam Learner

**Q: What does it do?**

It studies messages that were actually removed and suggests new keywords, phrases and domain endings. Suggestions wait on the **Suggestions** page until you approve them, or until **Auto Promote Trusted Rules** promotes those that have proven themselves.

---

**Q: It suggested a normal word like "google". Why?**

Only content violations feed it (keywords, patterns, links), never behaviour like caps or flooding. **Ignore Terms**, your channel and bot names, a clean-chat comparison and a brand denylist filter most mistakes. Reject the rest and add it to **Ignore Terms**.

---

**Q: Probation vs. trusted?**

New suggestions start on probation and become trusted after **Probation Runs Required** learner runs. Only trusted ones can be auto-promoted.

---

**Q: How do I clear bad suggestions?**

**Clear File** on the Suggestions page. It doesn't touch your active `spam.json` rules.

---

**Q: What is Decay?**

Cleanup of rules and suggestions that stopped appearing in chat. Entries starting with `!` are protected.

---

**Q: Where can I see what was removed?**

Under Results: **Violation Log** lists every message TwitchSentry acted on this month; **Clean Chat Log** is the sample of normal chat the learner compares against. Both have search and a per-account filter.

---

**Q: Where did last month's log go?**

Each month starts a new `action-log.txt` and `violation-log.txt`. The previous month is moved aside in the same `Logs` folder as `action-log-2026-09.txt` / `violation-log-2026-09.txt` and so on. Nothing is deleted, so you can remove old months by hand whenever you like.

---

## 🔗 Link Filter & Whitelist

**Q: Can I switch the Link Filter or Spam Scoring off?**

No, they are the core. Narrow them instead: whitelist domains, exempt roles or viewers on General Settings, or hand out a `!permit`.

---

**Q: There is no Link Filter page. Where are its settings?**

**Action On Violation** and **Timeout Duration (Seconds)** are at the top of the Message Filter page (shared with Spam Scoring and the Message Filter). **Whitelisted Domains** and **Always Allowed** are on General Settings. **Check Every Posted Link** is on the Check Link page.

---

**Q: Do I have to whitelist my own clips?**

No. **Always Allowed** on General Settings covers them. **Only Your Channel** allows links with your channel's name in them (`twitch.tv/<you>/clip/<id>`, `youtube.com/@you`); **Any Channel** allows that kind of link from everybody, so tick those only if you are fine with that. Channel names come from the accounts Streamer.bot is signed in to.

---

**Q: How does the whitelist match?**

| Entry | Matches |
|---|---|
| `youtube.com` | Exactly that address, nothing after it |
| `youtube.com/*` | Anything after `youtube.com/` |
| `*.youtube.com/*` | Any subdomain (`music.youtube.com`) and anything after it, but not bare `youtube.com` |
| `twitch.tv/aaskjer` | Exactly that channel link |

So `twitch.tv/yourname` does not cover your clips; add `twitch.tv/yourname/*` for that.

---

**Q: What happens to a link that isn't whitelisted?**

It gets your configured action. With **Check Every Posted Link** on, it is also scanned for malware. Exempt viewers are skipped by both.

---

## 🚨 Raid Protection

**Q: How is it different from the Message Filter?**

It arms itself for a while after an incoming raid, is stricter, and adds **swarm detection**: several accounts posting near-identical messages at once, which is decisive on its own. It has its own slider, escalation ladder and **Progressive Escalation**. A deck button (`tsRaid`) arms it without a raid.

---

**Q: Which chat mode does a raid get?**

The dominant pattern decides: emote spam prefers slow mode, fresh accounts follower-only, caps spam emote-only. Only modes you enabled are used.

---

## 👣 Follow Protection

**Q: What does it do?**

It watches follows. When enough different accounts follow within a short window (8 in 30 seconds by default), each is checked for a young account, default avatar, empty profile and throwaway name; age decides whether the cosmetic checks count. Off by default, and **Report Only** by default. On **Block**, the follow is removed and the account can't follow again. Blocked accounts are listed on the page, and `!tsundo` lifts the last block.

---

## 👾 AutoMod

**Q: What does it do?**

It answers the messages Twitch's AutoMod holds back, by the level and categories you set, so nobody has to sit in the queue. **AutoMod Categories** limits it to certain categories; empty means all.

---

**Q: Held messages are still waiting. What did I miss?**

The switch in the AutoMod page header. It ships off.

---

## 🕵️ Check Link

**Q: Which services does it use?**

VirusTotal (required, free key) and optionally IPQualityScore. IPQS flags links at a fraud score of 75, or 40 for recently registered domains, a classic phishing sign.

---

## ⚠️ Twitch Warn

**Q: What is Twitch Warn?**

Twitch's own warning screen: the viewer has to click through it before they can chat again. A step below a timeout.

---

**Q: How does escalation work?**

On the **Warning Escalation** card: after **Warns Before Final Warning** warnings the viewer gets a final warning, and the next violation gets the **Escalation Action**: Timeout, Ban or **Restrict** (they stay in chat, but only moderators see their messages). Counts reset after **Warn Count Reset (Hours)** without a violation.

**Monitor From The Final Warning** also flags the viewer as monitored on Twitch with the final warning. **Count Warnings From Moderators** counts a `/warn` from your mods towards the same ladder; it needs the trigger *Twitch > Moderation > Warned User* on the TwitchWarn action. Restrictions and monitoring are lifted with `!tsundo`.

---

## 🔓 Permits

**Q: What is a permit?**

A temporary exception that lets one viewer post a link. It waives the link, spam, message and raid checks for them; with **Check Every Posted Link** on, their links are still scanned for malware.

---

**Q: Can several viewers hold one?**

Yes, each with its own countdown. A running permit is never extended: end it with `!endpermit @user` first. Permits are cleared when Streamer.bot restarts.

---

**Q: What stops a mistyped duration?**

**Max Permit Duration Seconds** caps every permit, with a hard ceiling of 24 hours.

---

**Q: Can viewers grant themselves one?**

Yes, with **Allow Self-Permit** and a Channel Points reward: point the reward's trigger at the Permit action and put its ID in **Self-Permit Reward ID**. Turn the reward's **Skip Reward Requests Queue** OFF, or TwitchSentry can't refund points when a redemption can't become a permit.

---

## 🗳️ Voting

**Q: How does vote-kick work?**

`!vote @username`. Enough unique votes inside the time window time the viewer out, or ban them with **Allow Ban**. Otherwise the vote resets.

---

**Q: Can viewers be protected from votes?**

Yes: subscribers and VIPs globally, plus users and Streamer.bot groups on the exclusion lists. Everyone above VIP can never be voted against.

---

## 🦝 Discord Alerts

**Q: What can it post?**

Twenty-one kinds of event, each with its own switch: deletions, timeouts, bans; warnings and escalations; raid arming and raid actions; AutoMod denials, allows, restrictions and blocks; malicious and suspicious scans; permits granted, expired and revoked; follow waves and blocked followers; Shield Mode; Spam Learner auto-applies; and settings changed by chat command.

---

**Q: An alert says *TIMEOUT REFUSED*.**

Twitch turned the action down, so nothing happened to the viewer. Usual reasons: the target is a moderator or the broadcaster, the message was already removed, or the Streamer.bot Twitch account lacks a scope (`moderator:manage:banned_users`, `moderator:manage:chat_messages`, `moderator:manage:warnings`). The **Status Log** names which; a missing scope is fixed by re-authorising the account in Streamer.bot.

---

**Q: Will a raid get me throttled by Discord?**

No. Alerts are queued, and a burst is merged into messages of up to ten.

---

**Q: Can I change the name alerts post under?**

**Display Name** and **Avatar URL** on the Discord Alerts page. Clear them to use the webhook's own. Discord refuses names over 80 characters or containing *discord* or *clyde*, so TwitchSentry drops such a name instead of sending it.

---

## 🔔 Windows Notifications

**Q: Can TwitchSentry tell me things on the desktop?**

Yes, on the **Windows Notifications** page (Setup): a new TwitchSentry release and a deck button that could not do what it was asked (both on by default), and what a deck button just did (off by default). They show while the settings window is closed too. A profile never carries these switches.

---

**Q: The test notification never shows up.**

Windows is holding it back. Check *Do Not Disturb* (*Focus Assist*) and *Settings → System → Notifications*, where Streamer.bot has to be allowed to send notifications.

---

## 🏠 Home

**Q: Can I change anything on Home?**

No, it only reports. Its shortcuts lead to the page that owns each setting.

---

**Q: What do the numbers count?**

*Activity* counts lines in `action-log.txt` (today, the last seven days, all time; all time includes the earlier months' `action-log-<yyyy-MM>.txt` files); the details below it cover the last seven days. *What It Knows* counts the active block lists and waiting suggestions.

---

## 🐞 Reporting A Bug Or An Idea

**Q: How do I open a ticket?**

☰ → **Report...**, or **Report An Issue Or Idea** on Home. Fill in the form and TwitchSentry opens GitHub's new-issue page with everything filled in. Nothing is sent from the window: you submit it yourself on GitHub, which needs a GitHub account.

---

**Q: What does it say about my setup?**

Versions (TwitchSentry, Streamer.bot, language file), profile, whether betas are announced, language and theme, expert and test mode, which modules are on, the sensitivity steps, whether the API keys and webhook are **set or not set**, and your Windows version and screen size. Never your channel name, keys, webhook URL or file paths. It is shown in full before anything opens.

---

**Q: What helps most in a ticket?**

A line from the **Status Log** page. It usually names the problem.

---

## 🌍 Languages

**Q: Can I use TwitchSentry in my language?**

English, German, Spanish, French and Brazilian Portuguese ship, and Dutch comes from the community. ☰ → **Change Language**, pick one, **Use This Language**. Missing translations fall back to English.

---

**Q: The bot still writes English in chat.**

Intended. Translations cover the settings window only. What the bot says comes from the **Messages** pages, in your own words and language.

---

**Q: Can a chat message use a viewer's pronouns?**

Yes, for viewers who set theirs on [pronouns.alejo.io](https://pronouns.alejo.io). Switch on **Use Viewer Pronouns** (General Settings → Behavior) and put `{pronoun:he|she|they}` into a message, with the words your language needs: the first form is for he/him, the second for she/her, the third for they/them and anyone not known. Other pronouns (xe/xem, fae/faer, it/its…) get the first form with their own words, as long as it is English. Details: [Manual → pronouns](Manual.md#speaking-of-a-viewer-by-their-pronouns).

---

**Q: Can I fix or write a translation?**

Yes. One text that reads badly: ☰ → **Report...** → *A translation*, pick the text and write the better wording. A whole language: ☰ → **Share With Others...** → *A complete translation file*. The files live in `TwitchSentry/Settings/Language/` (📁 in the Change Language dialog); each key is the exact English text, each value its translation, and placeholders like `{user}` stay as they are. Shipped languages are refreshed from GitHub, so a file of your own belongs under an unused code.

---

## 🔄 Updates

**Q: How do I know a new version is out?**

The settings window checks GitHub whenever it opens and shows a notice at the top, stable releases and betas alike. A beta notification banner has a button that allows you to ignore future beta notifications. ☰ → **Show hidden notices again** brings betas back.

---

## 💾 Backup & Restore

**Q: What should I back up?**

`configs.json` and `messages.json` (every setting and chat message) and `spam.json` (what the Spam Learner built up) can't be recreated; those are ticked by default, and so are the language files. Caches download themselves again.

---

**Q: Where should backups go?**

Ideally another drive, a USB stick or a cloud-synced folder. Left empty, **Backup Folder** uses `TwitchSentry/Backups`, which survives a bad file but not a bad disk.

---

**Q: Is a restore safe if I pick the wrong backup?**

Yes. The current state is saved first, a restore only replaces what the backup contains, and it never deletes anything.

---

**Q: Can I copy a file back by hand?**

Yes. A backup is a plain folder with the same layout as TwitchSentry. Streamer.bot picks up the changed file without a restart.

---

# Is TwitchSentry AI slop?

Partially, yes. It was built with heavy AI assistance and input from the Streamer.bot community, and it is tested against real chat before it ships. AI-assisted code can have bugs, so please [open an issue](https://github.com/aaskjer/TwitchSentry/issues) when you find one.
