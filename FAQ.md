# ❓ TwitchSentry — FAQ

---

## 🛠️ Setup & Configuration

**Q: Where are the config files stored?**

Everything lives under your Streamer.bot base directory, in a `TwitchSentry` folder:

```
TwitchSentry/Settings/configs.json               ← all module settings
TwitchSentry/Settings/messages.json               ← all chat/response messages
TwitchSentry/Settings/Language/<code>.json         ← settings-window translations
TwitchSentry/Machine Learning/spam.json            ← active keywords, phrases, patterns, TLDs
TwitchSentry/Machine Learning/spam-suggestions.json ← Spam Learner's pending suggestions
TwitchSentry/Logs/action-log.txt                   ← moderation action history
TwitchSentry/Logs/violation-log.txt                ← raw text the Spam Learner mines from
TwitchSentry/Logs/clean-log.txt                    ← sampled normal chat, used to avoid false positives
TwitchSentry/Cache/stopwords.txt                   ← downloaded common-word list
TwitchSentry/Cache/tld_cache.txt                    ← downloaded valid domain-ending list
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

**Q: Can a moderator command be deleted or flagged as a violation?**

No. TwitchSentry recognizes commands — both its own built-in ones and anything else you've configured in Streamer.bot — and skips them entirely before any scanning happens, so a command never reaches the Account Age check or any other filter.

**Q: How do I switch the whole Message Filter off?**

Untick its four checks: Account Check, Caps Check, Emote Check and Flood Check. There is no separate module switch — each check carries its own, and a second one sitting above them only made "the module is on but nothing happens" harder to work out.

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

Only *content* violations feed the learner — a message that matched a keyword, pattern or link rule. *Behavioral* violations (young account, caps spam, flooding) never contribute words, because the fact that someone typed too fast tells you nothing about which of their words are spam.

Several guards sit on top of that: a permanent **Ignore Terms** list, automatic protection for your broadcaster and bot account names, a "clean chat" sample the learner compares against so everyday words get suppressed, and a denylist that keeps major brand names (Google, YouTube, Twitch, Discord, etc.) from ever being suggested as blocked domain endings.

A word that slips past all of that is still only a *suggestion*. Reject it on the Suggestions tab, and add it to **Ignore Terms** so it can't come back.

**Q: What's the difference between "probation" and "trusted" status?**

A brand-new suggestion starts on **probation**. Once it's been seen across enough separate learner runs (see **Probation Runs Required**), it's upgraded to **trusted**. Trusted suggestions are the only ones eligible for automatic promotion into `spam.json` if Auto Promote is enabled — probation suggestions always need your manual review first.

**Q: How do I get rid of a bunch of bad/stale suggestions?**

Use the **Clear File** button on the Suggestions tab — it wipes every pending suggestion and starts fresh. It does **not** touch your active `spam.json` rules, only the pending list.

**Q: What is "Decay"?**

Automatic cleanup. When enabled, both active rules and pending suggestions are checked against recent chat history, and get removed if they've stopped showing up — keeps the rule list from accumulating dead weight from one-off spam campaigns. Entries you added by hand (prefixed with `!` in `spam.json`) are protected from decay by default.

---

## 🔗 Link Filter & Whitelist

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

Once a viewer racks up enough warnings (**Warn's Before Final Warning**), the *next* violation escalates straight to a timeout (or ban, if **Use Ban** is enabled) instead of another warning. Warning counts reset automatically after a configurable number of hours without a new violation.

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

Deletions, timeouts, bans, raid escalations, AutoMod holds, malicious/suspicious link scans, TwitchWarn actions, permit grants/revokes, config changes made via chat commands, and Spam Learner auto-applies — each toggled independently in **Discord Mod Notifications**.

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

English is built in, and German, Spanish, French and Brazilian Portuguese ship as translations. Pick one from the **Language** dropdown on the General tab and click **Save** — the window closes and reopens in the new language.

If your language isn't in the dropdown, click **Get More**. It fetches the published list from GitHub and downloads the one you pick.

---

**Q: I switched language but the bot still writes English in chat.**

That's working as intended. Translations cover the *settings window* — labels, tooltips, tab names, dialogs. Everything TwitchSentry says in chat comes from the **Messages** pages, and those are yours to write: they're your wording, your tone, your language. Nothing translates them for you, because nothing should be putting words in your bot's mouth.

So to run a German channel, pick Deutsch for the window *and* write your chat messages in German on the Messages pages.

---

**Q: Where do the language files live, and how do they stay current?**

In `TwitchSentry/Settings/Language/`, one `<code>.json` per language. The 📁 button next to the dropdown opens the folder.

When you open the settings window, TwitchSentry checks GitHub for a newer copy of the language you're using, at most once every six hours. If GitHub is unreachable the window opens anyway, on the copy you already have.

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
- **Don't edit a shipped language in place.** `de`, `es`, `fr` and `pt-BR` are refreshed from GitHub, so your changes there get overwritten on the next check. Save your version under a code that isn't published and it's left alone permanently. Better still, [open an issue](https://github.com/aaskjer/TwitchSentry/issues) so the fix reaches everyone.

---

## 🔄 Updates

**Q: How do I know if a new version is out?**

Every time you open the Settings GUI, TwitchSentry checks GitHub's releases for you and shows a banner if a newer version is available. Set your preferred **Update Channel** (Stable or Beta) in the General tab — Beta will notify you about pre-releases too, Stable won't.

---

# Is TwitchSentry an AI Slop?

Partially, yes. This script was built with heavy AI assistance and input from the Streamer.bot community. I'm not a developer in the classical sense, I used this project to actually learn how a real moderation tool comes together, and I put a lot of time and care into it. My goal was to build something robust and genuinely useful for other streamers, not just something that works *meehh*...
I understand that a lot of people (especially more technical folks) will look at TwitchSentry or my other projects and dismiss the project because of the AI involvement, and honestly, I get it. That's a fair position to hold.
AI-assisted code can and does introduce bugs. I've spent real time testing, breaking, and fixing this thing. If you run into something wrong, or just have feedback, please [open an issue](https://github.com/aaskjer/TwitchSentry/issues) — I'm always happy to get input :)
