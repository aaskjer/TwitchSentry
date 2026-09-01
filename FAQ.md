# ❓ TwitchSentry — FAQ

---

**Q: I saved settings but nothing changed. Why?**

Settings are re-read from disk automatically whenever the file's been updated — no Streamer.bot restart needed. Just click **Save** (or **Save & Exit**) and the next chat message will already use the new config.

---

**Q: How do I reset everything to defaults?**

**Reset everything**, in the ☰ menu. It asks for confirmation, then rewrites both `configs.json` and `messages.json` with factory defaults and reopens the window. This cannot be undone.

If you only want to undo what you did to one page, **Reset this page** is right above it. That one puts the current page's controls back to their defaults and leaves every other page alone — and nothing is written until you press **Save**, so it is safe to look at first.

---

**Q: Where did the buttons along the bottom go?**

Into the **☰ menu**, in front of the search box at the top left. It holds expert mode, test mode, *Show hidden notices again*, the language files, the light/dark theme, and both resets. The bottom bar is now only **Save**, **Save & Exit** and **Cancel**, plus the note telling you whether you have unsaved changes.

---

**Q: How do I try my settings out without anyone getting timed out?**

**Test mode**, in the ☰ menu. While it runs nothing is deleted, timed out or banned: every module posts what it *would* have done instead, so you can point a real chat at your settings without somebody being punished for helping you test them. The chat modes stay off too — a dry run that puts your channel into follower-only is not a dry run.

It ends on its own after the time set on General Settings (five minutes by default) and the notice strip counts it down. The deadline is stored as a timestamp rather than an on/off flag, so a chat is never left unguarded because somebody forgot to switch it back.

---

**Q: What is expert mode?**

The Message Filter, Raid Protection and Spam Scoring pages each lead with a **sensitivity slider**, from Very relaxed to Very strict, with a line under it saying what the step actually means. It scales that page's threshold, standing in for the dozen individual numbers underneath.

Expert mode, in the ☰ menu, is what shows those numbers. They keep working exactly as before for anyone who wants to tune them by hand; the slider just moves them for you. Nothing is hidden from you permanently, and turning it on changes no setting by itself.

---

**Q: A notice appeared at the top of the window. Can I get rid of it?**

Yes — the **✕** on it. That is permanent: a notice you have read and answered should not keep coming back every time you open the window.

If you want them back, **Show hidden notices again** in the ☰ menu empties the list and rebuilds the window, so every notice is worked out again from scratch. It greys itself out when nothing is hidden.

---

**Q: The Settings GUI won't open or throws an error. What do I do?**

Check the Streamer.bot log for the actual error — TwitchSentry logs failures with a `[TwitchSentry/...]` prefix. If it's a malformed `configs.json`/`messages.json`, the simplest fix is deleting the broken file so a fresh default gets written. If it keeps happening, please report it [here](https://github.com/aaskjer/TwitchSentry/issues).

If the window *does* open, the **Status Log** page under Results shows the same thing without leaving TwitchSentry: it pulls every `[TwitchSentry/...]` line out of the Streamer.bot log, with a "Problems only" tick. That is the page for an API key still on its placeholder, a download that failed, or an action Twitch refused — none of which is announced in chat.

---

## 💬 Message Filter

**Q: What does Message Filter actually check?**

It looks at *how* someone is chatting, not specific words: account age, ALL CAPS / repeated-character spam, emote spam, and posting too fast or repeating the same message. Each of those four has its own switch, so you can run only the ones you want.

They do not each stand on their own, though, and that is the point. Shouting, spamming emotes and typing fast are circumstantial: people shout, and people spam emotes when something good happens. So the evidence has to compose — at least two of them on the same message, or one that is hard to do by accident. A repeated message is decisive and still enough on its own.

A young account is a **risk factor rather than evidence**: on its own it never gets anyone actioned, it makes whatever else the message tripped count for more. And someone with a long history in your chat has their score scaled down before it is measured, so a regular needs more against them than a stranger does.

Two switches under **Expert Tuning** turn the older, stricter behaviour back on if you want it: **Require Two Signals**, and **Act On Account Age Alone**.

**Q: Can a moderator command be deleted or flagged as a violation?**

No. TwitchSentry recognizes commands — both its own built-in ones and anything else you've configured in Streamer.bot — and skips them entirely before any scanning happens, so a command never reaches the Account Age check or any other filter.

