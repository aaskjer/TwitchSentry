# 🛡️ TwitchSentry — Manual

Every page of the settings window, what each module decides, and why. If you are here to find out what TwitchSentry is or how to install it, start on the **[overview page](README.md)**.

**[Overview](https://github.com/aaskjer/TwitchSentry/tree/main)** · **[FAQ](FAQ.md)** · **[Changelog](CHANGELOG.md)** · **[Report a problem](https://github.com/aaskjer/TwitchSentry/issues)**

Everything is configured from one window. There is no config file you are expected to edit by hand (well, you can if you want) and nothing to sign up for beyond the two link-scanning services, which are optional and free.

---

## Features

| | |
|---|---|
| **[Link Filter](#general-settings)** | Blocks links from viewers you have not trusted, with a whitelist that matches exactly or by wildcard. Always on. |
| **[Spam Scoring](#spam-scoring)** | Reads a message as an advert with parts — somewhere to go, something on offer, a way to redeem it, a signature — and acts when enough parts fit together. Always on. |
| **[Message Filter](#message-filter)** | Watches *how* someone chats: account age, ALL CAPS, emote spam, flooding and repeats. |
| **[Raid Protection](#raid-protection)** | Arms itself after an incoming raid and watches for a swarm of accounts posting the same line. |
| **[Follow Protection](#follow-protection)** | Watches follows. It counts how many different accounts arrive inside a short window and judges each on age, avatar, profile and login. |
| **[Spam Learner](#spam-learner)** | Mines what was actually removed for new keywords, phrases and domain endings, and proposes them for review. |
| **[AutoMod](#automod)** | Answers the messages Twitch's own AutoMod holds back, so nobody has to sit in the queue. |
| **[Twitch Warn](#twitch-warn)** | Twitch's warning screen, with escalation steps on top of it — a three-strikes rule, if you want one. |
| **[Permits](#permits)** | A time-limited link exception for one viewer, granted by you, a moderator, or a Channel Points redeem. |
| **[Check Link](#check-link)** | Scans a URL with VirusTotal and IPQualityScore, either automatically or on `!checklink`. |
| **[Voting](#voting)** | Lets chat vote someone out, with roles above VIP permanently unvotable. |
| **[Discord Alerts](#discord-alerts)** | Posts what happened to a webhook, one toggle per kind of action. |

---

# Import

<p align="center"><img alt="The Streamer.bot toolbar, with the Import button highlighted" src="https://github.com/user-attachments/assets/7db12d06-c0ee-42a2-a35a-996566f20b3c" /></p>

<p align="center"><img alt="The import dialog, with the TwitchSentry.sb file dragged into it" src="https://github.com/user-attachments/assets/b91f4bf4-2aa3-4730-8991-85c3eddd14b9" /></p>

Open your copy of Streamer.bot, click **Import**, and drag the `TwitchSentry.sb` file into the window that opens, like in the screenshot above. Answer **Yes / OK** to the prompts that follow to finish the import.

<p align="center"><img alt="The Commands tab in Streamer.bot with every TwitchSentry command ticked" src="https://github.com/user-attachments/assets/c3ba2442-a260-4f72-9dcc-22da02b30792" /></p>

Then enable all the commands under **Commands**, as in the picture.

---

# First run

<p align="center"><img alt="Right-clicking the Test sub-action of the TS - Settings action and choosing Test Trigger" src="https://github.com/user-attachments/assets/f1ef63e3-c5da-4e9e-a94f-e79a32a70ec2" /></p>

Go to the `[TS] - Settings` action, right-click **Test** and choose **Test Trigger**. That opens the settings window. *(The first start takes a moment — it fetches the language files.)*

The defaults are meant to be a working configuration, not a starting point you have to tune. If you change nothing at all, TwitchSentry filters links and spam and leaves everything else off.

---

# The settings window

| Dark Mode | White Mode |
|:---:|:---:|
| ![before](https://github.com/user-attachments/assets/145de2d6-7c56-4049-ade8-86db1469af9b) | ![after](https://github.com/user-attachments/assets/0f260b75-9a63-461e-8509-cb65a171ac40) |

Pages are grouped down the left: **Setup**, **Filters**, **Spam**, **Modules**, **Messages**, **Results** and **Help**. Click a group heading to collapse it.

**A few things worth knowing before you start:**
- **The search box** at the top left filters the page list by page name, setting label, or the internal setting key. `Ctrl+F` focuses it, `Esc` clears it. If you know roughly what a setting is called, this is faster than hunting for the page.
- **The ☰ menu**, in front of the search box, holds the things you reach for occasionally: the light/dark theme, expert mode, the language files, test mode, and both reset buttons.
- **The notice strip** across the top carries anything the window needs to tell you — an available update, a translation that is behind, a setting that will not do what it looks like it does. Notices stack, and the **✕** on one hides it for good. If you want them back, *Show hidden notices again* in the ☰ menu clears the list.
- **Nothing is saved until you press Save.** The bottom left says whether you have unsaved changes.

<img width="917" height="127" alt="grafik" src="https://github.com/user-attachments/assets/97fecd24-a799-4321-b976-8b043f2c78d1" />

### Test mode

Switched on from the ☰ menu. While it runs, nothing is deleted, timed out or banned — every module posts what it *would* have done instead, so you can point a real chat at your settings without anybody being punished for helping you test them. Not even the chat modes come on. It ends on its own after the time set on General Settings, five minutes by default, and the notice strip counts it down — so a chat can never be left unguarded because somebody forgot to switch it back.

### Easy & Expert mode

| Easy Mode | Expert Mode |
|:---:|:---:|
| ![before](https://github.com/user-attachments/assets/7049f482-589d-4fb1-bfd7-ff519465b270) | ![after](https://github.com/user-attachments/assets/191d4a2b-8d23-472a-b48b-684557acaee8) |

`Easy Mode` is active by default, intended for users new to TwitchSentry or this type of system at all. Simplified settings with a **sensitivity slider** to choose — `Very relaxed` through `Very strict`, with a line under it saying what the step actually means and does. 
Also in the ☰ menu. Expert mode reveals the individual numbers the slider is moving for you. In expert mode `Custom` gives you the possibility to create your own slider sensitivity and is remembered by the GUI if you move away from it, as long as you have hit `save` once.

---

# Setup

## General Settings

<img width="926" height="1338" alt="grafik" src="https://github.com/user-attachments/assets/36c548e0-e1da-4a5a-b6df-03cc9cc9e762" />

Behaviour shared by every module: whether to speak through your bot account, whether to reply in chat, whether to write the action log. Then **test mode**'s duration and wording, and the **exemptions** — followers, subscribers, VIPs, named viewers and Streamer.bot groups — which apply to the six modules that take action on a message. **Whitelisted Domains** lives here too.

A whitelist entry without a trailing `/*` is an exact match: `twitch.tv/yourname` allows that one link and nothing nested under it, so your own clip links still need `twitch.tv/yourname/*`.

## Discord Alerts

<img width="926" height="1338" alt="grafik" src="https://github.com/user-attachments/assets/2109d718-4066-446f-b054-35899892c0c5" />

Off by default, a discord webhook and one toggle per kind of action. A pasted webhook automatically gets hidden with `***` to prevent leaking critical information accidentally.

Example:
<img width="317" height="263" alt="grafik" src="https://github.com/user-attachments/assets/2d3d313d-d106-4bd5-a0ed-72f8df862509" />

**Create a discord webhook:**
* Right-Click on desired channel
* Edit Channel
* Create WebHook
* Give your webhook a fancy name and a logo
* Copy WebHook URL

---

# Filters

## Message Filter

| Easy Mode | Expert Mode |
|:---:|:---:|
| ![before](https://github.com/user-attachments/assets/7ede45ce-3592-4b99-b8e5-34bdf6e7fb96) | ![after](https://github.com/user-attachments/assets/9e7a3794-e89a-4857-8fc9-0bd937d737d0) |


Looks at how someone is chatting rather than at particular words: account age, ALL CAPS, emote spam, and posting too fast or repeating yourself.

No single one of those is proof of anything on its own — people shout, people spam emotes when something good happens — so a message is only acted on when at least two of them show up together, or when one of them is the kind that is not an accident. A repeated message is decisive on its own; being new to Twitch is a risk factor that makes whatever else the message tripped count for more, never a finding by itself. Someone with a long history in your chat needs more evidence than a stranger does.

Each of the four checks has its own switch and there is no module-wide one: unticking every check is what silences it.

**Escalation** sits on top of that and deals with the whole chat rather than one viewer. When enough *different* people trip the filters inside the same window, a Twitch chat mode is switched on for everyone and lifted again on its own. Which mode gets picked depends on what the wave looks like — and the table at the bottom of the page shows exactly what would happen with the boxes as you have them ticked right now, renumbering as you tick and striking through a mode you have switched off.

## Raid Protection

| Easy Mode | Expert Mode |
|:---:|:---:|
| ![before](https://github.com/user-attachments/assets/cd0c401f-449a-4ba2-8159-ab28e8637413) | ![after](https://github.com/user-attachments/assets/71fd4478-f69c-4bef-8d7b-95de3eb71767) |

The same idea as `Message Filter` but stricter and only armed for a limited window right after an incoming raid. Plus: **swarm detection**, which spots several different accounts posting near-identical messages at once which then gets scored against bot patterns.
It has its own escalation ladder and its own progressive escalation, so a second wave of the same pattern moves up a step instead of re-picking the mode that is already running.

## Follow Protection

| Easy Mode | Expert Mode |
|:---:|:---:|
| ![before](https://github.com/user-attachments/assets/30f7d996-0a13-4ee5-8512-018fab96659f) | ![after](https://github.com/user-attachments/assets/42270f7e-f998-45cb-a358-245a46ac277d) |

**Off by default**. It counts how many **different** accounts arrive inside **Window (Seconds)**, and
only once **Accounts Needed** is crossed, it looks them up and compares their account data against your settings, if there's a match, the accounts get blocked, which removes their follow and blocks them from any further action on your channel.

- Each account in the wave is judged on four things from that one lookup: **Young Account**, **Default
Avatar**, **Empty Profile** and **Throwaway Name**. 
- **Age gates the two cosmetic checks.** An account three years old with no picture and no bio is not a bot, it
is somebody who never filled the form in. 
- **It blocks rather than bans** A ban leaves the follower on your list while a block removes the follow and stops that account following again.
- **Report Only is default**, because a block is invisible from the viewer's side: they simply cannot follow,
and nobody tells them why. Every account it blocks is written to **Blocked Accounts** on the page with the
evidence that convicted it beside it, and [`!tsundo`](#chat-commands) lifts the last one.
- Off by Default: **Judge Single Follows Too** runs the checks on every follow rather than only inside a wave.

---

# Spam

## Spam Scoring

| Easy Mode | Expert Mode |
|:---:|:---:|
| ![before](https://github.com/user-attachments/assets/7049f482-589d-4fb1-bfd7-ff519465b270) | ![after](https://github.com/user-attachments/assets/191d4a2b-8d23-472a-b48b-684557acaee8) |

This does not judge a message by how many red flags it trips. It asks whether the message is built like an advert. An advert has parts: somewhere to go (**Destination**), something being sold (**Offer**), a way to redeem it (**Instrument**), the random `@handle` a spam bot signs with (**Tag**), and wording this channel has seen from spam before (**Signature**).

One part on its own is a coincidence — plenty of ordinary messages have one. Two parts together is an advert. That is what the sensitivity slider controls, and why false positives are rare: no single keyword is ever the whole verdict.

**Conversation Scam** is tracked separately, because it is a different animal from the bot that drops one advert and leaves. This account chats with you: it asks how long you have been streaming, says your channel looks a little empty, mentions that a logo or a VTuber model would fix that, and only then tells you it sells exactly that. No single message it sends is spam — the tell is the order. Four stages are tracked per account inside a window, they only count moving forwards, and it only acts once an account has walked them in order and ended on the offer. Being a familiar face does not buy an exemption here — it raises the bar to all four stages instead of three. Sitting in a channel for hours is how these accounts earn their standing in the first place.

## Known Patterns

<img width="926" height="1333" alt="grafik" src="https://github.com/user-attachments/assets/785e5ec5-cb02-4a75-beb5-1b4b11ba7bab" />

The actual active rules every module checks against — `spam.json`, editable in place. Spam domains, keywords, strong keywords, domain endings, custom patterns and voucher-code patterns, plus the four **conversation beats** the scam detector matches on. Add your own here, or approve what the Learner suggests. Don't forget **Save**.

## Spam Learner

<img width="926" height="1333" alt="grafik" src="https://github.com/user-attachments/assets/9a976adb-ba5c-4e33-a036-a417caa58e20" />

Watches what actually got removed and works out which words, phrases and domain endings keep showing up in it, scoring each candidate by how much more often it appears in spam than in ordinary chat. New finds start as suggestions for you to review; they are promoted into the real rule list only once they have built a track record — either because you approve them, or automatically if **Auto Promote Trusted Rules** is on.

Only *content* violations feed it. The fact that somebody typed too fast tells you nothing about which of their words were spam, so behavioural violations contribute none. On top of that sit an **Ignore Terms** list, automatic protection for your own account names, a denylist for major brands, and the clean-chat sample described below.

## Suggestions

<img width="926" height="1333" alt="grafik" src="https://github.com/user-attachments/assets/0cd9d832-f33b-4b3c-a75f-675992d31e27" />

Everything the Learner has proposed but not applied. Read the **Would hit** column first: that is how many messages from your own clean chat log the rule would have matched. Zero is what you want, and anything above zero is never auto-promoted. **Users** counts how many different people posted it, so one spammer repeating himself counts once; **Discrim.** is how much more often it shows up in spam than in ordinary chat.

**Probation** means a candidate is still building a record; **trusted** means it is proven enough to be auto-promoted, if you have turned that on. **Clear File** wipes the pending list and leaves your active rules alone.

---

# Modules

These are off by default. Each is genuinely optional — the two filters above are the core, and everything here is something you may or may not want.

## AutoMod

<img width="926" height="1333" alt="grafik" src="https://github.com/user-attachments/assets/f13b985d-4cd8-4bba-abf4-d2c319358efa" />

**Off by default**. Twitch's own AutoMod holds suspicious messages back and waits for a moderator to approve or deny each one. This answers them for you, by level and by category. Leave **AutoMod Categories** empty to act on everything Twitch holds, or list only the categories you care about.

## Twitch Warn

<img width="926" height="1333" alt="grafik" src="https://github.com/user-attachments/assets/ec4ca9cb-37c2-4752-aece-f7c07c96714c" />

A warned viewer has to read and click through a warning screen before they can chat again, and Twitch keeps the count in their moderation history. This adds escalation on top: warns accumulate, the last one before the threshold is a final warning, and the violation after that becomes a timeout or a ban. Counts reset on their own after a quiet period.

## Permits

<img width="926" height="1333" alt="grafik" src="https://github.com/user-attachments/assets/b7a3e22f-64da-42b5-b763-8c2a5b6bb0ae" />

A time-limited exception for a viewer, so they can post a link without it getting deleted. `!permit @user [seconds]` grants one, `!endpermit @user` ends it, `!endpermit` on its own ends every active permit. Several people can hold one at the same time, each with its own countdown; a permit that is already running is never extended. They are deliberately forgotten on restart.
**Max Permit Duration Seconds** caps whatever a moderator types, with a hard ceiling of 24 hours.
Viewers can also redeem a permit themselves through Channel Points, if **Allow Self-Permit** is on. Set that reward up with **Skip Reward Requests Queue** turned **off** — that is what lets TwitchSentry give the points back when a redemption cannot become a permit. A reward that skips the queue is spent the moment it is redeemed, and Twitch will not allow a refund.

## Check Link

<img width="926" height="1333" alt="grafik" src="https://github.com/user-attachments/assets/a3aaf79f-b219-4e4e-8db8-02b600d94add" />

Two jobs: Anyone can scan a URL on demand with `!checklink <url>`. The second feature adds a scan on top of the ordinary link rule and automatically scans any incoming link in chat.
Uses VirusTotal (required, free key) and optionally IPQualityScore for a second opinion. IPQS rates a link from 0 to 100; the default threshold is 75, with a stricter one for domains it also reports as recently registered, since a brand-new throwaway domain is a phishing classic.

## Voting

<img width="926" height="1333" alt="grafik" src="https://github.com/user-attachments/assets/307b5166-6c2a-4559-a59b-30bc88a7e27c" />

Lets chat decide! `!vote @user` starts or joins a vote, and enough *unique* voters inside the time window time that person out — or ban them, if you allow it. The window running out resets the vote. Subscribers and VIPs can be exempted, there are separate exclusion lists for users and Streamer.bot groups, and **everyone above VIP is permanently unvotable!**

---

# Messages

Everything TwitchSentry says in chat, one page per module, with the placeholders each message accepts listed under the box. Nothing here is translated for you — this is your bot's voice, your wording and your language, so a German channel picks Deutsch for the window *and* writes these in German.

| Command Replies | Filter Messages | Raid Messages | 
|:---:|:---:|:---:| 
| ![](https://github.com/user-attachments/assets/adfdfec4-7626-49db-9517-1468b6c971e1) | ![](https://github.com/user-attachments/assets/02120ab7-6865-48b2-93d1-70147a4b8ae2) | ![](https://github.com/user-attachments/assets/973b7c80-439b-4947-a5a5-9b1909799c9e) |
| Link Messages | Spam Messages | Learner Messages | 
| ![](https://github.com/user-attachments/assets/f2ccfe16-d849-4d03-a419-add6b06907ff) | ![](https://github.com/user-attachments/assets/ad216565-373d-4adf-8e29-5ff556bff987) | ![](https://github.com/user-attachments/assets/9c166a34-4634-4686-bc39-4e041e984b21) |
| AutoMod Messages | Warn Messages | Permit Messages | 
| ![](https://github.com/user-attachments/assets/44860855-2b46-4887-9a34-2d0a109925a8) | ![](https://github.com/user-attachments/assets/2d322a8f-0d28-4081-a186-2967142d01a4) | ![](https://github.com/user-attachments/assets/ea04a837-fcab-4179-b3dd-3f3eb0f8578c) |
| Scan Messages | Vote Messages | | 
| ![](https://github.com/user-attachments/assets/4327a6e1-998e-42e4-b8c1-dd393a0eda74) | ![](https://github.com/user-attachments/assets/485128ad-89b6-4773-8597-5eba7699d969) | |

---

# Results

## Action Log

<img width="926" height="1333" alt="grafik" src="https://github.com/user-attachments/assets/ac156268-a225-4e2a-8706-89f3409821d2" />

Every action involving a viewer, filterable by module and by result, with the raw line underneath. This is the page for *what happened*.

## Status Log

<img width="926" height="1333" alt="grafik" src="https://github.com/user-attachments/assets/a7e7cbe3-d65e-4cfd-a645-ca84ad38c569" />

What TwitchSentry has been saying about *itself*, pulled out of the Streamer.bot log: an API key still on its placeholder, a download that failed, an action Twitch refused. None of that is announced in chat, so this is the page to open when something quietly did not happen.

## Violation Log

<img width="926" height="1333" alt="grafik" src="https://github.com/user-attachments/assets/4f9ea565-f62a-471f-b474-5ca79750545d" />

The **Violation Log** is every message that was acted on, exactly as it was posted — the page to open when you disagree with a removal.

## Clean Chat Log

<img width="926" height="1333" alt="grafik" src="https://github.com/user-attachments/assets/60fca65f-dd01-4191-8057-d0dfbb481e47" />

The **Clean Chat Log** is the opposite of the violation log: a sample of ordinary chat that was deliberately left alone, roughly one message in ten. The Spam Learner measures its candidates against it, which is what stops an everyday word from becoming a rule. Both pages have a search box and a per-account filter, and both show the full line under the list, because chat messages are usually wider than the row.

---

# Help

## Backup & Restore

<img width="926" height="1333" alt="grafik" src="https://github.com/user-attachments/assets/d029a1b3-b4e9-4df1-a505-b0cb5ccdff87" />

Everything TwitchSentry knows about your channel is a handful of files in one folder, and two of those
files are things nothing can give back: your settings and the replies you have written, and the
keywords, phrases and domain endings the Spam Learner has built up from months of your own chat.

**Backing up** writes a dated folder of ordinary files. Tick what goes in: settings and chat messages,
learned spam data, language files, logs, cache. The first two are the parts nothing can give back, and
are ticked by default; all five ticked is the whole TwitchSentry folder, a few hundred kilobytes unless
you keep long logs. *Backup Folder* is where they go — leave it empty and they land in a `Backups` folder inside
TwitchSentry itself, which is better than nothing but shares a disk with the thing it is protecting,
so point it at a second drive or a synced folder if you have one. Pressing **Back Up Now** saves your
settings first, so the copy is never taken around edits you have not committed.

**Restoring** asks for a backup folder and copies its files back over the ones in use. Only the parts
that backup actually contains are touched and nothing is ever deleted — a settings-only backup leaves
your logs and your learned spam data exactly where they are. A copy of the current state is put aside
first, in the same backup folder, so a restore you did not mean is itself undoable, and the settings
window reopens afterwards showing what was restored. A folder that is not a TwitchSentry backup is
refused rather than copied.

Because a backup is a plain folder, you can also open it, read it, and copy a single file back by
hand — there is no archive to unpack.

---

# Chat commands

Moderator-only unless noted, and always recognised as commands — a command is never scanned as ordinary chat.

| Command | Manages |
|---|---|
| `!checklink <url>` / `!linkcheck <url>` | Scans a link with Check Link *(anyone)* |
| `!permit @user [seconds]` | Grants a temporary link permit |
| `!endpermit [@user]` | Ends that viewer's permit, or all of them |
| `!vote @user` | Starts or joins a vote *(anyone)* |
| `!wladd` / `!wlremove` / `!wllist` | Whitelisted Domains |
| `!amadd` / `!amremove` / `!amlist` | AutoMod Whitelist |
| `!euadd` / `!euremove` / `!eulist` | Excluded Users |
| `!egadd` / `!egremove` / `!eglist` | Excluded Groups |
| `!veuadd` / `!veuremove` / `!veulist` | Vote-Excluded Users |
| `!vegadd` / `!vegremove` / `!veglist` | Vote-Excluded Groups |
| `!kwadd` / `!kwremove` / `!kwlist` | Spam Keywords |
| `!tldadd` / `!tldremove` / `!tldlist` | Spaced-URL TLDs |
| `!tsundo` | Undo the last action (ban/timeout/etc) |

---

# Languages

<img width="446" height="423" alt="grafik" src="https://github.com/user-attachments/assets/3a1517f6-9406-4118-b5a9-893ca1da3f7c" />

The settings window ships in English, German, Spanish, French and Brazilian Portuguese. Pick one from the ☰ menu; the window closes and reopens in it. Files are refreshed from GitHub in the background, and the window opens on the copy you already have if GitHub is unreachable.

This covers the window only. What the bot says in chat comes from the **Messages** pages and stays exactly as you wrote it.

Writing a translation is a matter of copying `Language/en.json` and replacing the values — each key is the exact English string from the window. Keep any `{user}`, `{count}` or `{duration}` placeholders spelled the same way. Save it under a code that is not published and it will never be overwritten; better still, [open an issue](https://github.com/aaskjer/TwitchSentry/issues) so the fix reaches everyone.

---

# Where the files live

Everything sits under your Streamer.bot base directory, in a `TwitchSentry` folder. You should never need to edit any of it by hand.

```
TwitchSentry/Settings/configs.json                   ← all module settings
TwitchSentry/Settings/messages.json                  ← everything the bot says in chat
TwitchSentry/Settings/Language/<code>.json           ← settings-window translations
TwitchSentry/Machine Learning/spam.json              ← active keywords, phrases, patterns, TLDs
TwitchSentry/Machine Learning/spam-suggestions.json  ← the Learner's pending suggestions
TwitchSentry/Logs/action-log.txt                     ← moderation action history
TwitchSentry/Logs/violation-log.txt                  ← raw text the Learner mines from
TwitchSentry/Logs/clean-log.txt                      ← sampled normal chat
TwitchSentry/Cache/stopwords.txt                     ← downloaded common-word list
TwitchSentry/Cache/tld_cache.txt                     ← downloaded valid domain-ending list
```

Settings are re-read whenever the file changes, so **Save** is enough — no Streamer.bot restart.

---

Questions are answered in more depth in the **[FAQ](https://github.com/aaskjer/TwitchSentry/blob/main/FAQ.md)**, and anything that looks wrong is worth an **[issue](https://github.com/aaskjer/TwitchSentry/issues)**.
