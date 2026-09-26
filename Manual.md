# 🛡️ TwitchSentry — Manual

Every page of the settings window, what each module decides, and why. If you are here to find out what TwitchSentry is or how to install it, start on the **[overview page](README.md)**.

**[Overview](https://github.com/aaskjer/TwitchSentry/tree/main)** · **[FAQ](FAQ.md)** · **[Changelog](https://github.com/aaskjer/TwitchSentry/releases)** · **[Report a problem](https://github.com/aaskjer/TwitchSentry/issues)**

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
| **[Twitch Warn](#twitch-warn)** | Twitch's warning screen with escalation on top: warnings, a final warning, then a timeout, a ban or a restriction. Your moderators' own warnings can count too. |
| **[Permits](#permits)** | A time-limited link exception for one viewer, granted by you, a moderator, or a Channel Points redeem. |
| **[Check Link](#check-link)** | Scans a URL with VirusTotal and IPQualityScore, either automatically or on `!checklink`. |
| **[Voting](#voting)** | Lets chat vote someone out, with roles above VIP permanently unvotable. |
| **[Discord Alerts](#discord-alerts)** | Posts what happened to a webhook, one toggle per kind of action. |
| **[Windows Notifications](#windows-notifications)** | A Windows notification for a new TwitchSentry release and, if you want them, for what a deck button did or could not do. |
| **[Deck Buttons](#deck-buttons)** | Switches profiles, modules, exemptions and test mode, arms Raid Protection or takes the last action back, from a Stream Deck key or a Streamer.bot Deck button. |

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

The defaults are meant to be a working configuration, not a starting point you have to tune. If you change nothing at all, TwitchSentry filters links and spam, watches how people chat, learns from what it removes and hands out permits; Raid Protection, Follow Protection, AutoMod, Twitch Warn, Check Link, Voting and Discord Alerts stay off until you switch them on.

---

# The settings window

| Dark Mode | White Mode |
|:---:|:---:|
| ![before](https://github.com/user-attachments/assets/2524f403-8f7e-4cce-b56a-fd131277af4c) | ![after](https://github.com/user-attachments/assets/295f46ee-153e-445f-90bf-5e650d7c51b9) |

Pages are grouped down the left: **Setup**, **Filters**, **Spam**, **Global Modules**, **Messages**, **Results** and **Help**. Click a group heading to collapse it.

The window opens on **Home**: the version you are running, six shortcut tiles to the pages most people came for, a *Right Now* card summarising what TwitchSentry is currently set to do, and links to the [Manual page](#manual), the FAQ, the report form, the repository and the Streamer.bot thread. Nothing on Home is editable — every line on it lives on the page that owns it, and the tile takes you there.

**A few things worth knowing before you start:**
- **The search box** at the top left filters the page list by page name, setting label, or the internal setting key. `Ctrl+F` focuses it, `Esc` clears it. If you know roughly what a setting is called, this is faster than hunting for the page.
- **The ☰ menu**, in front of the search box, holds the things you reach for occasionally: profiles, the light/dark theme, expert mode, the language files, test mode, sharing with other streamers, opening a ticket, and both reset buttons.
  - **Opening a ticket** fills in GitHub's new-issue page and opens it in your browser — nothing is sent from the window, and you submit it yourself under your own account. The first dropdown decides whether it is labelled `bug` or `enhancement`; the second says which part of TwitchSentry it is about, and becomes a second label so tickets about the same thing sit together. *Not sure* is one of the choices and a perfectly good answer. A block describing your setup always rides along, shown in full before it goes: TwitchSentry's version, settings schema, whether betas are announced and which profile you are on; the Streamer.bot version; your window language and which version of that language file, the theme, and whether expert and test mode are on; which modules are on and which are off; the shared action and the four sensitivity steps; whether the VirusTotal key, the IPQS key and the Discord webhook are **set or not set**; whether the two cache files are there; and your Windows build, CLR version and desktop size. No channel name, no API keys, no webhook URL and no file paths.
- **The notice strip** across the top carries anything the window needs to tell you — an available update, a translation that is behind, a setting that will not do what it looks like it does. Notices stack, and the **✕** on one hides it for good. An update notice for a beta also carries **Ignore Betas**, which does the same for every beta to come: only stable releases are announced after it. If you want them back, *Show hidden notices again* in the ☰ menu clears the list.
- **The ? in a card's corner** opens the [Manual page](#manual) at that card's section, for the cards whose options need more than their tooltips. A **?** in a page's title bar opens what the Manual says about the page as a whole.
- **Nothing is saved until you press Save.** The bottom left says whether you have unsaved changes.

<img width="917" height="127" alt="grafik" src="https://github.com/user-attachments/assets/97fecd24-a799-4321-b976-8b043f2c78d1" />

### Profiles

In the **☰ menu**, at the top. One decision instead of forty: how hard the message filter, the raid
and follow filters and spam scoring all push, set together. Picking one writes those settings and
reopens the settings window showing them, so nothing changes behind your back and you can tune
anything afterwards.

**Five built-in profiles ship with TwitchSentry**, and those five names are reserved.

| Profile | What it is for |
|---|---|
| **Relaxed** | Best for small chats or background guard. Every check still runs, the cosmetic ones only look at somebody's first message. |
| **Balanced** | Best for most chats. Default Preset. |
| **Strict** | Best for crowded chats. Tighter thresholds and each check fires faster. |
| **Under Attack** | Best for bot attacks. Everything at its tightest, chat modes enable automatically on an incoming raid rather than after the first message. |
| **Just Chatting** | Best for talking or reaction streams. The message and spam sides ease off; the raid and follow sides stay as they are. |

Every built-in profile names the same settings, which is what makes coming back work: **Balanced** genuinely
undoes what **Under Attack** turned on, rather than leaving the heavy switches standing.

**Saved profiles are yours.** Type a name under *Save Your Profile* and **Save Current Settings** writes
what you are running to `TwitchSentry/Settings/Profiles`, where it joins the list under that name.
Anything else dropped into that folder shows up too, so a profile a friend sent you only has to be
copied there. Each one shows how many settings it carries and when it was written, and the **✎**
beside one **renames** it, and the **↺** beside that writes what you are running now into it, keeping its name and its file. Nothing in this window deletes or moves a profile file — the folder is the list, and what is in it is yours to arrange.

**The title bar says which one you are on.** *TwitchSentry – Settings · Strict*, or *· Strict (modified)*
once the settings that profile names no longer say what it said.

**When *(modified)* appears is a question about span, and the two kinds of profile have very
different ones.** A built-in profile claims exactly 34 settings: the four sensitivity sliders, all 23 dials
behind them, and seven switches (*Require Two Signals* on the message and raid sides, *Require Two
Parts*, *First Message Only*, *Activate Modes On Arm*, and Shield Mode on a raid and on a follow
wave). It has no opinion at all about the other 227, so changing an action, a timeout duration, a
message, a Discord switch or a whole module on or off leaves you sitting *exactly* on Strict, with no
marker. That is the honest reading rather than a flag that would be on permanently.

A saved profile claims all 261, so almost any change marks it modified. If you want the tight
reading, save your settings as a profile: that is what makes every one of them something to drift
from.

**Before you click one, it tells you what it would do.** Under every profile in the list is a *would change N settings* line; open it and each one is there, with what it says now and what the profile would put in its place. A profile that matches says *nothing would change* instead. This matters because picking a profile writes `configs.json` and reopens the settings window — finding out by trying is the expensive way round.

**The list is the folder, live.** It is re-read every time the window comes back to the front, so a file you drop in, rename or delete in Explorer shows up without closing and reopening the dialog — and the folder button in the corner is one click away. A search box appears above the list once there are six or more.

**What a profile holds.** Every threshold, every switch, every action and every duration — the whole
of how strict this channel is, which is 261 of the 297 settings in `configs.json`.

**What it deliberately does not:** your Discord webhook and your VirusTotal and IPQS keys; the people
and addresses this channel knows, meaning your whitelist, your excluded and trusted users, the AutoMod
allow list and the Follow Protection block list; and what belongs to this install rather than to a
policy — bot account, language, theme, backup folder, and whether test mode is running.

**Import Profile...** reads a file from anywhere, copies it into the Profiles folder so you can come
back to it, and then applies it the way picking a built-in profile does: what the file names is written,
everything else is left where it is.

The same filter runs in both directions, so a profile file that has had a webhook URL written into it
by hand still cannot put one into your settings — the key is dropped on the way in, not merely left
out on the way out. A file that is not a profile is refused rather than half-applied, and keys from a
newer version than yours are counted and ignored instead of throwing.

**Switching from a deck.** A Stream Deck key or a Streamer.bot Deck button can switch profiles
mid-stream without this window, see [Deck buttons](#deck-buttons). The Profiles dialog lists the names
to put on a key under *Switch From A Deck*.

### Test mode

Switched on from the ☰ menu. While it runs, nothing is deleted, timed out or banned — every module posts what it *would* have done instead, so you can point a real chat at your settings without anybody being punished for helping you test them. Not even the chat modes come on. It ends on its own after the time set on General Settings, five minutes by default, and the notice strip counts it down — so a chat can never be left unguarded because somebody forgot to switch it back.

### Easy & Expert mode

| Easy Mode | Expert Mode |
|:---:|:---:|
| ![before](https://github.com/user-attachments/assets/f86f6495-7e20-436c-af26-e0c9dd3570d3) | ![after](https://github.com/user-attachments/assets/af74522b-7c7e-4140-8eb3-2b2883376a05) |


`Easy Mode` is active by default, intended for users new to TwitchSentry or this type of system at all. Simplified settings with a **sensitivity slider** to choose — `Very relaxed` through `Very strict`, with a line under it saying what the step actually means and does. 
Also in the ☰ menu. Expert mode reveals the individual numbers the slider is moving for you. In expert mode `Custom` gives you the possibility to create your own slider sensitivity and is remembered by the GUI if you move away from it, as long as you have hit `save` once.

`Custom` only appears while expert mode is on: the rows it keeps *are* the expert rows, so there is nothing to tune without them, and with expert mode off the slider ends at `Very strict`. A slider that is *already* sitting on `Custom` keeps the stop either way — switching expert mode off never drops a preset column over numbers you tuned yourself.

---

# Setup

## General Settings

<img width="926" height="1491" alt="grafik" src="https://github.com/user-attachments/assets/298969cd-e65b-4b75-b0cd-70d2955dbaeb" />

Behaviour shared by every module: whether to speak through your bot account, whether to reply in chat, and whether a message may speak of a viewer by [their pronouns](#speaking-of-a-viewer-by-their-pronouns). Then **test mode**'s duration and wording, and the **exemptions** — followers, subscribers, VIPs, named viewers and Streamer.bot groups — which apply to the six modules that take action on a message. **Whitelisted Domains** lives here too.

A whitelist entry without a trailing `/*` is an exact match: `twitch.tv/yourname` allows that one link and nothing nested under it, so anything below it needs `twitch.tv/yourname/*`.

**Always Allowed**, the card below the whitelist, is the shortcut for the entry most people write first: switches that let your own clips and videos through for everybody, without a permit and without a whitelist line. The channel names are read from whichever accounts Streamer.bot is signed in to, so a rename follows along.

The switches come in two groups, because a link can only be checked against your channel when your channel's name is in it:

- **Only Your Channel** — your Twitch clips (`twitch.tv/yourchannel/clip/…`), your Twitch channel page (`twitch.tv/yourchannel`, and the pages under it), your YouTube channel page (`youtube.com/@yourhandle`), your Kick clips and your Kick VODs. The address names your channel, so a clip or video of anybody else's is still judged by the Link Filter. A platform Streamer.bot is not signed in to matches nothing here.
- **Any Channel** — the same shapes with the channel left open, each on its own switch: Twitch clips (`twitch.tv/anychannel/clip/…`, and `clips.twitch.tv/…` for the same clip by a shorter address), Twitch VOD links (`twitch.tv/videos/…`, which is what Twitch's own Share button gives for a VOD), YouTube videos, Shorts, live streams and clips, and Kick VOD links (`kick.com/video/…`). Ticking one allows that kind of link for every channel on the platform, not only yours. Most of these addresses name no channel at all; a clip address always names one, and that switch simply does not read it.

They sit here rather than on the Permits page because they are not a permit: they keep working with Permits switched off entirely.

## Discord Alerts

One switch per thing that can happen, not per module: what you are deciding is how much you want to
hear, and a permit being granted happens hundreds of times more often than one being revoked.
Twenty-one of them, grouped by where the alert comes from.

Every alert says what happened in one word, the same in every module: **DELETED**, **TIMEOUT**,
**BANNED**, **WARNED**, **RESTRICTED**, **BLOCKED** and so on, under a title that names the module the
way the window does (*Spam Scoring — Action Taken*). The evidence is a bulleted **Why** — *Account is
12d old, under the 30d minimum*, *78% capital letters* — rather than a comma-run of tokens. The
tokens stay in the action log and the Streamer.bot log, where they are the more useful form.

Alerts are queued and sent on a background thread, so moderation never waits on Discord. A single
alert goes out immediately; a burst arrives as one message carrying up to ten of them, which is what
keeps a raid from spending Discord's rate limit on thirty separate requests.

<img width="926" height="1491" alt="grafik" src="https://github.com/user-attachments/assets/436ea1c4-fab0-4dd4-9b63-55ff2c77e956" />

Off by default, a discord webhook and one toggle per kind of action. A pasted webhook is covered with dots straight away, so the window is safe to have on stream; the eye beside it uncovers it.

Example:
<img width="403" height="344" alt="grafik" src="https://github.com/user-attachments/assets/7ecf5eda-d6f6-4325-abfd-dc9e5bbf27ce" />
<img width="404" height="287" alt="grafik" src="https://github.com/user-attachments/assets/bf33fd04-f4af-4502-b836-24e67152a8be" />

**Create a discord webhook:**
* Right-Click on desired channel
* Edit Channel
* Create WebHook
* Give your webhook a fancy name and a logo
* Copy WebHook URL

**When Twitch says no:** an alert can read **TIMEOUT REFUSED** rather than **TIMEOUT**. Twitch answers every deletion, timeout, ban and warning with a yes or a no, and a no is reported rather than swallowed: the viewer was not touched, nothing went into the undo trail and nothing was said in chat, so the alert is the only record. The **Status Log** page carries the reason — usually a target Twitch will not let a bot touch, a message somebody else has already removed, or a missing scope on the Streamer.bot Twitch account.

**How the alerts look in Discord:** under *Webhook Appearance* on the *Discord Webhook* card there are two more fields, **Display Name** and **Avatar URL**. Discord names a new webhook itself and that name says nothing about what is posting, so these ship as `TwitchSentry-Log` and the TwitchSentry logo and ride along with every alert — you do not have to give the webhook a fancy name and a logo yourself unless you want to. Empty either box and that override is not sent at all, and whatever the webhook carries in Discord shows through instead; that is the way back. Discord refuses a display name over 80 characters, or one containing *discord* or *clyde*, and refuses the whole post along with it, so TwitchSentry drops such a name rather than lose the alert — and the window warns you when you save one.

## Windows Notifications

<img width="926" height="1491" alt="grafik" src="https://github.com/user-attachments/assets/ebf6641f-12f6-4462-8797-e397081302c9" />

A small Windows notification in the corner of the screen, kept afterwards in Windows' notification
centre. It works while the settings window is closed, and carries TwitchSentry's icon once the window
has been opened at least once. The switch in the page's title bar turns all of them on or off; below it
is one switch per kind:

| Switch | Default | When |
|---|---|---|
| **On New Releases** | on | A new TwitchSentry release is out. Once per release; the settings window looks for one each time it opens. |
| **On Deck Button Actions** | off | A [deck button](#deck-buttons) just did something: switched a profile, a module or an exemption, test mode, Raid Protection, an undo. |
| **On Deck Button Problems** | on | A deck button could not do what it was asked, and why: a profile that no longer exists, a name that matches nothing, a `configs.json` that cannot be read. |

**Show A Test Notification** sends one straight away, whatever is switched on. If nothing appears,
Windows is holding it back: check *Do Not Disturb* (*Focus Assist*) and *Settings → System →
Notifications*, where Streamer.bot has to be allowed to send notifications.
<img width="396" height="149" alt="grafik" src="https://github.com/user-attachments/assets/0dada811-9bec-43c9-8f0d-47f97886b34f" />

---

# Filters

## Message Filter

| Easy Mode | Expert Mode |
|:---:|:---:|
| ![before](https://github.com/user-attachments/assets/1cc3d103-99fc-434d-bb42-bf2376e27a3d) | ![after](https://github.com/user-attachments/assets/b5455fb6-f8f2-4670-b9f5-69f74fc579ed) |


Looks at how someone is chatting rather than at particular words: account age, ALL CAPS, emote spam, and posting too fast or repeating yourself.

No single one of those is proof of anything on its own — people shout, people spam emotes when something good happens — so a message is only acted on when at least two of them show up together, or when one of them is the kind that is not an accident. A repeated message is decisive on its own; being new to Twitch is a risk factor that makes whatever else the message tripped count for more, never a finding by itself. Someone with a long history in your chat needs more evidence than a stranger does.

Each of the four checks has its own switch and there is no module-wide one: unticking every check is what silences it.

**Escalation** sits on top of that and deals with the whole chat rather than one viewer. When enough *different* people trip the filters inside the same window, a Twitch chat mode is switched on for everyone and lifted again on its own. Which mode gets picked depends on what the wave looks like — and the table at the bottom of the page shows exactly what would happen with the boxes as you have them ticked right now, renumbering as you tick and striking through a mode you have switched off.

## Raid Protection

| Easy Mode | Expert Mode |
|:---:|:---:|
| ![before](https://github.com/user-attachments/assets/1f440b4e-b638-4aa3-82ea-78b1cb4751c9) | ![after](https://github.com/user-attachments/assets/e60ffaff-ca33-41c5-9289-2f3a518cd6fb) |

The same idea as `Message Filter` but stricter and only armed for a limited window right after an incoming raid. Plus: **swarm detection**, which spots several different accounts posting near-identical messages at once which then gets scored against bot patterns.
It has its own escalation ladder and its own progressive escalation, so a second wave of the same pattern moves up a step instead of re-picking the mode that is already running.

## Follow Protection

| Easy Mode | Expert Mode |
|:---:|:---:|
| ![before](https://github.com/user-attachments/assets/3dcbc4f9-a940-4844-b324-c4d1621423f5) | ![after](https://github.com/user-attachments/assets/b8df4859-a2ae-475a-bac9-8fba1376eb5e) |

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
| ![before](https://github.com/user-attachments/assets/ed021f3a-b5c5-4aa2-843f-2768e8c08b8d) | ![after](https://github.com/user-attachments/assets/172a8972-aa35-4022-857c-dcb9ee3601fc) |

This does not judge a message by how many red flags it trips. It asks whether the message is built like an advert. An advert has parts: somewhere to go (**Destination**), something being sold (**Offer**), a way to redeem it (**Instrument**), the random `@handle` a spam bot signs with (**Tag**), and wording this channel has seen from spam before (**Signature**).

One part on its own is a coincidence — plenty of ordinary messages have one. Two parts together is an advert. That is what the sensitivity slider controls, and why false positives are rare: no single keyword is ever the whole verdict.

**Conversation Scam** is tracked separately, because it is a different animal from the bot that drops one advert and leaves. This account chats with you: it asks how long you have been streaming, says your channel looks a little empty, mentions that a logo or a VTuber model would fix that, and only then tells you it sells exactly that. No single message it sends is spam — the tell is the order. Four stages are tracked per account inside a window, they only count moving forwards, and it only acts once an account has walked them in order and ended on the offer. Being a familiar face does not buy an exemption here — it raises the bar to all four stages instead of three. Sitting in a channel for hours is how these accounts earn their standing in the first place.

## Known Patterns

<img width="926" height="1491" alt="grafik" src="https://github.com/user-attachments/assets/51d9fb62-0985-4796-a436-56a589d6735e" />

The actual active rules every module checks against — `spam.json`, editable in place. Spam domains, keywords, strong keywords, domain endings, custom patterns and voucher-code patterns, plus the four **conversation beats** the scam detector matches on. Add your own here, or approve what the Learner suggests. Don't forget **Save**.

**New entries arrive on their own.** When a new viewer-selling site starts circulating, it is added once to the [spam feed](https://github.com/aaskjer/TwitchSentry/blob/main/Feed/README.md), and within a few hours it shows up in these lists — no new version to import. Each entry arrives exactly once: delete one here and it stays deleted. The feed only ever adds to the plain-text lists; custom patterns and voucher patterns are yours alone. **Receive New Entries** at the top of the page switches it off.

**Share what you found.** *Share With Other Streamers...* on this page, or *Share With Others...* in the ☰ menu, offers the entries in your lists that TwitchSentry does not have yet: nothing the feed already carries, and nothing a version shipped as a default. Each list is headed with what an entry in it does, and *How this works* above the list explains the rest, including why a conversation stage can show up on its own. Tick the ones worth passing on and it opens a GitHub form with them filled in; you press Submit there yourself, and once an entry holds up it reaches everyone else through the feed. The same dialog shares your saved settings as a profile, or a complete translation file. Nothing is sent from the window, and only the entries go along — never a chat message or a name. A single translated text that reads badly is a ticket rather than a share: *Report...* in the ☰ menu, *A translation*.

A shared profile is too long for the link, so it goes onto your clipboard to paste into the form. If Windows will not hand the clipboard over (it happens in Remote Desktop sessions), the form opens anyway and the dialog shows the profile, with *Copy Again* beside it. Once you submit, the repository checks the profile the way the window checks an import, and if it holds up it is stored on the [`profiles` branch](https://github.com/aaskjer/TwitchSentry/tree/profiles) and the ticket is closed. There is no pull request and nobody has to accept it, so it doubles as a backup: download the file from there and put it into `Settings/Profiles`, on this PC or any other.

## Spam Learner

<img width="926" height="1491" alt="grafik" src="https://github.com/user-attachments/assets/dbd692ab-c025-4a69-9250-70dfbe5cf39b" />

Watches what actually got removed and works out which words, phrases and domain endings keep showing up in it, scoring each candidate by how much more often it appears in spam than in ordinary chat. New finds start as suggestions for you to review; they are promoted into the real rule list only once they have built a track record — either because you approve them, or automatically if **Auto Promote Trusted Rules** is on.

Only *content* violations feed it. The fact that somebody typed too fast tells you nothing about which of their words were spam, so behavioural violations contribute none. On top of that sit an **Ignore Terms** list, automatic protection for your own account names, a denylist for major brands, and the clean-chat sample described below.

## Suggestions

<img width="926" height="1491" alt="grafik" src="https://github.com/user-attachments/assets/a5ef63b4-bac9-46ce-8d5b-adc7c95c4179" />

Everything the Learner has proposed but not applied. Read the **Would hit** column first: that is how many messages from your own clean chat log the rule would have matched. Zero is what you want, and anything above zero is never auto-promoted. **Users** counts how many different people posted it, so one spammer repeating himself counts once; **Discrim.** is how much more often it shows up in spam than in ordinary chat.

**Probation** means a candidate is still building a record; **trusted** means it is proven enough to be auto-promoted, if you have turned that on. **Clear File** wipes the pending list and leaves your active rules alone.

---

# Modules

These are off by default, except Permits. Each is genuinely optional — the two filters above are the core, and everything here is something you may or may not want.

## AutoMod

<img width="926" height="1491" alt="grafik" src="https://github.com/user-attachments/assets/9bee3152-a497-43c5-9081-b8465f9569d3" />

**Off by default**. Twitch's own AutoMod holds suspicious messages back and waits for a moderator to approve or deny each one. This answers them for you, by level and by category. Leave **AutoMod Categories** empty to act on everything Twitch holds, or list only the categories you care about.

## Twitch Warn

<img width="926" height="1491" alt="grafik" src="https://github.com/user-attachments/assets/3236a485-3488-4b78-a332-937b44ec8a95" />

A warned viewer has to read and click through a warning screen before they can chat again, and Twitch keeps the count in their moderation history. **Warning Escalation** adds steps on top: warns accumulate, the last one before the threshold is a final warning, and the violation after that becomes a timeout, a ban or a **restriction**. A restricted viewer stays in chat, but everything they write from then on reaches only the moderators. Counts reset on their own after a quiet period.

Two switches go with it:

- **Monitor From The Final Warning** flags the viewer as monitored on Twitch along with the final warning. They chat as before, and the moderators see a marker on every message they send, so whoever is watching knows who is one violation away.
- **Count Warnings From Moderators** counts a warning a moderator gives in Twitch — `/warn`, or the warning on the viewer's card — towards the same ladder. It needs the trigger **Twitch > Moderation > Warned User** on the TwitchWarn action; the settings window says so while that trigger has never fired. A moderator's warning never escalates by itself, and TwitchSentry's own warnings, which Twitch reports through the same trigger, are not counted twice.

A restriction and a monitoring are both lifted with `!tsundo`, from a deck button, or on the viewer's card in Twitch.

## Permits

<img width="926" height="1491" alt="grafik" src="https://github.com/user-attachments/assets/03deb61c-ec42-4e7b-a5ca-315662ff7bab" />

A time-limited exception for a viewer, so they can post a link without it getting deleted. `!permit @user [seconds]` grants one, `!endpermit @user` ends it, `!endpermit` on its own ends every active permit. Several people can hold one at the same time, each with its own countdown; a permit that is already running is never extended. They are deliberately forgotten on restart.
**Max Permit Duration Seconds** caps whatever a moderator types, with a hard ceiling of 24 hours.
Viewers can also redeem a permit themselves through Channel Points, if **Allow Self-Permit** is on. Set that reward up with **Skip Reward Requests Queue** turned **off** — that is what lets TwitchSentry give the points back when a redemption cannot become a permit. A reward that skips the queue is spent the moment it is redeemed, and Twitch will not allow a refund.

## Check Link

<img width="926" height="1491" alt="grafik" src="https://github.com/user-attachments/assets/454d6ee6-c3c5-42c8-be7f-790e7375f1b2" />


Two jobs: Anyone can scan a URL on demand with `!checklink <url>`. The second feature adds a scan on top of the ordinary link rule and automatically scans any incoming link in chat.
Uses VirusTotal (required, free key) and optionally IPQualityScore for a second opinion. IPQS rates a link from 0 to 100; the default threshold is 75, with a stricter one for domains it also reports as recently registered, since a brand-new throwaway domain is a phishing classic.

## Voting

<img width="926" height="1491" alt="grafik" src="https://github.com/user-attachments/assets/8d6b263b-049d-4bfe-8f7e-1271addde19b" />

Lets chat decide! `!vote @user` starts or joins a vote, and enough *unique* voters inside the time window time that person out — or ban them, if you allow it. The window running out resets the vote. Subscribers and VIPs can be exempted, there are separate exclusion lists for users and Streamer.bot groups, and **everyone above VIP is permanently unvotable!**

---

# Messages

Everything TwitchSentry says in chat, one page per module, with the placeholders each message accepts listed under the box. Nothing here is translated for you — this is your bot's voice, your wording and your language, so a German channel picks Deutsch for the window *and* writes these in German.

| Command Replies | Message Filter Messages | Raid Protection Messages | 
|:---:|:---:|:---:| 
| ![](https://github.com/user-attachments/assets/c60d7514-7d40-4556-a47a-8196c67e523a) | ![](https://github.com/user-attachments/assets/5a6031e7-b36b-4fd3-a37c-d427376d90b1) | ![](https://github.com/user-attachments/assets/03dad722-04f7-4096-aa9f-0f0c469dbd64) |
| Link Filter Messages | Spam Scoring Messages | Spam Learner Messages | 
| ![](https://github.com/user-attachments/assets/6000bcb7-4a03-4fc3-b6e1-ccc1b747e253) | ![](https://github.com/user-attachments/assets/d3ee38ef-4722-46fc-89e9-2e0acb8b7372) | ![](https://github.com/user-attachments/assets/454741f7-4aa6-4ae7-9286-db6c45f78f10) |
| AutoMod Messages | Warn Messages | Permit Messages | 
| ![](https://github.com/user-attachments/assets/682a7a11-c0e4-491b-be03-37885e0703ca) | ![](https://github.com/user-attachments/assets/3fc448fa-2156-4b25-976d-ccfb8e6cf0d7) | ![](https://github.com/user-attachments/assets/b97dcaa7-d92c-4829-8f62-0cf92cc539ef) |
| Check Link Messages | Voting Messages | | 
| ![](https://github.com/user-attachments/assets/3448a6a7-2752-4241-9866-e81d0d2834db) | ![](https://github.com/user-attachments/assets/0b217de7-b614-43d1-be0c-9d7b2568b6e3) | |

## Speaking of a viewer by their pronouns

A message about a viewer can use the pronouns they set on [pronouns.alejo.io](https://pronouns.alejo.io):
`{pronoun:he|she|they}` holds three forms, written in whatever words your language needs. The first is
used for *he/him*, the second for *she/her*, the third for *they/them* and for anyone whose pronouns are
not known: none set, *Any* or *Other*, or the switch off. The switch is **Use Viewer Pronouns** under
General Settings → Behavior, off by default.

Every other set alejo.io offers (*xe/xem*, *fae/faer*, *ve/ver*, *ae/aer*, *zie/hir*, *per/per*, *e/em*,
*it/its*) takes the first form in the viewer's own words: its *he*, *him*, *his* and *himself* become
theirs, since these pronouns take the same verbs as *he*. A first form that is not English has no such
word to change, so these viewers get the third form instead.

| In the message | he/him | she/her | they/them, not known | xe/xem | it/its |
|---|---|---|---|---|---|
| `{pronoun:He is\|She is\|They are} back` | He is back | She is back | They are back | Xe is back | It is back |
| `give {pronoun:him\|her\|them} a follow` | him | her | them | xem | it |
| `{pronoun:his\|her\|their} clip` | his | her | their | xyr | its |
| `{pronoun:er\|sie\|die Person} ist zurück` | er | sie | die Person | die Person | die Person |

- It speaks of the viewer the message is about: `{user}`, or `{target}` on the Voting page. Every message
  with one of those offers the placeholder as a chip under its box. One message may use it several times.
- Twitch keeps no pronouns, so only viewers who set theirs on pronouns.alejo.io are known. Streamer.bot
  looks them up (its own Pronouns integration) and TwitchSentry keeps the answer for an hour, so a raid
  does not ask once per message. A lookup that takes longer than 2 seconds gives the third form rather
  than holding the reply.
- Leave a form out and the last one written stands in for it, so always write all three.
- Nothing is looked up for a message that does not use the placeholder, and a message about nobody in
  particular (an escalation notice, say) always takes the third form.

---

# Results

## Action Log

<img width="926" height="1491" alt="grafik" src="https://github.com/user-attachments/assets/9d3bcdfa-249a-4079-94c0-a16cd035d7f0" />

Every action involving a viewer this month, filterable by module and by result, with the raw line underneath. This is the page for *what happened*.

Each month starts a new `action-log.txt` (and a new `violation-log.txt`). The month before is moved aside in the same `Logs` folder as `action-log-2026-09.txt` and so on, and nothing is deleted. The Home counters still count the older months, and the Spam Learner's History Lines reach back into them, so a new month does not start its memory from nothing.

## Status Log

| Issues Only | All TS Logs |
|:---:|:---:|
| ![before](https://github.com/user-attachments/assets/60a72f58-dff8-47d3-9653-d1cbdf9e2a92) | ![after](https://github.com/user-attachments/assets/9250c9fb-6841-4b9b-83f5-c5facb7ece52) |

What TwitchSentry has been saying about *itself*, pulled out of the Streamer.bot log: an API key still on its placeholder, a download that failed, an action Twitch refused. None of that is announced in chat, so this is the page to open when something quietly did not happen.

## Violation Log

<img width="926" height="1491" alt="grafik" src="https://github.com/user-attachments/assets/6abf0ee0-1ade-4597-bead-89d60abe8a52" />

The **Violation Log** is every message that was acted on this month, exactly as it was posted — the page to open when you disagree with a removal. Earlier months are in `violation-log-2026-09.txt` and so on, beside it in the `Logs` folder.

## Clean Chat Log

<img width="926" height="1491" alt="grafik" src="https://github.com/user-attachments/assets/778f0cbc-8fe2-4fd0-8375-b8461f35a54b" />

The **Clean Chat Log** is the opposite of the violation log: a sample of ordinary chat that was deliberately left alone, roughly one message in ten. The Spam Learner measures its candidates against it, which is what stops an everyday word from becoming a rule. Both pages have a search box and a per-account filter, and both show the full line under the list, because chat messages are usually wider than the row.

---

# Help

## Manual

<img width="926" height="1491" alt="grafik" src="https://github.com/user-attachments/assets/08977284-9a50-4208-9093-feca29170f07" />

The longer explanation behind every card with a **?** in its corner, page by page in the order of the sidebar, and a list of every [chat command](#chat-commands) under *Command Replies*. A **?** opens the Manual at its card's section and lights it up for a moment; **← Back to …** at the top takes you back to the page you came from, scrolled to where you left it. Opened from the sidebar or from Home, the Manual has no back button.

The cards themselves stay short: an explanation of a sentence or two lives only in the Manual, a longer one keeps a short version under the card's *How this works*. Installing TwitchSentry, the deck buttons and where the files live are covered only here, in the online manual, which the Manual page links to.

## Backup & Restore

<img width="926" height="1491" alt="grafik" src="https://github.com/user-attachments/assets/12156697-c485-44ae-8309-73e7293dad7a" />

Everything TwitchSentry knows about your channel is a handful of files in one folder, and two of those
files are things nothing can give back: your settings and the replies you have written, and the
keywords, phrases and domain endings the Spam Learner has built up from months of your own chat.

**Backing up** writes a dated folder of ordinary files. Tick what goes in: settings and chat messages,
learned spam data, language files, logs, cache. The first two are the parts nothing can give back; they
and the language files are ticked by default. All five ticked is the whole TwitchSentry folder, a few hundred kilobytes unless
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

**If one of TwitchSentry's own files cannot be read at all**, the settings window says so before it
opens, in a window of its own: which file it is, what it holds and what the reader made of it. From
there you can put a copy back from one of your backups — only the ones holding a readable copy are
offered, newest first — or open the folder, correct the file and check again, or start on the defaults,
which renames the damaged file to `.bak` beside itself and keeps saying so in the window until you save.
A file that is simply not there yet, as on a fresh install, is not damaged and nothing is said.

---

# Deck buttons

A Stream Deck key or a Streamer.bot Deck button can do what a streamer wants mid-stream without opening
the settings window: switch profiles, switch a module or an exemption, start or end test mode, arm Raid
Protection, take the last action back. The action behind them is **`[TS] - Deck`**. It works on what the
other actions share — `configs.json`, the Profiles folder and Streamer.bot's globals — so it does not
matter whether the settings window is open.

## Setting up a key

A key runs `[TS] - Deck` and says in an argument what it wants:

| Argument | Example | What it does |
|---|---|---|
| `tsProfile` | `Under Attack` | Switches to that profile: `Relaxed`, `Balanced`, `Strict`, `Under Attack`, `Just Chatting`, or the name of one of your saved profiles |
| `tsModule` | `Voting off` | Switches a module on or off: `Raid Protection`, `Follow Protection`, `AutoMod`, `Twitch Warn`, `Permits`, `Check Link`, `Voting`, `Spam Learner`, `Discord Alerts` |
| `tsExempt` | `VIPs on` | Whether `Followers`, `Subscribers` or `VIPs` are left alone by the filters — *Exclude Followers*, *Exclude Subscribers* and *Exclude VIPs* on General Settings |
| `tsTestMode` | `on` | Test mode `on` for the *Test Duration* on General Settings, `off`, or `toggle` |
| `tsRaid` | `arm` | Arms Raid Protection now, without a raid, or `disarm` ends it |
| `tsUndo` | `last` | Takes back the last timeout, ban, restriction, monitoring or block, as `!tsundo` does; `@name` takes back that viewer's last one |

The state after a module or an exemption is `on` or `off` (`an` and `aus` work too). Left out, the key
switches the setting over, which is what a plain key wants. Names ignore upper and lower case, spaces and
dashes, so `follow-protection on` is Follow Protection.

- **Stream Deck**, with the Streamer.bot plugin: an **Action** key on `[TS] - Deck`, with the argument
  under its arguments. For something that goes on and off, an **Action Switch** key with `[TS] - Deck`
  on both sides: `tsModule = Voting on` on *Toggle On* and `tsModule = Voting off` on *Toggle Off*, or
  `tsProfile = Under Attack` and `tsProfile = Balanced` for a panic button that comes back.
- **Streamer.bot Deck**: a button that runs `[TS] - Deck` with the argument.
- **Anything else that runs an action** — a hotkey, a timer, a command of your own — works the same
  way. Where it cannot pass an argument itself, make a small action that first sets the argument
  (*Set Argument*) and then runs `[TS] - Deck` (*Run Action*): an action started that way gets the
  arguments of the one that started it.

**One key can do several things.** Give it more than one argument and they are carried out in the order
of the table: `tsProfile = Under Attack` together with `tsRaid = arm` is a panic button. A part that fails
does not stop the rest.

## What the key tells you

A Stream Deck key shows a ✓ when everything it asked for went through and a ⚠ when something did not,
for a moment, and then goes back to its own picture. The blue lightning bolt is that picture: it is the
Streamer.bot plugin's standard icon for an *Action* key, not a warning, and it stays until you give the
key an icon of your own. A Streamer.bot Deck button shows neither mark: what it did is in the logs, and in
a [Windows notification](#windows-notifications) if you switch those on. Either way the Streamer.bot log and the **Status Log** page say what happened, or why not: a name that
matches nothing (the line lists what there is), a `configs.json` that cannot be read, or one from an older
TwitchSentry, which the settings window brings up to date the next time you open it and press Save.
Whatever fails writes nothing.

## Notes on each

- **Profiles** are written exactly the way picking one in the Profiles dialog writes them, through the
  same filter, so a saved profile cannot bring a webhook URL or somebody else's whitelist in this way
  either. The English name always works. The name the window shows in your language works too, but only
  while the window stays in that language, so the English one is the safer label for a key: the Profiles
  dialog lists them under *Switch From A Deck*, with your language's name beside each.
- **Modules and exemptions** are the master switch at the top of a module's page and the three exemptions
  on General Settings, written the same way the window writes them. The Link Filter, Spam Scoring and the
  Message Filter have no switch, by design, so a key cannot switch them off either.
- **Test mode** is the same as the one in the ☰ menu: it ends by itself when its time is up.
- **Arming Raid Protection** does what an incoming raid does: the raid window, plus the chat modes and
  Shield Mode where *Activate Modes On Arm* and *Shield Mode On Raid* are on. It is for a wave of accounts
  that never came as a raid, so there is no raider to trust and no raid size to measure, and *Trusted
  Raiders* and *Min. Raid Viewers* do not apply. Pressed again while armed, it starts the window over
  without adding a chat mode. `disarm` lifts what arming put on, as the window running out would. Raid
  Protection itself has to be switched on.
- **Undo** follows `!tsundo` step for step: the newest entry on the undo trail, whichever module wrote it.
  When Twitch refuses, the entry stays on the trail to be tried again. It is written to the Action Log,
  and said in chat only where TwitchSentry says what it does in chat (*Reply In Chat*).

## With the settings window open

The window notices within a couple of seconds and says so in the notice strip — *A deck button switched
to Under Attack*, or *A deck button changed settings* — with **Reload** beside it, because its pages still
show what was running before. Saving without reloading does not undo the key: a setting you did not touch
in the window keeps what the key wrote, and one you did change keeps your change. Test mode started from
a key counts down in the strip, as it does from the menu.

---

# Chat commands

Moderator-only unless noted. TwitchSentry recognises each command by its Streamer.bot command id, so a command or trigger word renamed in the Commands tab keeps working; a command deleted and made again gets a new id and is no longer TwitchSentry's. A viewer's `!checklink` is left to Check Link while Check Link is on. Any other message that starts with a command is checked like every other message — moderators and the broadcaster are exempt from the filters anyway.

| Command | Manages |
|---|---|
| `!checklink <url>` / `!linkcheck <url>` | Scans a link with Check Link *(anyone)* |
| `!permit @user [seconds]` | Grants a temporary link permit |
| `!endpermit [@user]` | Ends that viewer's permit, or all of them |
| `!vote @user` | Starts or joins a vote *(anyone)* |
| `!endvote` | Ends the running vote early |
| `!wladd` / `!wlremove` / `!wllist` | Whitelisted Domains |
| `!amadd` / `!amremove` / `!amlist` | AutoMod Whitelist |
| `!euadd` / `!euremove` / `!eulist` | Excluded Users |
| `!egadd` / `!egremove` / `!eglist` | Excluded Groups |
| `!veuadd` / `!veuremove` / `!veulist` | Vote-Excluded Users |
| `!vegadd` / `!vegremove` / `!veglist` | Vote-Excluded Groups |
| `!kwadd` / `!kwremove` / `!kwlist` | Spam Keywords |
| `!tldadd` / `!tldremove` / `!tldlist` | Spaced-URL TLDs |
| `!tsundo [@user]` | Takes back the last timeout, ban, restriction, monitoring or follow block (or that viewer's last one) |

---

# Languages

<img width="446" height="423" alt="grafik" src="https://github.com/user-attachments/assets/4a36658a-007e-414f-8641-d356d796d3ea" />

The settings window ships in English, German, Spanish, French and Brazilian Portuguese, and Dutch comes from the community. Pick one from the ☰ menu; the window closes and reopens in it. Files are refreshed from GitHub in the background, and the window opens on the copy you already have if GitHub is unreachable.

This covers the window only. What the bot says in chat comes from the **Messages** pages and stays exactly as you wrote it.

Writing a translation is a matter of copying `Language/en.json` and replacing the values — each key is the exact English string from the window. Keep any `{user}`, `{count}` or `{duration}` placeholders spelled the same way. Save it under a code that is not published and it will never be overwritten. To bring it to everyone, **Share With Others...** in the ☰ menu → *A complete translation file*: for a language TwitchSentry does not have yet, or to bring an existing one up to date. One text that reads badly is quicker as **Report...** → *A translation*.

---

# Where the files live

Everything sits under your Streamer.bot base directory, in a `TwitchSentry` folder. You should never need to edit any of it by hand.

```
TwitchSentry/Settings/configs.json                   ← all module settings
TwitchSentry/Settings/messages.json                  ← everything the bot says in chat
TwitchSentry/Settings/Language/<code>.json           ← settings-window translations
TwitchSentry/Settings/Profiles/<name>.json           ← exported policy profiles
TwitchSentry/Machine Learning/spam.json              ← active keywords, phrases, patterns, TLDs
TwitchSentry/Machine Learning/spam-suggestions.json  ← the Learner's pending suggestions
TwitchSentry/Machine Learning/spam-feed-state.json   ← which spam feed entries were already handed over
TwitchSentry/Logs/action-log.txt                     ← this month's moderation action history
TwitchSentry/Logs/action-log-<yyyy-MM>.txt           ← earlier months, one file each
TwitchSentry/Logs/violation-log.txt                  ← this month's raw text the Learner mines from
TwitchSentry/Logs/violation-log-<yyyy-MM>.txt        ← earlier months, one file each
TwitchSentry/Logs/clean-log.txt                      ← sampled normal chat
TwitchSentry/Cache/stopwords.txt                     ← downloaded common-word list
TwitchSentry/Cache/tld_cache.txt                     ← downloaded valid domain-ending list
TwitchSentry/Cache/spam-feed.json                    ← the last downloaded spam feed
TwitchSentry/Cache/home-banner.png                   ← the banner on Home
TwitchSentry/Cache/TwitchSentry-Toast.ico            ← the icon Windows notifications carry
TwitchSentry/Backups/                                ← backups, unless Backup Folder points elsewhere
```

Settings are re-read whenever the file changes, so **Save** is enough — no Streamer.bot restart.

---

Questions are answered in more depth in the **[FAQ](https://github.com/aaskjer/TwitchSentry/blob/main/FAQ.md)**, and anything that looks wrong is worth an **[issue](https://github.com/aaskjer/TwitchSentry/issues)**.
