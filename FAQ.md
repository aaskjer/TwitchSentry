# ❓ TwitchSentry — FAQ

---

## 🛠️ Setup & Configuration

**Q: Where are the config files stored?**

Everything lives under your Streamer.bot base directory, in a `TwitchSentry` folder:

```
TwitchSentry/Settings/configs.json                   ← all module settings
TwitchSentry/Settings/messages.json                  ← all chat/response messages
TwitchSentry/Machine Learning/spam.json              ← active keywords, phrases, patterns, TLDs 
TwitchSentry/Machine Learning/spam-suggestions.json  ← Spam Learner's pending suggestions
TwitchSentry/Logs/action-log.txt                     ← moderation action history
TwitchSentry/Logs/violation-log.txt                  ← raw text the Spam Learner mines from
TwitchSentry/Logs/clean-log.txt                      ← sampled normal chat, used to avoid false positives
TwitchSentry/Cache/stopwords.txt                     ← downloaded common-word list
TwitchSentry/Cache/tld_cache.txt                     ← downloaded valid domain-ending list
```

You should never need to edit these by hand — use the built-in Settings GUI instead.

---

**Q: I saved settings but nothing changed. Why?**

Settings are re-read from disk automatically whenever the file's been updated — no Streamer.bot restart needed. Just click **Save** (or **Save & Exit**) and the next chat message will already use the new config.

---

**Q: How do I reset everything to defaults?**

Open the Settings GUI and click **Reset to Defaults** (red button, bottom-left). It asks for confirmation, then rewrites both `configs.json` and `messages.json` with factory defaults and reopens the GUI. This cannot be undone.

---

**Q: The Settings GUI won't open or throws an error. What do I do?**

Check the Streamer.bot log for the actual error — TwitchSentry logs failures with a `[TwitchSentry/...]` prefix. If it's a malformed `configs.json`/`messages.json`, the simplest fix is deleting the broken file so a fresh default gets written. If it keeps happening, please report it [here](https://github.com/aaskjer/TwitchSentry/issues).

---

## 💬 Message Filter (Chat Guard)

**Q: What does Message Filter actually check?**

It looks at *how* someone is chatting, not specific words: account age, ALL CAPS / repeated-character spam, emote spam, and posting too fast or repeating the same message. Every check that trips adds a bit to a shared score for that message — action is taken once the total score crosses your configured threshold, so a couple of small red flags together can be enough even if none of them alone would be.

**Q: What is "Escalation"?**

A chat-wide safety net layered on top of the per-user checks above. If enough *different* users trigger violations within a short window (a spam wave, not one annoying person), TwitchSentry automatically activates a Twitch chat mode (slow mode, follower-only, emote-only, or sub-only) to protect the whole chat, then lifts it automatically once things calm down. Which mode gets picked depends on the dominant spam pattern detected (e.g. an emote-spam wave prefers slow mode; a wave of brand-new accounts prefers follower-only).

---

## 🚫 Spam Filter

**Q: What kinds of spam does it catch?**

