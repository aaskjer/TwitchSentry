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
| **[Message Filter](#message-filter)** | Watches *how* someone chats: account age, ALL CAPS, emote spam, flooding and repeats, and if you want them, repeated words, symbol spam, walls of text, mass mentions, ASCII art and Zalgo text. |
| **[Raid Protection](#raid-protection)** | Arms itself after an incoming raid and watches for a swarm of accounts posting the same line. |
| **[Follow Protection](#follow-protection)** | Watches follows. It counts how many different accounts arrive inside a short window and judges each on age, avatar, profile and login. |
| **[LurkBot Filter](#lurkbot-filter)** | Watches who sits in chat without writing. Looks up accounts with a bot wave's name shape and reports or bans the ones made on a known bot day, or on the same day as several others. |
| **[Word Filter](#word-filter)** | Your own list of words and phrases, found through their disguises, kept in step with Twitch's Blocked Terms, and `!nuke` for the wave no list knows yet. |
| **[Shared Bot List](#shared-bot-list)** | Bans the accounts other TwitchSentry channels identified as bots, from a shared list on GitHub, and reports the bots this channel is sure of to it. |
| **[Spam Learner](#spam-learner)** | Mines what was actually removed for new keywords, phrases and domain endings, and proposes them for review. |
| **[AutoMod](#automod)** | Answers the messages Twitch's own AutoMod holds back, so nobody has to sit in the queue. |
| **[Twitch Warn](#twitch-warn)** | Twitch's warning screen with escalation on top: warnings, a final warning, then a timeout, a ban or a restriction. Your moderators' own warnings can count too. |
| **[Permit](#permit)** | A time-limited link exception for one viewer, granted by you, a moderator, or a Channel Points redeem. |
| **[Check Link](#check-link)** | Scans a URL with VirusTotal and IPQualityScore, either automatically or on `!checklink`. |
| **[Voting](#voting)** | Lets chat vote someone out, with roles above VIP permanently unvotable. |
| **[Discord Alerts](#discord-alerts)** | Posts what happened to a webhook, one toggle per kind of action. |
| **[Windows Notifications](#windows-notifications)** | A Windows notification for a new TwitchSentry release and, if you want them, for what a deck button did or could not do and for any alert Discord Alerts can post. |
| **[Offline Protection](#offline-protection)** | Puts chat into the modes you pick when the stream ends, so an empty channel is guarded while Streamer.bot is closed, and lifts them when you go live. |
| **[Deck Buttons](#deck-buttons)** | Switches profiles, modules, exemptions, Always Allowed links, AutoMod's answer and test mode, arms Raid Protection, takes the last action back or grants a link permit, from a Stream Deck key, a Streamer.bot Deck button or the [OBS dock](#the-obs-dock). A key can show what it switched. |

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

The defaults are meant to be a working configuration, not a starting point you have to tune. If you change nothing at all, TwitchSentry filters links and spam, watches how people chat, learns from what it removes, hands out permits and bans the accounts on the [Shared Bot List](#shared-bot-list); Raid Protection, Follow Protection, LurkBot Filter, AutoMod, Twitch Warn, Check Link, Voting and Discord Alerts stay off until you switch them on.

---

# The settings window

| Dark Mode | White Mode |
|:---:|:---:|
| ![Dark mode](docs/screenshots/home.png) | ![White mode](docs/screenshots/home-light.png) |

Pages are grouped down the left: **Setup**, **Chat**, **Spam Filter**, **Bots & Raids**, **Moderation**, **Results** and **Help**. Click a group heading to collapse it.

A module's page has **tabs** under its title: its settings first, then **Messages**, everything that module says in chat. The Message Filter and Raid Protection also have a **Chat Modes** tab. The switch that turns a module on or off sits in the title bar, so it is there on every tab.

The window opens on **Home**: the version you are running, six shortcut tiles to the pages most people came for, a *Right Now* card summarising what TwitchSentry is currently set to do, and links to the [Manual page](#manual), the FAQ, the report form, the repository and the Streamer.bot thread. Nothing on Home is editable — every line on it lives on the page that owns it, and the tile takes you there.

**A few things worth knowing before you start:**
- **The search box** at the top left filters the page list by page name, setting label, or the internal setting key, and opens the tab that holds what it found. `Ctrl+F` focuses it, `Esc` clears it. If you know roughly what a setting is called, this is faster than hunting for the page.
- **The ☰ menu**, in front of the search box, holds the things you reach for occasionally: profiles, the light/dark theme, expert mode, the language files, test mode, sharing with other streamers, opening a ticket, and both reset buttons.
  - **Opening a ticket** fills in GitHub's new-issue page and opens it in your browser — nothing is sent from the window, and you submit it yourself under your own account. The first dropdown decides whether it is labelled `bug` or `enhancement`; the second says which part of TwitchSentry it is about, and becomes a second label so tickets about the same thing sit together. *Not sure* is one of the choices and a perfectly good answer. A block describing your setup always rides along, shown in full before it goes: TwitchSentry's version, settings schema, whether betas are announced and which profile you are on; the Streamer.bot version; your window language and which version of that language file, the theme, and whether expert and test mode are on; which modules are on and which are off; the shared action and the four sensitivity steps; whether the VirusTotal key, the IPQS key and the Discord webhook are **set or not set**; whether the two cache files are there; and your Windows build, CLR version and desktop size. No channel name, no API keys, no webhook URL and no file paths.
- **The notice strip** across the top carries anything the window needs to tell you — an available update, a translation that is behind, a setting that will not do what it looks like it does. Notices stack, and the **✕** on one hides it for good. An update notice for a beta also carries **Ignore Betas**, which does the same for every beta to come: only stable releases are announced after it. If you want them back, *Show hidden notices again* in the ☰ menu clears the list.
- **The ? in a card's corner** opens the [Manual page](#manual) at that card's section, for the cards whose options need more than their tooltips. A **?** in a page's title bar, or beside the first sentence of a later tab, opens what the Manual says about the page or that tab as a whole.
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
Parts*, *First Message Only*, *As Soon As A Raid Arrives*, and Shield Mode on a raid and on a follow
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
| ![Easy mode](docs/screenshots/spam-scoring.png) | ![Expert mode](docs/screenshots/spam-scoring-expert.png) |


`Easy Mode` is active by default, intended for users new to TwitchSentry or this type of system at all. Simplified settings with a **sensitivity slider** to choose — `Very relaxed` through `Very strict`, with a line under it saying what the step actually means and does. 
Also in the ☰ menu. Expert mode reveals the individual numbers the slider is moving for you. In expert mode `Custom` gives you the possibility to create your own slider sensitivity and is remembered by the GUI if you move away from it, as long as you have hit `save` once.

`Custom` only appears while expert mode is on: the rows it keeps *are* the expert rows, so there is nothing to tune without them, and with expert mode off the slider ends at `Very strict`. A slider that is *already* sitting on `Custom` keeps the stop either way — switching expert mode off never drops a preset column over numbers you tuned yourself.

---

# Setup

## General Settings

<img width="926" alt="General Settings" src="docs/screenshots/general-settings.png" />

Behaviour shared by every module: whether to speak through your bot account, whether to reply in chat, and whether a message may speak of a viewer by [their pronouns](#speaking-of-a-viewer-by-their-pronouns).

**Default Action** is what the Message Filter, the Link Filter and Spam Scoring do with a message that breaks a rule: delete it, time the viewer out for *Timeout Duration*, or ban them. It is one choice for all three; Raid Protection has its own, on its Detection tab.

Then the **exemptions** — followers, subscribers, VIPs, named viewers and Streamer.bot groups — which apply to the six modules that take action on a message, and **test mode**'s duration and wording. The whitelist and **Always Allowed** are on the [Link Filter](#link-filter) page.

## Command Replies

<img width="926" alt="Command Replies" src="docs/screenshots/command-replies.png" />

What TwitchSentry answers when a moderator uses a [chat command](#chat-commands): confirmations, what `!tsundo` says, rejections and replies to input it could not read. The placeholders each reply accepts are listed under its box.

## Discord Alerts

One switch per thing that can happen, not per module: what you are deciding is how much you want to
hear, and a permit being granted happens hundreds of times more often than one being revoked.
Twenty-nine of them, grouped by where the alert comes from; the Word Filter has its own group,
so its removals do not ride on the Chat Moderation switches.

Every alert says what happened in one word, the same in every module: **DELETED**, **TIMEOUT**,
**BANNED**, **WARNED**, **RESTRICTED**, **BLOCKED** and so on, under a title that names the module the
way the window does (*Spam Scoring — Action Taken*). The evidence is a bulleted **Why** — *Account is
12d old, under the 30d minimum*, *78% capital letters* — rather than a comma-run of tokens. The
tokens stay in the action log and the Streamer.bot log, where they are the more useful form.

Alerts are queued and sent on a background thread, so moderation never waits on Discord. A single
alert goes out immediately; a burst arrives as one message carrying up to ten of them, which is what
keeps a raid from spending Discord's rate limit on thirty separate requests.

<img width="926" alt="Discord Alerts" src="docs/screenshots/discord-alerts.png" />

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

**Send A Test Message**, under *Test Message* at the bottom of the page, posts one message to the webhook in
the box, under the display name and avatar set there, whether Discord Alerts is on or not and without saving
first. The line beside the button says whether Discord took it, and if not, what Discord answered: *404
Unknown Webhook* is a webhook that was deleted in Discord, *401 Invalid Webhook Token* a URL that lost part of
itself on the way in.

**When Twitch says no:** an alert can read **TIMEOUT REFUSED** rather than **TIMEOUT**. Twitch answers every deletion, timeout, ban and warning with a yes or a no, and a no is reported rather than swallowed: the viewer was not touched, nothing went into the undo trail and nothing was said in chat, so the alert is the only record. The **Status Log** page carries the reason — usually a target Twitch will not let a bot touch, a message somebody else has already removed, or a missing scope on the Streamer.bot Twitch account.

**How the alerts look in Discord:** under *Webhook Appearance* on the *Discord Webhook* card there are two more fields, **Display Name** and **Avatar URL**. Discord names a new webhook itself and that name says nothing about what is posting, so these ship as `TwitchSentry-Log` and the TwitchSentry logo and ride along with every alert — you do not have to give the webhook a fancy name and a logo yourself unless you want to. Empty either box and that override is not sent at all, and whatever the webhook carries in Discord shows through instead; that is the way back. Discord refuses a display name over 80 characters, or one containing *discord* or *clyde*, and refuses the whole post along with it, so TwitchSentry drops such a name rather than lose the alert — and the window warns you when you save one.

## Windows Notifications

<img width="926" alt="Windows Notifications" src="docs/screenshots/windows-notifications.png" />

A small Windows notification in the corner of the screen, kept afterwards in Windows' notification
centre. It works while the settings window is closed, and carries TwitchSentry's icon once the window
has been opened at least once. The switch in the page's title bar turns all of them on or off; below it
is one switch per kind:

| Switch | Default | When |
|---|---|---|
| **On New Releases** | on | A new TwitchSentry release is out. Once per release; the settings window looks for one each time it opens. |
| **On Deck Button Actions** | off | A [deck button](#deck-buttons) just did something: switched a profile, a module or an exemption, test mode, Raid Protection, an undo. |
| **On Deck Button Problems** | on | A deck button could not do what it was asked, and why: a profile that no longer exists, a name that matches nothing, a `configs.json` that cannot be read. |
| **On LurkBots Found** | on | [LurkBot Filter](#lurkbot-filter) found bot accounts sitting in chat, once per round, naming them. |

Below those come the same switches as on [Discord Alerts](#discord-alerts), group for group and all off until
you switch them on. They do not need Discord Alerts at all, so the alerts can be on screen instead of, or as
well as, in a Discord channel. What one module reports within a few seconds arrives as one notification
(*Raid Protection — Action Taken (5)*, with the first viewers named), so a raid does not bury the screen.

**Show A Test Notification** sends one straight away, whatever is switched on. If nothing appears,
Windows is holding it back: check *Do Not Disturb* (*Focus Assist*) and *Settings → System →
Notifications*, where Streamer.bot has to be allowed to send notifications.
<img width="396" height="149" alt="grafik" src="https://github.com/user-attachments/assets/0dada811-9bec-43c9-8f0d-47f97886b34f" />

---

# Chat

## Message Filter

| Easy Mode | Expert Mode |
|:---:|:---:|
| ![Easy mode](docs/screenshots/message-filter.png) | ![Expert mode](docs/screenshots/message-filter-expert.png) |


Three tabs: **Checks**, **Chat Modes** and **Messages**. The checks look at how someone is chatting rather than at particular words: account age, ALL CAPS, emote spam, posting too fast or repeating yourself, and, if you switch them on, repeated words, symbol spam, walls of text, mass mentions, ASCII art and Zalgo text.

No single one of those is proof of anything on its own — people shout, people spam emotes when something good happens — so a message is only acted on when at least two of them show up together, or when one of them is the kind that is not an accident. A repeated message is decisive on its own; being new to Twitch is a risk factor that makes whatever else the message tripped count for more, never a finding by itself. Someone with a long history in your chat needs more evidence than a stranger does.

Each check has its own switch and there is no module-wide one: unticking every check is what silences it.

**Repetition Spam** holds two checks. *Repeated characters* (`aaaaaaa`, `!!!!!!!`, `NOOOOOO`) used to be part of the caps check; it has its own switch now, and an install that never saved it keeps what the caps switch gave it. A stretched letter counts once towards the caps ratio, so one held-down key is one signal, not two. *Repeated words* catches the same word or a phrase of up to three words back to back (`lol lol lol lol lol`); a wall of emotes is left to the emote check. Repeated words are off by default.

**Symbol Spam**, **Long Messages** and **Mass Mentions** are scored like caps and emotes, so a regular's single hit is discounted and *Require Two Signals* applies. All three are off by default. Symbols measure the share of punctuation and symbols in a message, leaving out emoji, emotes and whatever the ASCII art check counts; Long Messages flags anything over *Max. Characters* (300); Mass Mentions counts *different* @names (5).

**Zalgo Text** works like ASCII art: a rule rather than a score, acting on regulars too, off by default. Writing never needs more than two marks on one letter, so only the third mark onwards is counted, and *Min. Stacked Marks* (10) of them is Zalgo text.

**ASCII Art** is off by default. Switched on, it removes pictures drawn out of Braille dots (⣿⠄) or block and box characters (█▀═), which raids, bot waves and ordinary viewers all paste into chat. It counts those characters, and a message with at least *Min. Art Characters* of them (20, in Expert mode) is acted on the way *Default Action* on General Settings says; the reply is *ASCII Art Flag* on the page's Messages tab. Unlike the other checks it is a rule rather than a score, so *Require Two Signals* and the regular's discount do not apply and a regular's picture goes too. Exempted viewers and anyone with a permit stay exempt.

In expert mode every check's card also carries its **Score Hit**, the weight that check adds to a message's score. What they add up against is under *Expert Tuning — Scoring* at the bottom of the tab: *Require Two Signals*, how many messages make a viewer known or a regular, and the threshold.

**Chat Modes**, the second tab, deals with the whole chat rather than one viewer. When enough *different* people trip the filters inside the same window, a Twitch chat mode is switched on for everyone and lifted again on its own. The tab reads top to bottom:

- **Chat Modes**: the main switch, *Switch Chat Modes On Automatically*, and a sentence under it that says in plain words what the numbers below add up to.
- **When It Starts**: how many *Violations*, from at least how many different *Viewers*, *Within* how many seconds.
- **Modes It May Use**: *Slow Mode* with its *Seconds Between Messages* and *Always Add Slow Mode*, *Follower-Only* with how long someone must have followed, *Emote-Only* and *Sub-Only*. A mode switched off here is skipped.
- **How Long It Stays On**: *Lift After*, counted from the last violation, so the mode lasts as long as the wave.
- **What Happens**: a table with one row per kind of wave, showing which mode comes first and, with *Step Up If The Wave Continues* on, what is added if the wave keeps going. It redraws as you tick and names the modes it skips.

<img width="926" alt="Message Filter, Chat Modes tab" src="docs/screenshots/message-filter-chat-modes.png" />

The third tab, **Messages**, holds what the Message Filter says in chat, including the two chat mode notices.

## Link Filter

<img width="926" alt="Link Filter" src="docs/screenshots/link-filter.png" />

Always on. A link from a viewer who is not exempt and holds no [permit](#permit) is removed the way **Default Action** on General Settings says, unless this page allows it. Two tabs: **Settings** and **Messages**.

**Whitelisted Domains**, under *Allowed Domains*, is your own list of addresses that always pass. A whitelist entry without a trailing `/*` is an exact match: `twitch.tv/yourname` allows that one link and nothing nested under it, so anything below it needs `twitch.tv/yourname/*`.

**Always Allowed**, the card below it, is the shortcut for the entry most people write first: switches that let your own clips and videos through for everybody, without a permit and without a whitelist line. The channel names are read from whichever accounts Streamer.bot is signed in to, so a rename follows along.

The switches come in two groups, because a link can only be checked against your channel when your channel's name is in it:

- **Only Your Channel** — your Twitch clips (`twitch.tv/yourchannel/clip/…`), your Twitch channel page (`twitch.tv/yourchannel`, and the pages under it), your YouTube channel page (`youtube.com/@yourhandle`), your Kick clips and your Kick VODs. The address names your channel, so a clip or video of anybody else's is still judged by the Link Filter. A platform Streamer.bot is not signed in to matches nothing here.
- **Any Channel** — the same shapes with the channel left open, each on its own switch: Twitch clips (`twitch.tv/anychannel/clip/…`, and `clips.twitch.tv/…` for the same clip by a shorter address), Twitch VOD links (`twitch.tv/videos/…`, which is what Twitch's own Share button gives for a VOD), YouTube videos, Shorts, live streams and clips, and Kick VOD links (`kick.com/video/…`). Ticking one allows that kind of link for every channel on the platform, not only yours. Most of these addresses name no channel at all; a clip address always names one, and that switch simply does not read it.

They sit here rather than on the Permit page because they are not a permit: they keep working with Permit switched off entirely.

**Check Every Posted Link**, the scan of every link with VirusTotal, is on the [Check Link](#check-link) page.

## Word Filter

<img width="926" alt="Word Filter" src="docs/screenshots/word-filter.png" />

Your own list of words and phrases that are not welcome in your chat. It is its own action, **[TS] - Word Filter**, with the triggers *Twitch > Chat > Chat Message*, *Twitch > Moderation > Blocked Terms Added* and *Blocked Terms Deleted*, and the `!nuke` command.

- **A word or phrase matches as a whole word**, whatever its case and accents: `cheap` does not catch `cheaper`. A `*` stands for any letters (`*cheap*`), and an entry written as `/pattern/` is a regular expression.
- **Catch Disguised Words** (on by default) also reads every message with its disguises off: lookalike letters from other alphabets, digits and signs standing in for letters (`h4te`, `$pam`), letters spaced out (`h a t e`, `h.a.t.e`) and letters held down (`haaaate`). Digits stuck on to dodge the list (`hate123`) do not hide a word either.
- **There is no score.** A match is acted on whoever sends it, except moderators, the broadcaster and the viewers exempted on General Settings. **Page Action** (Delete, Timeout or Ban) applies to every entry set to *Page Action*; **Timeout Duration** sets the length of every timeout, an entry's own *Timeout* too. With Twitch Warn on, a deletion is handed over like the other filters'.
- **Each entry** can be marked **Block On Twitch**, have its own action, and run out on its own after an hour, a day or a week, which is what a spoiler or today's drama wants.
- **Twitch's Blocked Terms**: Twitch's own list stops a message before anyone sees it, even while Streamer.bot is closed, but such a message never reaches TwitchSentry either. Entries marked *Block On Twitch* are put on Twitch's list and taken off again when you unmark, remove or let them run out. What a moderator adds on Twitch is taken in; what a moderator deletes there goes from here too if it came from Twitch, and only loses its mark if it was made here. The two lists are compared after every save, every quarter of an hour while chat runs, and at once through the two Blocked Terms triggers. A failed read of Twitch's list never empties either side.
- **`!nuke <word or phrase> [seconds]`** reaches back through the last stretch of chat (60 seconds unless the command says, 600 at most) and removes every matching message, by default with a timeout for each sender. The phrase then stays on the list for *Keep Blocking* minutes. One `!tsundo` takes the whole nuke back, `!tsundo @name` one viewer's part of it.
- The list is never posted in chat: `!bwlist` only says how many entries there are, unless it is whispered.

---

# Spam

## Spam Scoring

| Easy Mode | Expert Mode |
|:---:|:---:|
| ![Easy mode](docs/screenshots/spam-scoring.png) | ![Expert mode](docs/screenshots/spam-scoring-expert.png) |

This does not judge a message by how many red flags it trips. It asks whether the message is built like an advert. An advert has parts: somewhere to go (**Destination**), something being sold (**Offer**), a way to redeem it (**Instrument**), the random `@handle` a spam bot signs with (**Tag**), and wording this channel has seen from spam before (**Signature**).

One part on its own is a coincidence — plenty of ordinary messages have one. Two parts together is an advert. That is what the sensitivity slider controls, and why false positives are rare: no single keyword is ever the whole verdict.

**Fancy fonts change nothing.** Spam is often written in letters from other alphabets that only look Latin: Cherokee (`ᏙᏆᎬᎳᎬᎡᏚ`), Lisu, Greek, Cyrillic, Canadian syllabics, small capitals, boxed or circled letters, letters with strokes or stacked accents, or plain words padded with invisible characters. Before any list is read, all of that is read back as the letters it shows, and the Spam Learner and Raid Protection read messages the same way. Disguised letters that reveal wording from your lists are deliberate evasion and make that evidence decisive; harmless words in such a font stay harmless. A phrase on your lists also finds its words joined by underscores, and a Telegram bot named next to "tg" or "telegram" in a message selling viewers or followers is a hand-off, the same part of an advert as "add me on Discord".

**Conversation Scam** is tracked separately, because it is a different animal from the bot that drops one advert and leaves. This account chats with you: it asks how long you have been streaming, says your channel looks a little empty, mentions that a logo or a VTuber model would fix that, and only then tells you it sells exactly that. No single message it sends is spam — the tell is the order. Four stages are tracked per account inside a window, they only count moving forwards, and it only acts once an account has walked them in order and ended on the offer. Being a familiar face does not buy an exemption here — it raises the bar to all four stages instead of three. Sitting in a channel for hours is how these accounts earn their standing in the first place.

## Known Patterns

<img width="926" alt="Known Patterns" src="docs/screenshots/known-patterns.png" />

The actual active rules every module checks against — `spam.json`, editable in place. Spam domains, keywords, strong keywords, domain endings, custom patterns and voucher-code patterns, plus the four **conversation beats** the scam detector matches on. Add your own here, or approve what the Learner suggests. Don't forget **Save**.

**New entries arrive on their own.** When a new viewer-selling site starts circulating, it is added once to the [spam feed](https://github.com/aaskjer/TwitchSentry/blob/main/Feed/README.md), and within a few hours it shows up in these lists — no new version to import. Each entry arrives exactly once: delete one here and it stays deleted. The feed only ever adds to the plain-text lists; custom patterns and voucher patterns are yours alone. **Receive New Entries** at the top of the page switches it off.

**Share what you found.** *Share With Other Streamers...* on this page, or *Share With Others...* in the ☰ menu, offers the entries in your lists that TwitchSentry does not have yet: nothing the feed already carries, and nothing a version shipped as a default. Each list is headed with what an entry in it does, and *How this works* above the list explains the rest, including why a conversation stage can show up on its own. Tick the ones worth passing on and it opens a GitHub form with them filled in; you press Submit there yourself, and once an entry holds up it reaches everyone else through the feed. The same dialog shares your saved settings as a profile, or a complete translation file. Nothing is sent from the window, and only the entries go along — never a chat message or a name. A single translated text that reads badly is a ticket rather than a share: *Report...* in the ☰ menu, *A translation*.

A shared profile is too long for the link, so it goes onto your clipboard to paste into the form. If Windows will not hand the clipboard over (it happens in Remote Desktop sessions), the form opens anyway and the dialog shows the profile, with *Copy Again* beside it. Once you submit, the repository checks the profile the way the window checks an import, and if it holds up it is stored on the [`profiles` branch](https://github.com/aaskjer/TwitchSentry/tree/profiles) and the ticket is closed. There is no pull request and nobody has to accept it, so it doubles as a backup: download the file from there and put it into `Settings/Profiles`, on this PC or any other.

## Spam Learner

<img width="926" alt="Spam Learner" src="docs/screenshots/spam-learner.png" />

Watches what actually got removed and works out which words, phrases and domain endings keep showing up in it, scoring each candidate by how much more often it appears in spam than in ordinary chat. New finds start as suggestions for you to review; they are promoted into the real rule list only once they have built a track record — either because you approve them, or automatically if **Auto Promote Trusted Rules** is on.

Only *content* violations feed it. The fact that somebody typed too fast tells you nothing about which of their words were spam, so behavioural violations contribute none. On top of that sit an **Ignore Terms** list, automatic protection for your own account names, a denylist for major brands, and the clean-chat sample described below.

## Suggestions

<img width="926" alt="Suggestions" src="docs/screenshots/suggestions.png" />

Everything the Learner has proposed but not applied. Read the **Would hit** column first: that is how many messages from your own clean chat log the rule would have matched. Zero is what you want, and anything above zero is never auto-promoted. **Users** counts how many different people posted it, so one spammer repeating himself counts once; **Discrim.** is how much more often it shows up in spam than in ordinary chat.

**Probation** means a candidate is still building a record; **trusted** means it is proven enough to be auto-promoted, if you have turned that on. **Clear File** wipes the pending list and leaves your active rules alone.

---

# Bots & Raids

## Raid Protection

| Easy Mode | Expert Mode |
|:---:|:---:|
| ![Easy mode](docs/screenshots/raid-protection.png) | ![Expert mode](docs/screenshots/raid-protection-expert.png) |

The same idea as `Message Filter` but stricter and only armed for a limited window right after an incoming raid. Plus: **swarm detection**, which spots several different accounts posting near-identical messages at once which then gets scored against bot patterns.
Three tabs: **Detection** (sensitivity, the **Action** for a message it catches, what counts as a raid worth stopping and, in expert mode, the raid window, velocity, duplicate and swarm numbers), **Chat Modes** and **Messages**.

**Chat Modes** works like the [Message Filter's](#message-filter), with three differences: **When It Starts** is one switch, *As Soon As A Raid Arrives* (otherwise the first mode goes on when a raid message crosses the score threshold); **Shield Mode** has its own card; and everything is lifted when the raid window ends rather than after a set time. A second wave of the same pattern moves up a step instead of re-picking the mode that is already running.

<img width="926" alt="Raid Protection, Chat Modes tab" src="docs/screenshots/raid-protection-chat-modes.png" />

**Pause Queues**, at the bottom of the Chat Modes tab, holds Streamer.bot action queues while a harmful raid is being stopped, so its spam never
reaches text-to-speech or alerts. Tick **Pause Queues During A Raid** and enter the queue names, one per
line, exactly as Streamer.bot lists them under *Action Queues*. They are paused the first time a raid
message crosses the score threshold, or when Raid Protection is armed from a deck button or the panic
button; a friendly raid that never crosses it leaves every queue running. When the raid window ends they
run again, with what piled up meanwhile, or without it when **Clear Queues On Resume** is ticked. Only
queues TwitchSentry paused are resumed, and test mode pauses nothing. Never name a queue TwitchSentry's own
actions run in.

## Follow Protection

| Easy Mode | Expert Mode |
|:---:|:---:|
| ![Easy mode](docs/screenshots/follow-protection.png) | ![Expert mode](docs/screenshots/follow-protection-expert.png) |

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
- Its one chat message, **Follower Blocked**, is on the page's Messages tab and empty by default: the account it blocked is not there to read it.

## LurkBot Filter

<img width="926" alt="LurkBot Filter" src="docs/screenshots/lurkbot-filter.png" />

**Off by default, and on Report Only when switched on.** Bot networks keep accounts sitting in thousands
of channels without ever writing, most likely to log the chat. They are made in batches: the same day, the
same short name pattern, no picture, no bio.

- It runs as its own action, **`LurkBotFilter`**, on the trigger *Twitch → General → Present Viewers*.
  Tick **Live Update** under *Platforms → Twitch → Settings → Present Viewers*: without it Streamer.bot
  only lists viewers who wrote recently, and a LurkBot never writes.
- **Which Accounts Are Looked Up**: only names of exactly **Letters In The Name** letters followed by
  **Digits At The End** digits (5 and 2). Moderators, the broadcaster and the viewers exempted on General
  Settings are skipped. Each account is looked up on Twitch once, at most **Lookups Per Round** (20) per round.
- **When An Account Counts As A Bot**: made on one of the **Known Bot Days** (`2024-05-05`), or on the same
  day as at least **Same Day Accounts** (3) other accounts of that name shape. Accounts are remembered for
  30 days, so a group does not have to sit in chat at the same time. **Bare Profiles Only** (on) judges
  only accounts with Twitch's default picture, no bio, and neither affiliate nor partner.
- **Report Only** writes each account to the Action Log and **Found Accounts**, and to Discord and a Windows
  notification if those are on. **Ban** bans each account once; one [`!tsundo`](#chat-commands) lifts the whole
  round, `!tsundo @name` one account, and an account let back in is never banned again by LurkBot Filter.
- A real viewer can be caught: somebody whose name happens to fit, who never set a picture or a bio, and who
  made the account on such a day. Watch Report Only for a while before you switch to Ban.
- Test mode bans nothing and says in chat who would have been banned.

## Shared Bot List

<img width="926" alt="Shared Bot List" src="docs/screenshots/shared-bot-list.png" />

**On by default.** Every TwitchSentry install reports the bots it is sure of to a shared, public list on
GitHub ([the `botlist` branch](https://github.com/aaskjer/TwitchSentry/tree/botlist)), and bans what other
channels reported there.

- **What is reported**, automatically and without a switch: a decisive hit in Spam Scoring (a known spam
  domain, a strong keyword, a conversation scam) from a viewer who is not a regular; a LurkBot Filter verdict
  with the name shape, a bot day and a bare profile together; an account in one of Follow Protection's follow
  waves; and an account in a Raid Protection swarm whose wording is on a spam list. Only the account is sent,
  never a chat message or which channel reported it. Test mode reports nothing, and lifting a ban or a
  timeout on Twitch takes the report back.
- **What is banned**: an account at least two channels reported, from the lists switched on: **Spam Bots**,
  **LurkBots** and **Bot Waves** (all on). Each account is looked up on Twitch first; moderators, VIPs,
  partners, affiliates, the bot account and the viewers exempted on General Settings are never banned. Up to
  30 accounts are banned per round, so a long list is worked through over hours rather than in one burst.
- These bans are not on the [`!tsundo`](#chat-commands) list, so an undo always means a moderator's own
  action. To let an account back in, unban it on Twitch: the list never bans it here again.
- **Listed by mistake?** Anyone can ask for an account to come off the list with *Report...* in the ☰ menu. It comes
  off at once, every install that banned it through the list lifts that ban by itself, and the channels that
  reported it are not counted for it again.
- **Status** says which version of the list was read last and when, how many accounts on it are confirmed,
  how many were banned here, how many wait and how many bans were lifted after a removal, and how many
  accounts this install reported in the last 30 days.
- Test mode bans and lifts nothing.

## Offline Protection

<img width="926" alt="Offline Protection" src="docs/screenshots/offline-protection.png" />

**Off by default.** Nothing in TwitchSentry runs once Streamer.bot is closed, but Twitch keeps chat modes on
by itself. So the moment Twitch reports the stream offline, the modes ticked here go on: **Emote-Only**
(ticked by default), **Sub-Only**, **Follower-Only** with its follow age, **Slow Mode** with its delay, and
**Shield Mode**. When the stream goes live again, **Lift When The Stream Goes Live** switches off exactly
what this page switched on, and nothing else.

- It runs as its own action, **`OfflineProtection`**, with two triggers: *Twitch → Stream Offline* and
  *Twitch → Stream Online*. Streamer.bot has to be running when the stream ends.
- With [Discord Alerts](#discord-alerts) on, **On Chat Modes Switched** posts *Chat Modes On* as the stream ends
  and *Chat Modes Lifted* as it goes live, naming any mode Twitch would not switch.
- What it switched on is remembered across a restart of Streamer.bot, so going live lifts it even then.
- A Shield Mode that was already on is left alone, and never switched off when you go live.
- Leave a mode unticked here if your channel keeps it on all the time: going live switches off whatever
  this page switched on.
- Test mode switches nothing on.

---

# Moderation

These are off by default, except Permit. Each is genuinely optional — the chat filters and spam scoring are the core, and everything here is something you may or may not want.

## AutoMod

<img width="926" alt="AutoMod" src="docs/screenshots/automod.png" />

**Off by default**. Twitch's own AutoMod holds suspicious messages back and waits for a moderator to approve or deny each one. This answers them for you, by level and by category. Leave **AutoMod Categories** empty to act on everything Twitch holds, or list only the categories you care about.

**Ban Evasion** (off by default, needs the trigger *Twitch > Moderation > Suspicious User Message*) acts on the rating Twitch gives an account it compares with the ones banned here before: *likely* only, or *possible* too. Twitch's own Suspicious User Controls can already monitor or restrict such accounts; this adds a ban if you want one, the Action Log, Discord and `!tsundo`. Each account is acted on once a day.

**Unban Requests** (on, and working with the AutoMod module switched off too, needs the trigger *Twitch > Moderation > Unban Request Created*) posts every unban request to Discord with what TwitchSentry's logs say about the account beside it: which module acted, when, why and on which message, archived months included. The decision is still made in Twitch's moderator view.

## Twitch Warn

<img width="926" alt="Twitch Warn" src="docs/screenshots/twitch-warn.png" />

A warned viewer has to read and click through a warning screen before they can chat again, and Twitch keeps the count in their moderation history. **Warning Escalation** adds steps on top: warns accumulate, the last one before the threshold is a final warning, and the violation after that becomes a timeout, a ban or a **restriction**. A restricted viewer stays in chat, but everything they write from then on reaches only the moderators. Counts reset on their own after a quiet period.

Two switches go with it:

- **Monitor From The Final Warning** flags the viewer as monitored on Twitch along with the final warning. They chat as before, and the moderators see a marker on every message they send, so whoever is watching knows who is one violation away.
- **Count Warnings From Moderators** counts a warning a moderator gives in Twitch — `/warn`, or the warning on the viewer's card — towards the same ladder. It needs the trigger **Twitch > Moderation > Warned User** on the TwitchWarn action; the settings window says so while that trigger has never fired. A moderator's warning never escalates by itself, and TwitchSentry's own warnings, which Twitch reports through the same trigger, are not counted twice.

A restriction and a monitoring are both lifted with `!tsundo`, from a deck button, or on the viewer's card in Twitch.

## Permit

<img width="926" alt="Permit" src="docs/screenshots/permit.png" />

A time-limited exception for a viewer, so they can post a link without it getting deleted. `!permit @user [seconds]` grants one, `!endpermit @user` ends it, `!endpermit` on its own ends every active permit. Several people can hold one at the same time, each with its own countdown; a permit that is already running is never extended. They are deliberately forgotten on restart.
**Max Permit Duration Seconds** caps whatever a moderator types, with a hard ceiling of 24 hours.
A permit can also come from a [deck button](#deck-buttons) or the [OBS dock](#the-obs-dock), which lists the links the Link Filter removed with a **Grant Permit** beside each.
Viewers can also redeem a permit themselves through Channel Points, if **Allow Self-Permit** is on. **When A Self-Permit Is Redeemed** decides what happens next: **Grant It Right Away**, or **Wait For A Deck Button**, where the request waits in the [OBS dock](#the-obs-dock)'s Permit list (or for a `tsPermit` key) until you let it through or refuse it and the points go back. Chat hears *Self-Permit Waiting* meanwhile. Set that reward up with **Skip Reward Requests Queue** turned **off** — that is what lets TwitchSentry give the points back when a redemption cannot become a permit. A reward that skips the queue is spent the moment it is redeemed, and Twitch will not allow a refund.

## Check Link

<img width="926" alt="Check Link" src="docs/screenshots/check-link.png" />


Two jobs: Anyone can scan a URL on demand with `!checklink <url>`. The second feature adds a scan on top of the ordinary link rule and automatically scans any incoming link in chat.
Uses VirusTotal (required, free key) and optionally IPQualityScore for a second opinion. IPQS rates a link from 0 to 100; the default threshold is 75, with a stricter one for domains it also reports as recently registered, since a brand-new throwaway domain is a phishing classic.

## Voting

<img width="926" alt="Voting" src="docs/screenshots/voting.png" />

Lets chat decide! `!vote @user` starts or joins a vote, and enough *unique* voters inside the time window time that person out — or ban them, if you allow it. The window running out resets the vote. Subscribers and VIPs can be exempted, there are separate exclusion lists for users and Streamer.bot groups, and **everyone above VIP is permanently unvotable!**

---

# Messages

Everything TwitchSentry says in chat is on the **Messages** tab of the module that says it, with the placeholders each message accepts listed under the box. Its answers to chat commands are on [Command Replies](#command-replies), under Setup. Nothing here is translated for you — this is your bot's voice, your wording and your language, so a German channel picks Deutsch for the window *and* writes these in German.

| Command Replies | Message Filter → Messages | Raid Protection → Messages |
|:---:|:---:|:---:|
| ![Command Replies](docs/screenshots/command-replies.png) | ![Message Filter → Messages](docs/screenshots/message-filter-messages.png) | ![Raid Protection → Messages](docs/screenshots/raid-protection-messages.png) |
| Link Filter → Messages | Spam Scoring → Messages | Spam Learner → Messages |
| ![Link Filter → Messages](docs/screenshots/link-filter-messages.png) | ![Spam Scoring → Messages](docs/screenshots/spam-scoring-messages.png) | ![Spam Learner → Messages](docs/screenshots/spam-learner-messages.png) |
| AutoMod → Messages | Twitch Warn → Messages | Permit → Messages |
| ![AutoMod → Messages](docs/screenshots/automod-messages.png) | ![Twitch Warn → Messages](docs/screenshots/twitch-warn-messages.png) | ![Permit → Messages](docs/screenshots/permit-messages.png) |
| Check Link → Messages | Voting → Messages | Word Filter → Messages |
| ![Check Link → Messages](docs/screenshots/check-link-messages.png) | ![Voting → Messages](docs/screenshots/voting-messages.png) | ![Word Filter → Messages](docs/screenshots/word-filter-messages.png) |
| Follow Protection → Messages |  |  |
| ![Follow Protection → Messages](docs/screenshots/follow-protection-messages.png) |  |  |

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

<img width="926" alt="Action Log" src="docs/screenshots/action-log.png" />

Every action involving a viewer this month, filterable by module and by result, with the raw line underneath. This is the page for *what happened*.

Each month starts a new `action-log.txt` (and a new `violation-log.txt`). The month before is moved aside in the same `Logs` folder as `action-log-2026-09.txt` and so on, and nothing is deleted. The Home counters still count the older months, and the Spam Learner's History Lines reach back into them, so a new month does not start its memory from nothing.

## Status Log

<img width="926" alt="Status Log" src="docs/screenshots/status-log.png" />

What TwitchSentry has been saying about *itself*, pulled out of the Streamer.bot log: an API key still on its placeholder, a download that failed, an action Twitch refused. None of that is announced in chat, so this is the page to open when something quietly did not happen.

## Violation Log

<img width="926" alt="Violation Log" src="docs/screenshots/violation-log.png" />

The **Violation Log** is every message that was acted on this month, exactly as it was posted — the page to open when you disagree with a removal. Earlier months are in `violation-log-2026-09.txt` and so on, beside it in the `Logs` folder.

## Clean Chat Log

<img width="926" alt="Clean Chat Log" src="docs/screenshots/clean-chat-log.png" />

The **Clean Chat Log** is the opposite of the violation log: a sample of ordinary chat that was deliberately left alone, roughly one message in ten. The Spam Learner measures its candidates against it, which is what stops an everyday word from becoming a rule. Both pages have a search box and a per-account filter, and both show the full line under the list, because chat messages are usually wider than the row.

---

# Help

## Manual

<img width="926" alt="Manual" src="docs/screenshots/manual.png" />

The longer explanation behind every card with a **?** in its corner, page by page in the order of the sidebar, and a list of every [chat command](#chat-commands) under *Command Replies*. A **?** opens the Manual at its card's section and lights it up for a moment; **← Back to …** at the top takes you back to the page you came from, scrolled to where you left it. Opened from the sidebar or from Home, the Manual has no back button.

The cards themselves stay short: an explanation of a sentence or two lives only in the Manual, a longer one keeps a short version under the card's *How this works*. Installing TwitchSentry, the deck buttons and where the files live are covered only here, in the online manual, which the Manual page links to.

## Backup & Restore

<img width="926" alt="Backup & Restore" src="docs/screenshots/backup-restore.png" />

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

<img width="607" height="395" alt="grafik" src="https://github.com/user-attachments/assets/a7de0cf7-a274-4968-b2d0-f54963dffad3" />

A Stream Deck key, a Streamer.bot Deck button or the [OBS dock](#the-obs-dock) can do what a streamer wants
mid-stream without opening the settings window: switch profiles, switch a module, an exemption or an Always
Allowed link, change what AutoMod does with held messages, start or end test mode, arm Raid Protection,
take the last action back, or switch LurkBot Filter between reporting and banning. The action behind them is **`[TS] - Deck`**.
It works on what the other actions share — `configs.json`, the Profiles folder and Streamer.bot's globals —
so it does not matter whether the settings window is open.

## Setting up a key

A key runs `[TS] - Deck` and says in an argument what it wants:

| Argument | Example | What it does |
|---|---|---|
| `tsPanic` | `toggle` | The panic button: switches to **Under Attack** and arms Raid Protection, and pressed again puts back every setting the way it was before. `on` and `off` work too |
| `tsProfile` | `Under Attack` | Switches to that profile: `Relaxed`, `Balanced`, `Strict`, `Under Attack`, `Just Chatting`, or the name of one of your saved profiles |
| `tsModule` | `Voting off` | Switches a module on or off: `Raid Protection`, `Follow Protection`, `LurkBot Filter`, `Word Filter`, `Offline Protection`, `AutoMod`, `Twitch Warn`, `Permit`, `Check Link`, `Voting`, `Spam Learner`, `Discord Alerts` |
| `tsExempt` | `VIPs on` | Whether `Followers`, `Subscribers` or `VIPs` are left alone by the filters — *Exclude Followers*, *Exclude Subscribers* and *Exclude VIPs* on General Settings |
| `tsAllow` | `YouTube Videos on` | One of the twelve *Always Allowed* switches on General Settings: `Your Twitch Clips`, `Your Twitch Channel Page`, `Your YouTube Channel Page`, `Your Kick Clips`, `Your Kick VODs`, `Twitch Clips`, `Twitch VOD Links`, `YouTube Videos`, `YouTube Shorts`, `YouTube Live Streams`, `YouTube Clips`, `Kick VOD Links` |
| `tsAutoMod` | `allow` | What AutoMod does with held messages (*AutoMod Action*): `deny`, `allow`, or `toggle` |
| `tsLurkBot` | `ban` | What LurkBot Filter does with the bots it finds (*Action On A LurkBot*): `report`, `ban`, or `toggle` |
| `tsTestMode` | `on` | Test mode `on` for the *Test Duration* on General Settings, `off`, or `toggle` |
| `tsRaid` | `arm` | Arms Raid Protection now, without a raid, or `disarm` ends it |
| `tsUndo` | `last` | Takes back the last timeout, ban, restriction, monitoring or block, as `!tsundo` does; `@name` takes back that viewer's last one |
| `tsForget` | `@name` | Takes the last entry, or that viewer's last one, off the undo trail without asking Twitch: for something a moderator already lifted on Twitch itself |
| `tsPermit` | `last` | Grants a link permit the way `!permit` does: `last` to the newest Channel Points request waiting for a button, else to the viewer whose link the Link Filter removed most recently, `@name` to anyone. A number after it sets the seconds (`@name 120`), within *Max Permit Duration Seconds* |
| `tsPermitDeny` | `last` | Refuses the newest Channel Points request waiting for a button, or `@name`'s, and gives the points back |
| `tsPermitForget` | `last` | Takes the newest entry, or that viewer's, off the list of removed links without granting anything |
| `tsState` | `now` | Changes nothing. It only writes down again where everything stands, for the [OBS dock](#the-obs-dock) or for a key that [shows the profile](#a-key-that-shows-what-it-switched) |

The state after a module or an exemption is `on` or `off` (`an` and `aus` work too). Left out, the key
switches the setting over, which is what a plain key wants. Names ignore upper and lower case, spaces and
dashes, so `follow-protection on` is Follow Protection.

- **Stream Deck**, with the Streamer.bot plugin: an **Action** key on `[TS] - Deck`, with the argument
  under its arguments. For something that goes on and off, an **Action Switch** key with `[TS] - Deck`
  on both sides: `tsModule = Voting on` on *Toggle On* and `tsModule = Voting off` on *Toggle Off*, or
  `tsPanic = on` and `tsPanic = off` for a panic button that shows whether a panic is on.
- **Streamer.bot Deck**: a button that runs `[TS] - Deck` with the argument.
- **Anything else that runs an action** — a hotkey, a timer, a command of your own — works the same
  way. Where it cannot pass an argument itself, make a small action that first sets the argument
  (*Set Argument*) and then runs `[TS] - Deck` (*Run Action*): an action started that way gets the
  arguments of the one that started it.

**One key can do several things.** Give it more than one argument and they are carried out in the order
of the table: `tsProfile = Strict` together with `tsTestMode = on` tries a stricter profile out first. A
part that fails does not stop the rest.

**The panic button** (`tsPanic`) remembers what it changed. Pressed, it puts aside every setting Under
Attack is about to write, switches to Under Attack and arms Raid Protection. Pressed again, it puts every
one of those settings back as it was and disarms Raid Protection, so a profile of your own, or one you had
changed since, comes back as it was, not as a built-in profile. What it put aside survives a restart of
Streamer.bot. A profile picked by hand in between ends the panic, and the next press starts a new one.
With Raid Protection switched off, it only switches the profile.

## What the key tells you

A Stream Deck key shows a ✓ when everything it asked for went through and a ⚠ when something did not,
for a moment, and then goes back to its own picture. The blue lightning bolt is that picture: it is the
Streamer.bot plugin's standard icon for an *Action* key, not a warning, and it stays until you give the
key an icon of your own. A Streamer.bot Deck button shows neither mark: what it did is in the logs, in the
[OBS dock](#the-obs-dock), and in a [Windows notification](#windows-notifications) if you switch those on. Either way the Streamer.bot log and the **Status Log** page say what happened, or why not: a name that
matches nothing (the line lists what there is), a `configs.json` that cannot be read, or one from an older
TwitchSentry, which the settings window brings up to date the next time you open it and press Save.
Whatever fails writes nothing.

## A key that shows what it switched

A Stream Deck key can show the state its press left behind instead of a fixed label. Give it the argument
**`tsTitle`**:

- **`tsTitle = auto`** writes TwitchSentry's own few words: the name on the key and **On** or **Off** for a
  module or an exemption, the profile that is running for a profile key (with a `*` once a setting was
  changed since), when test mode or the raid window ends, and whom the next undo sets free.
- **Words of your own** with placeholders: `{state}` (On or Off, in the window's language), `{state:LIVE|OFF}`
  (your own words for on and off), `{name}` (the name on the key), `{profile}`, `{until}` (when test mode
  or the raid window ends) and `{last}` (the viewer the next undo sets free). `\n` starts a new line, as in
  `{name}\n{state:ON|OFF}`.

**`tsColor`** paints the key as well: `auto` is green for on, red for an armed Raid Protection, amber for
test mode and dark grey for off; `#1E7B34|#2B2B2B` gives colours of your own for on and off, and one colour
paints it the same either way. It replaces the key's background, so leave it out on a key with an icon of
its own.

Leave the key's title empty in the Stream Deck software: a title typed there is not written over. The
Streamer.bot plugin has a title field of its own (since its version 1.1.0), and that is the one TwitchSentry
writes into.

An **Action Switch** key needs neither argument to stay honest: after a press it is set to the side that is
true. A press that failed flips it back, and a module switched in the settings window meanwhile is shown
the right way round again. A key shows the new state when it is pressed; to have a pure status key, give it
`tsState` and `tsTitle` only, and a press brings its title up to date without changing anything.

## The OBS dock

<img width="462" height="658" alt="grafik" src="https://github.com/user-attachments/assets/ab1f7797-d43f-4758-8fde-02c4a8cd15aa" />

The same buttons inside OBS. **☰ → Set Up OBS Dock** in the settings window writes the dock's page into
the TwitchSentry folder (`Dock\TwitchSentry-Dock.html`) and puts its address on the clipboard. In OBS, open
**Docks → Custom Browser Docks**, give the dock a name and paste the address as its URL.

The dock talks to Streamer.bot through its **WebSocket Server** (*Servers/Clients → WebSocket Server*),
which has to be running: switch on *Auto Start* there. The dock connects to `ws://127.0.0.1:8080/`,
Streamer.bot's default. Another address, and the password when *Authentication* is on, go under ⚙ in the
dock, which keeps them in OBS's own browser storage on this PC. That is also where you pick the action it
runs, `[TS] - Deck` unless yours has another name.

- **Profile** at the top: the one running, marked when a setting was changed since.
- **Under Attack + Arm Raid Protection**: the [panic button](#setting-up-a-key). While a panic is on it
  turns red and reads **End Panic**, with the profile it goes back to beneath.
- **Six buttons of your own**: the four built-in profiles besides Under Attack, then **Test Mode** and
  **Raid Protection**, until you change them. ✎ at the top sets each one to a profile (built-in or saved),
  a module, an exemption, an Always Allowed switch, **AutoMod Action**, **LurkBot Action**, **Test Mode**, **Raid Protection**,
  **Undo** or **Grant Permit**, with a label and a colour of your own if you like. The profile running, and a switch that is on,
  are lit; Test Mode and Raid Protection show the time they have left. The dock keeps them in OBS's own
  browser storage, so each dock has its own.
- **Modules** (with **AutoMod Action**, Deny or Allow, and **LurkBot Action**, Report Only or Ban, each on a
  rail under its module and faded while that module is off), **Exemptions**, **Always Allowed** and **Recent
  Actions** fold away with a click on their heading, and the dock remembers which are folded. Every switch
  shows its state, and a click flips it; Recent Actions are the newest five entries on the undo trail, each
  with an **Undo** of its own and a **✕** that takes it off the list without asking Twitch. An entry
  drops off by itself when a moderator unbans that viewer or lifts the timeout on Twitch.
- **Permit**: the link permits running now, with the time they have left, then the Channel Points requests
  waiting for a button (**Grant Permit** lets one through, **✕** refuses it and gives the points back), then the newest five
  links the Link Filter removed from viewers without one, each with **Grant Permit** and a **✕** that takes it
  off the list. Grant Permit runs the Permit action, so chat, Discord and the Action Log hear of it as they do of
  `!permit`, for the duration set on the Permit page; the viewer's removed links leave the list with it.
- What a press did, for a moment at the bottom edge, from a Stream Deck key or a Streamer.bot Deck button
  as well.

Every button runs `[TS] - Deck` with the arguments a key would pass, so the dock can do what a key can and
nothing more, and the log and the notifications say the same. It shows what the deck action writes after
every press; a Save in the settings window, a raid that arms Raid Protection and test mode started from the
☰ menu reach it by themselves.

The settings window writes the page again whenever it opens, so it keeps up with TwitchSentry's version and
with the window's language; OBS shows the new one the next time it loads the dock. The page is an ordinary
web page, and opened in a browser on the same PC it works the same way.

## Notes on each

- **Profiles** are written exactly the way picking one in the Profiles dialog writes them, through the
  same filter, so a saved profile cannot bring a webhook URL or somebody else's whitelist in this way
  either. The English name always works. The name the window shows in your language works too, but only
  while the window stays in that language, so the English one is the safer label for a key: the Profiles
  dialog lists them under *Switch From A Deck*, with your language's name beside each.
- **Modules and exemptions** are the master switch at the top of a module's page and the three exemptions
  on General Settings, written the same way the window writes them. The Link Filter, Spam Scoring and the
  Message Filter have no switch, by design, so a key cannot switch them off either.
- **Always Allowed** and **AutoMod Action** are the same switches as on General Settings and the AutoMod
  page. AutoMod's answer can be changed while the AutoMod module is off; it applies once it is on.
- **LurkBot Action** is *Action On A LurkBot* on the LurkBot Filter page, and works the same way.
- **Test mode** is the same as the one in the ☰ menu: it ends by itself when its time is up.
- **Arming Raid Protection** does what an incoming raid does: the raid window, plus the chat modes and
  Shield Mode where *As Soon As A Raid Arrives* and *Shield Mode On Raid* are on. It is for a wave of accounts
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
| `!bwadd <word> [2h] [twitch] [delete\|timeout\|ban]` / `!bwremove` / `!bwlist` | Blocked Words on the Word Filter page. `!bwlist` says only how many there are, unless whispered |
| `!nuke <phrase> [seconds]` | Removes every message with that phrase from the last stretch of chat, by default with a timeout for each sender |
| `!tsundo [@user]` | Takes back the last timeout, ban, restriction, monitoring, follow block or whole nuke (or that viewer's last one) |

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