**Q: How do I switch the whole Message Filter off?**

Untick its four checks: Account Check, Caps Check, Emote Check and Flood Check. There is no separate module switch — each check carries its own, and a second one sitting above them only made "the module is on but nothing happens" harder to work out.

**Q: What is "Escalation"?**

A chat-wide safety net layered on top of the per-user checks above. If enough *different* users trigger violations within a short window (a spam wave, not one annoying person), TwitchSentry automatically activates a Twitch chat mode (slow mode, follower-only, emote-only, or sub-only) to protect the whole chat, then lifts it automatically once things calm down. Which mode gets picked depends on the dominant spam pattern detected (e.g. an emote-spam wave prefers slow mode; a wave of brand-new accounts prefers follower-only).

You do not have to take that on trust: the table at the bottom of the section — **What actually happens** — draws the whole preference order live from the checkboxes above it. Step numbers renumber as you tick modes, and a mode you have switched off is struck through where it would have been used.

Sub-only and emote-only are **not** on by default. They are the two drastic modes, so they are opt-in.

---

## 🚫 Spam Filter (the Spam Scoring page)

**Q: What kinds of spam does it catch?**

Keyword matches, custom patterns (flexible text matching for things a plain word list can't catch), spaced-out/disguised links (`twitch. tv`), fancy lookalike-Unicode obfuscation, excessive @mentions (especially to nonexistent accounts), and gift/voucher-code-shaped strings.

None of those is a verdict by itself. TwitchSentry asks whether the message is built like an **advert**, and an advert has parts: somewhere to go (Destination), something being sold (Offer), a way to redeem it (Instrument), the random `@handle` a spam bot signs with (Tag), and wording this channel has seen from spam before (Signature). One part on its own is a coincidence — plenty of ordinary messages have one. Two parts together is an advert, and each part contributes its value at most once however many times it was found.

The **sensitivity slider** at the top of the Spam Scoring page is how you shift that balance. The individual weights behind it are under **Expert Tuning — Scoring**, in expert mode. The slider deliberately does not touch **Require Two Parts**: "act on weaker evidence" and "act on a single part of an advert" are different decisions, and the second one keeps its own switch.

**Q: What is the "conversation scam" and why does it have its own action?**

It is the sales approach that arrives as a conversation rather than as an advert: friendly questions about your stream, then a remark that your channel looks empty, then a suggestion (a logo, emotes, an overlay, a VTuber model), and finally the offer — "i work with streamers, i can show you my previous work". No single message is spam, so the normal rules cannot see it; the tell is the order.

Four stages are tracked per account inside a 45-minute window, and they only count moving forwards. Two stages never do anything. Three, with the pitch last, is what closes it.

Being a regular here does **not** exempt an account from this check — it raises the bar to all four stages instead of three. Trust raises the bar; it never removes it. Exempting familiar accounts outright was backwards, because the accounts running this scam sit in a channel for hours on purpose, chatting about nothing, which is exactly how they earned that standing. It also meant a fresh account could switch the detector off for itself by posting two dozen throwaway lines first.

Every beat is written to the log as it lands, so an arc that does not close leaves a trail explaining why.

It gets its own action because it is a different animal from the usual bot: those post once and disappear, while these accounts sit in the channel for hours. **Report Only** is silent in chat and only writes the log and the Discord alert, **Timeout** removes them for the configured time (a day by default), **Ban** removes them for good.

**Q: Can I add my own detection patterns?**

Yes — the **Known Patterns** page lets you add custom keywords, custom patterns, and voucher-code patterns directly, on top of whatever the Spam Learner suggests.

---

## 🧠 Spam Learner

**Q: What does the Spam Learner do?**

It watches messages that actually get deleted/timed-out/banned and tries to spot new spam keywords, phrases, and domain endings automatically. New finds start as pending suggestions (the Suggestions page) for you to review, and only get promoted to the real, active rule list (`spam.json`) once they've built up enough of a track record — either you approve them yourself, or the learner promotes them automatically if **Auto Promote Trusted Rules** is turned on.

**Q: The Spam Learner suggested a totally normal word (like "google"). Why?**

Only *content* violations feed the learner — a message that matched a keyword, pattern or link rule. *Behavioral* violations (young account, caps spam, flooding) never contribute words, because the fact that someone typed too fast tells you nothing about which of their words are spam.

Several guards sit on top of that: a permanent **Ignore Terms** list, automatic protection for your broadcaster and bot account names, a "clean chat" sample the learner compares against so everyday words get suppressed, and a denylist that keeps major brand names (Google, YouTube, Twitch, Discord, etc.) from ever being suggested as blocked domain endings.

A word that slips past all of that is still only a *suggestion*. Reject it on the Suggestions page, and add it to **Ignore Terms** so it can't come back.

**Q: What's the difference between "probation" and "trusted" status?**

A brand-new suggestion starts on **probation**. Once it's been seen across enough separate learner runs (see **Probation Runs Required**), it's upgraded to **trusted**. Trusted suggestions are the only ones eligible for automatic promotion into `spam.json` if Auto Promote is enabled — probation suggestions always need your manual review first.

**Q: How do I get rid of a bunch of bad/stale suggestions?**

Use the **Clear File** button on the Suggestions page — it wipes every pending suggestion and starts fresh. It does **not** touch your active `spam.json` rules, only the pending list.

**Q: Where can I see what was removed, and what was left alone?**

Under **Results**. The **Violation Log** lists every message TwitchSentry acted on, exactly as it was posted — that is the page to open when a removal looks wrong. The **Clean Chat Log** lists the sample of ordinary chat that was deliberately left alone, roughly one message in ten, which is what the Spam Learner compares its candidates against so an everyday word never becomes a rule. Both have a search box and a per-account filter, and both show the full line under the list, because chat messages are usually wider than the row.

**Q: What is "Decay"?**

Automatic cleanup. When enabled, both active rules and pending suggestions are checked against recent chat history, and get removed if they've stopped showing up — keeps the rule list from accumulating dead weight from one-off spam campaigns. Entries you added by hand (prefixed with `!` in `spam.json`) are protected from decay by default.

---

## 🔗 Link Filter & Whitelist

**Q: Can I switch the Link Filter or the Spam Filter off?**

No, and that is deliberate — those two are the core of TwitchSentry, and every other module is built around them. What you can do is narrow them: whitelist the domains you want allowed, exempt roles or specific viewers under General Settings, or hand out a `!Permit` for a one-off. Every other module has its own on/off switch precisely because it is optional; these two are not.

**Q: Where did the Link Filter settings page go?**

Only the page was dissolved — the module itself is unchanged. **Check Harmful Domains** and its four notification tickboxes are on the **Check Link** page, under "Behavior On Harmful Domains". **Action On Violation** and **Timeout Duration** are at the top of the **Message Filter** page, because the Link Filter, the Spam Filter and the Message Filter have always shared those two. **Whitelisted Domains** is on **General Settings**, where it always was.

**Q: How does the whitelist actually match URLs?**

Three patterns, each behaving differently:

| Entry | Matches |
|---|---|
| `youtube.com` | That exact address only — nothing after it |
| `youtube.com/*` | Anything after `youtube.com/` |
| `*.youtube.com/*` | Any subdomain (e.g. `music.youtube.com`) plus anything after it, but **not** bare `youtube.com` |
| `twitch.tv/aaskjer` | That exact channel link only, nothing after it |

An entry without a trailing `/*` is always an **exact match** — it will not accidentally allow sub-pages, clip links, or anything else nested under it.

**Q: My own clip link got blocked even though I whitelisted my channel. What's going on?**

Your entry is an exact match. A bare `twitch.tv/yourname` allows that one link and nothing nested under it, so a clip or sub-page URL is still treated as an ordinary link.

Add the wildcard if you want everything under your channel covered: `twitch.tv/yourname/*`. Keep both entries if you also want the bare channel link itself allowed.

**Q: What happens to a link that isn't whitelisted?**

It's scored and, depending on your configured action, deleted/timed-out/banned. If **Check Harmful Domains** is enabled, the same link is *also* sent to the Check Link module afterwards and scanned for malware — the scan sits on top of the ordinary rule, it does not replace it. Anyone your exemptions cover is skipped by both: the broadcaster, moderators, the excluded lists, and whichever of VIPs, subscribers and followers you have exempted.

---

## 🚨 Raid Protection

**Q: How is this different from Message Filter's normal flood checks?**

It's a stricter, temporary version of the same idea that only arms itself for a limited window right after an incoming raid, and adds **swarm detection** — spotting multiple different accounts posting near-identical messages at once, the signature of a bot raid rather than real viewers. Like a repeated message in the Message Filter, a swarm is decisive on its own; velocity and the rest are circumstantial and mean something only in combination.

It has its own sensitivity slider, its own escalation ladder and its own **Progressive Escalation**, running the same algorithm under the same names as the Message Filter. Before that, progressive escalation was a Message Filter setting only, which meant a second wave of the same pattern during a raid re-picked the mode that was already running and did nothing.

**Q: What determines which chat mode gets activated during a raid?**

The dominant spam pattern detected during the wave: emote spam prefers slow mode, waves of fresh/throwaway accounts prefer follower-only (locks out accounts that just followed), and caps/character spam prefers emote-only (makes text spam impossible). Only modes you've enabled are eligible — if your preferred mode is off, it falls through to the next one in the preference order.

---

## 👾 Twitch AutoMod Integration

**Q: What does this module actually do?**

Twitch's own built-in AutoMod holds back messages it thinks might be harmful and normally waits for a moderator to manually approve or deny each one. This module lets TwitchSentry make that call automatically instead, based on the AutoMod level and categories you configure.

**Q: My held messages are still waiting for a moderator. What did I miss?**

**Use AutoMod**, at the top of the AutoMod page — it ships off, and until it is ticked TwitchSentry leaves held messages alone. (In releases before v1.4.0 that tickbox was ignored and the module acted either way, so an install that has been auto-denying without you ticking anything will go quiet until you do.)

**Q: Can I limit it to specific categories instead of everything AutoMod flags?**

Yes — the **AutoMod Categories** setting lets you list exactly which categories to act on (Profanity, Racism, SmartDetection, etc.). Leave it empty to act on everything AutoMod holds.

---

## 🕵️ Check Link (Malicious Link Scanning)

**Q: What services does it use to scan links?**

VirusTotal (required — free API key) and, optionally, IPQualityScore (IPQS) for a second opinion, especially good at catching brand-new/throwaway phishing domains.

**Q: How is the IPQS fraud score threshold chosen?**

IPQS rates every link from 0 (safe) to 100 (certainly malicious). The default threshold is 75, matching IPQS's own "flag for review" guidance (they recommend 85 to outright block). There's a separate, stricter threshold (default 40) that only applies to domains IPQS also flags as *recently registered* — brand-new throwaway domains are a classic phishing tactic, so they're held to a lower bar.

---

## ⚠️ Twitch Warn & Escalation

**Q: What is "Twitch Warn"?**

Twitch's own built-in warning system — the flagged viewer has to read and click through a warning screen before they can chat again. It's a step below a timeout: firm, but it doesn't remove them from chat entirely.

**Q: How does escalation to a timeout/ban work?**

Once a viewer racks up enough warnings (**Warns Before Final Warning**), the *next* violation escalates straight to a timeout (or ban, if **Use Ban** is enabled) instead of another warning. Warning counts reset automatically after a configurable number of hours without a new violation.

---

## 🔓 Permits

**Q: What's a permit?**

A temporary, per-user exception that lets someone post a link even while Link Filter would normally block it — useful for letting a specific viewer share something once without changing your whitelist. It waives the ordinary link, spam, message and raid checks for that viewer; if **Check Harmful Domains** is on, their links are still scanned for malware.

**Q: Can more than one viewer hold a permit at a time?**

Yes. Each permit runs its own countdown, so permits granted at different moments end at different moments. A permit that is already running is never extended — `!Permit` for someone who already holds one is refused, so end it with `!EndPermit @user` and grant a fresh one. `!EndPermit` with no name ends every active permit at once.

Permits are deliberately not remembered across restarts: closing Streamer.bot clears them all.

**Q: What stops a mistyped duration?**

**Max Permit Duration Seconds** on the Permits page. Any longer time a moderator types is cut back to it, and so is a default or self-permit duration set above it. There is a hard ceiling of 86400 seconds (24 hours) whatever you configure.

**Q: Can viewers grant themselves a permit?**

Yes, if **Allow Self-Permit** is enabled — viewers can redeem a Channel Points reward to grant themselves a temporary permit without needing a moderator. Point that reward's Streamer.bot trigger at the same Permit action and put its ID in **Self-Permit Reward ID**.

Set the reward up with **Skip Reward Requests Queue** turned OFF. That is what lets TwitchSentry give the points back when a redemption cannot become a permit — the viewer already holds one, or the feature is off. A reward that skips the queue is spent the moment it is redeemed and Twitch will not allow a refund.

---

## 🗳️ Voting

**Q: How does vote-kick work?**

Viewers vote against someone breaking chat rules (e.g. `!vote @username`). Once enough unique votes are cast within the time window, that user is automatically timed out (or banned, if **Allow Ban** is enabled). If the window runs out before enough votes come in, the vote resets.

**Q: Can specific users be protected from being voted against?**

Yes — subscribers and VIPs can be excluded globally, and you can add specific usernames or Streamer.bot groups to the exclusion lists.

---

## 🔔 Discord Webhook Alerts

**Q: What can it send alerts for?**

Deletions, timeouts, bans, raid escalations, AutoMod holds, malicious/suspicious link scans, TwitchWarn actions, permit grants/revokes, config changes made via chat commands, and Spam Learner auto-applies — each toggled independently on the **Discord Alerts** page, under Setup.

**Q: What does an alert look like?**

User, Action, Score, Triggers, Message and the rest arrive as separate labeled fields rather than one dense block, and internal details like raw regex patterns are summarized in plain terms instead of being dumped verbatim.

---

## 🧭 Commands

TwitchSentry ships with these built-in commands for managing its lists from chat (moderator-only unless noted):

| Command | Manages |
|---|---|
| `!checklink <url>` / `!linkcheck <url>` | Scans a link with Check Link |
| `!wladd` / `!wlremove` / `!wllist` | Whitelisted Domains |
| `!amadd` / `!amremove` / `!amlist` | AutoMod Whitelist |
| `!euadd` / `!euremove` / `!eulist` | Excluded Users |
| `!egadd` / `!egremove` / `!eglist` | Excluded Groups |
| `!veuadd` / `!veuremove` / `!veulist` | Vote-Excluded Users |
| `!vegadd` / `!vegremove` / `!veglist` | Vote-Excluded Groups |
| `!kwadd` / `!kwremove` / `!kwlist` | Spam Keywords |
| `!tldadd` / `!tldremove` / `!tldlist` | Spaced-URL TLDs |
| `!permit @user [seconds]` | Grants a temporary link permit |
| `!endpermit [@user]` | Ends that viewer's permit, or all of them if no name is given |
| `!vote @user` | Starts/joins a vote-kick |

These are always recognized as commands (never scanned as regular chat) regardless of how they're wired up in Streamer.bot.

---

## 🌍 Language & Translations

**Q: Can I use TwitchSentry in my language?**

English, German, Spanish, French and Brazilian Portuguese all ship as translations. Open **Languages…** in the ☰ menu, pick one and click **Use This Language** — the window closes and reopens in it.

That dialog lists every published and installed language together, with a 🔔 against any that has a newer build available, and **Download** fetches or refreshes the one you have selected. English is a published translation like the rest rather than a special case: it is downloaded and version-checked on the same path, so a correction to the English wording actually reaches you.

It also sits *under* the other four. A lookup goes to your chosen language first, then to `en.json`, then to the text built into the window — so where a translation is incomplete you get the current English sentence rather than whichever one happened to be compiled in. A missing or broken `en.json` still leaves a working window, which is why English is the one language you can select without having its file.

---

**Q: I switched language but the bot still writes English in chat.**

That's working as intended. Translations cover the *settings window* — labels, tooltips, page names, dialogs. Everything TwitchSentry says in chat comes from the **Messages** pages, and those are yours to write: they're your wording, your tone, your language. Nothing translates them for you, because nothing should be putting words in your bot's mouth.

So to run a German channel, pick Deutsch for the window *and* write your chat messages in German on the Messages pages.

---

**Q: Where do the language files live, and how do they stay current?**

In `TwitchSentry/Settings/Language/`, one `<code>.json` per language. The 📁 button at the bottom left of the **Languages…** dialog opens the folder; drop a translation in there by hand and it appears in the list.

When you open the settings window, TwitchSentry checks GitHub for a newer copy of the language you're using, at most once every 15 minutes per language. `en.json` is fetched as well even when the window is not in English, because it is the layer under whichever language is. If GitHub is unreachable the window opens anyway, on the copy you already have.

---

**Q: Can I fix or write a translation myself?**

Yes. The files are flat JSON: each key is the exact English string from the window, each value is what gets shown instead.

```json
{
  "__languageName": "Nederlands",
  "__languageCode": "nl",
  "__version": 1,
  "Use Bot Account": "Botaccount gebruiken"
}
```

`__languageName` is what appears in the dropdown. Drop the file in the Language folder and it shows up in the list — no restart needed beyond reopening the window.

Two things to watch:

- **Keep the placeholders.** If the English text contains `{user}`, `{count}`, `{duration}` or similar, the translation has to contain them too, spelled the same way. They're filled in at runtime; a dropped one is a hole in the message.
- **Don't edit a shipped language in place.** `en`, `de`, `es`, `fr` and `pt-BR` are all refreshed from GitHub, so your changes there get overwritten on the next check — `en.json` included, now that English is published like the others. Save your version under a code that isn't published and it's left alone permanently. Better still, [open an issue](https://github.com/aaskjer/TwitchSentry/issues) so the fix reaches everyone.

---

## 🔄 Updates

**Q: How do I know if a new version is out?**

Every time you open the settings window, TwitchSentry checks GitHub's releases for you. If a newer one is out it appears as a line in the **notice strip** across the top, with a button that opens the releases page — it used to be a Yes/No box in front of the window, where answering "Yes" closed your settings outright. Now the window opens either way and the releases page is one optional click. Dismiss the notice with its **✕** if you would rather not be told again.

The update channel is `updateChannel` in `configs.json` — `stable` (the default) or `beta`, which notifies you about pre-releases too. It currently has no control in the settings window.

---

## 💾 Backup & Restore

**Q: What happens to my settings if a file gets corrupted?**

Nothing, if you have a backup. The **Backup & Restore** page under Help writes a dated copy of the
TwitchSentry folder wherever you point it, and copies it back on request.

Two things in there cannot be recreated: `configs.json` and `messages.json` (every setting in the
window, and every line TwitchSentry says in chat), and `spam.json` (the keywords, phrases and domain
endings the Spam Learner has built up from months of your own chat). Everything else — the language
files, the caches — re-downloads itself, and the logs are a record rather than a setting. Those first
two are ticked by default; tick all five and you have copied the whole folder.

**Q: Where should I put my backups?**

Somewhere that is not the disk TwitchSentry is on, if you have the option — a second drive, a USB
stick, or a folder your cloud storage syncs. Left empty, the *Backup Folder* box defaults to a
`Backups` folder inside TwitchSentry itself, which survives a bad file but not a bad disk.

**Q: Is a restore safe if I pick the wrong backup?**

It is undoable. A copy of the current state is put aside in the same backup folder before anything is
written, so the state you just replaced is still there. A restore also only touches what that backup
actually contains and never deletes anything — restoring a settings-only backup leaves your logs and
learned spam data alone — and a folder that holds no TwitchSentry files is refused rather than copied
over your install.

**Q: Can I just copy a file back by hand?**

Yes. A backup is a plain folder of ordinary files with the same layout as the TwitchSentry folder, not
an archive, so you can open it and drag one file back yourself. Streamer.bot re-reads the settings
when the file changes, so no restart is needed.

---

# Is TwitchSentry an AI Slop?

Partially, yes. This script was built with heavy AI assistance and input from the Streamer.bot community.

I'm not a developer in the classical sense, this project was my intention to improve my coding skills, learn how to handle AI and also make twitch a better place *cough*. 
In the beginning of this project (formerly known as TwitchLinkGuard) there wasn't much available in the streamer.bot community to battle scam in twitch chat, so i thought it would be a good start for me and i had and still have a ton of fun creating, prompting, breaking and fixing stuff and love to hear from you about things to make it better!
I do understand that there will be a lot of people hating the project or even me for using AI to create this slop work which probably kinda break anytime for no reason and is horrible written. I fully support their point of view, admire their handcrafted work and i will never act as i did everything by myself, as i'm probably never be able to. But AI won't vanish and AI gets better and in that matter, why not make a use of it. Of course, prompting something is easy peasy, but you still need to know where your goal is and how to fix things if necessary. TwitchLinkGuard, TwitchSentry and everything around it burned away a year or work, sitting on my ass for hours a day testing stuff. Maybe it's very inefficient and a real coder would do this in a couple weeks but again, i have fun doing it and all i can say is: Try it out, speak up if something's wrong and help me out making it better :)

Nonetheless, AI-assisted code can and does introduce bugs. Feel free to [open an issue](https://github.com/aaskjer/TwitchSentry/issues) — I'd rather hear about it than have it sit there quietly.