Keyword matches, custom patterns (flexible text matching for things a plain word list can't catch), spaced-out/disguised links (`twitch. tv`), fancy lookalike-Unicode obfuscation, excessive @mentions (especially to nonexistent accounts), and gift/voucher-code-shaped strings. Each of these is its own scoring signal that adds to one total — see **Score Settings** in the GUI to tune how much each one is worth.

**Q: Can I add my own detection patterns?**

Yes — the **Known Patterns** tab lets you add custom keywords, custom patterns, and voucher-code patterns directly, on top of whatever the Spam Learner suggests.

---

## 🧠 Spam Learner

**Q: What does the Spam Learner do?**

It watches messages that actually get deleted/timed-out/banned and tries to spot new spam keywords, phrases, and domain endings automatically. New finds start as pending suggestions (Suggestions tab) for you to review, and only get promoted to the real, active rule list (`spam.json`) once they've built up enough of a track record — either you approve them yourself, or the learner promotes them automatically if **Auto Promote Trusted Rules** is turned on.

**Q: The Spam Learner suggested a totally normal word (like "google"). Why?**

In older versions, behavior flags don't tell you anything about which words are spam, so unrelated words could slip through. That's fixed now: only genuine content matches feed the learner. On top of that, there's now a permanent **Ignore Terms** list, automatic protection for your broadcaster/bot account names, a "clean chat" sample the learner compares against to avoid flagging everyday words, and a denylist so major brand names (Google, YouTube, Twitch, Discord, etc.) can never be suggested as blocked domain endings.

**Q: What's the difference between "probation" and "trusted" status?**

A brand-new suggestion starts on **probation**. Once it's been seen across enough separate learner runs (see **Probation Runs Required**), it's upgraded to **trusted**. Trusted suggestions are the only ones eligible for automatic promotion into `spam.json` if Auto Promote is enabled — probation suggestions always need your manual review first.

**Q: How do I get rid of a bunch of bad/stale suggestions?**

Use the **Clear File** button on the Suggestions tab — it wipes every pending suggestion and starts fresh. It does **not** touch your active `spam.json` rules, only the pending list.

**Q: What is "Decay"?**

Automatic cleanup. When enabled, both active rules and pending suggestions are checked against recent chat history, and get removed if they've stopped showing up — keeps the rule list from accumulating dead weight from one-off spam campaigns. Entries you added by hand (prefixed with `!` in `spam.json`) are protected from decay by default.

---

## 🔗 Link Filter & Whitelist

**Q: How does the whitelist actually match URLs?**

Three patterns, each behaving differently:

| Entry | Matches |
|---|---|
| `youtube.com` | That exact address only — nothing after it |
| `youtube.com/*` | Anything after `youtube.com/` |
| `*.youtube.com/*` | Any subdomain (e.g. `music.youtube.com`) plus anything after it, but **not** bare `youtube.com` |
| `twitch.tv/aaskjer` | That exact channel link only, nothing after it |

An entry without a trailing `/*` is always an **exact match** — it will not accidentally allow sub-pages, clip links, or anything else nested under it.

**Q: My own channel/clip link got blocked even though I whitelisted my channel. What's going on?**

Make sure your whitelist entry ends in `/*` if you want clip/sub-page links to be covered too (e.g. `twitch.tv/yourname/*`), since a bare `twitch.tv/yourname` entry only matches that exact link.

**Q: What happens to a link that isn't whitelisted?**

It's scored and, depending on your configured action, deleted/timed-out/banned. If **Check Harmful Domains** is enabled, it's also scanned in the background (even for trusted roles) via the Check Link module, purely as a safety check.

---

## 🚨 Raid Protection

**Q: How is this different from Message Filter's normal flood checks?**

It's a stricter, temporary version of the same idea that only arms itself for a limited window right after an incoming raid, and adds **swarm detection** — spotting multiple different accounts posting near-identical messages at once, the signature of a bot raid rather than real viewers.

**Q: What determines which chat mode gets activated during a raid?**

The dominant spam pattern detected during the wave: emote spam prefers slow mode, waves of fresh/throwaway accounts prefer follower-only (locks out accounts that just followed), and caps/character spam prefers emote-only (makes text spam impossible). Only modes you've enabled are eligible — if your preferred mode is off, it falls through to the next one in the preference order.

---

## 👾 Twitch AutoMod Integration

**Q: What does this module actually do?**

Twitch's own built-in AutoMod holds back messages it thinks might be harmful and normally waits for a moderator to manually approve or deny each one. This module lets TwitchSentry make that call automatically instead, based on the AutoMod level and categories you configure.

**Q: Can I limit it to specific categories instead of everything AutoMod flags?**

Yes — the **AutoMod Categories** setting lets you list exactly which categories to act on (Profanity, Racism, SmartDetection, etc.). Leave it empty to act on everything AutoMod holds.

---

## 🕵️ Check Link (Malicious Link Scanning)

**Q: What services does it use to scan links?**

VirusTotal (required — free API key) and, optionally, IPQualityScore (IPQS) for a second opinion, especially good at catching brand-new/throwaway phishing domains. Great if a new user comes in and want you to click on a sketchy link. Run it first through `Check Link` to be safe!

**Q: How is the IPQS fraud score threshold chosen?**

IPQS rates every link from 0 (safe) to 100 (certainly malicious). The default threshold is 75, matching IPQS's own "flag for review" guidance (they recommend 85 to outright block). There's a separate, stricter threshold (default 40) that only applies to domains IPQS also flags as *recently registered* — brand-new throwaway domains are a classic phishing tactic, so they're held to a lower bar.

---

## ⚠️ Twitch Warn & Escalation

**Q: What is "Twitch Warn"?**

Twitch's own built-in warning system — the flagged viewer has to read and click through a warning screen before they can chat again. It's a step below a timeout: firm, but it doesn't remove them from chat entirely.

**Q: How does escalation to a timeout/ban work?**

Once a viewer racks up enough warnings (*Like a 3-Strikes Rule*), the *next* violation escalates straight to a timeout (or ban, if **Use Ban** is enabled) instead of another warning. Warning counts reset automatically after a configurable number of hours without a new violation.

---

## 🔓 Permits

**Q: What's a permit?**

A temporary, per-user exception that lets someone post a link even while Link Filter would normally block it — useful for letting a specific viewer share something once without changing your whitelist.

**Q: Can viewers grant themselves a permit?**

Yes, if **Allow Self-Permit** is enabled — viewers can redeem a Channel Points reward to grant themselves a one-time, temporary permit without needing a moderator.

---

## 🗳️ Voting

**Q: How does vote-kick work?**

Viewers vote against someone breaking chat rules (e.g. `!vote @username`). Once enough unique votes are cast within the time window, that user is automatically timed out (or banned, if **Allow Ban** is enabled). If the window runs out before enough votes come in, the vote resets.

**Q: Can specific users be protected from being voted against?**

Yes — subscribers and VIPs can be excluded globally, and you can add specific usernames or Streamer.bot groups to the exclusion lists.

---

## 🔔 Discord Webhook Alerts

**Q: What can it send alerts for?**

Deletions, timeouts, bans, raid escalations, AutoMod holds, malicious/suspicious link scans, TwitchWarn actions, permit grants/revokes, config changes made via chat commands, and Spam Learner auto-applies — each toggled independently in **Discord Mod Notifications**.

**Q: Can i chose the channel where the notifications get send?**

Yes — enter the webhook of your preferred channel in the settings. Also works great for a *Shame Channel* to make bans/timeouts/etc. public

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
| `!vote @user` | Starts/joins a vote-kick |

These are always recognized as commands (never scanned as regular chat) regardless of how they're wired up in Streamer.bot.

---


## 🔔 Update Notifications

**Q: How do I know when a new version is available?**

Opening the Settings GUI checks GitHub for the latest release tag. If it's newer than what's installed, a popup offers to open the releases page.

**Q: Can I check for updates without opening the Settings window?**

Partially — You still have to trigger the `Test` trigger but if you press `Yes` in the update notification popup, the check won't open the GUI but the GitHub page instead. Running Beta will notify you about pre-releases too, Stable won't.

---

# Is TwitchSentry an AI Slop?

Partially, yes. This script was built with heavy AI assistance and input from the Streamer.bot community. I'm not a developer in the classical sense, I used this project to actually learn how a real moderation tool comes together, and I put a lot of time and care into it. My goal was to build something robust and genuinely useful for other streamers, not just some half-ass bullshit. The Project learned me a lot and i still have fun maintaining it. I understand that a lot of people, especially more technical skilled people, will look at that and dismiss the project because of the AI involvement, and honestly, I get it. That's a fair and i respect and support it.
AI-assisted code can and does introduce bugs. I've spent real time testing, breaking, and fixing this thing. If you run into something wrong, or just have feedback, please [open an issue](https://github.com/aaskjer/TwitchSentry/issues) — I'd rather hear about it than have it sit there quietly.
