# Import of TwitchSentry

<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/c4a4960b-9c2f-4ce9-b24f-abb0f7407926" /></p>
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/3acc30c6-9728-4eba-b68e-77d13163bedb" /></p>

Boot up your copy of streamer.bot, click **Import**, drag the `TwitchSentry.sb` file into the new popup window like in the screenshot above.
Click on `Yes/Ok` on the following popup messages to succesfully import the project.

<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/823a293d-bc95-45f2-a11f-1ef2048f611f" /></p>

Like you see in the picture, enable all commands under `Commands` in streamer.bot.

---

# Initial Setup
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/c56165e8-798f-4e79-b105-fd13d1e66f1b" /></p>

After the import is done, go to the `[TS] - Settings` action, right-click on `Test` and click onto `Test Trigger` to open up the settings GUI of **TwitchSentry**.
*(this may take a second on first startup)*

---

# Tab Explanations

## General 
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/5ed36086-e75d-471a-a7af-4514013232be" /></p>

The `General` tab as the name suggests, holds settings that are used across all actions as long they doesn't offer their own implementation.
Adjust as you like, the default settings should be a good start. `Writing Action-Log` is recommended but not a must.

## Link Filter
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/aeb7dd37-1027-4f49-af96-bf0fb878f3ba" /></p>
 
`Link Filter` keep your chat safe from any sort of message, containing classic URLs like: "Hey, check out [streamer.bot](https://streamer.bot) it's awesome!"
Toggle `Check Harmful Domains` as a second safeguard. This will trigger `Check Link` to run and will also scan messages from trusted users/roles, so nothing can slip through.
*(If you want to use `Check Harmful Domains` you need to toggle `Use Check Link` in the `Check Link` tab under `Other Modules`)*

## Spam Filter
### Spam Filter
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/7661f784-1121-4ea8-a9e5-a1953a090358" /></p>

`Spam Filter` detects all the typical spam messages that occure in twitch chat, such as `Cheap viewers  streamboo .com (remove the space)  @hAhstXIb` and other typical spam.
Toggle ON/OFF some categories if you want to be less strict there.
The `Score Setting` is the new mechanic behind `Spam Filter`, that split a message in parts, weight all parts of a message against a score and if the score meets your threshold the message is removed.
While some patterns can accumulate score points, others won't. This way false-positives are basically impossible as they not just rely on specific keywords but everything together need to hit the threshold

### Spam Learner
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/663c6cda-67b8-4321-8c2a-d284fb3d618c" /></p>

`Spam Learner` is still a WIP Project but does work very well already. It tracks every message that was removed from chat and uses TF-IDF scoring for each recognized keyword, pattern, TLD, collect them
and waits if they build up a history. Currently per default `Spam Learner` requires manual review. But this can be easily down by heading over to the next tab.

### Spam Suggestions
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/1921ca64-e0fb-4481-9a98-518c94fcab1b" /></p>

`Spam Suggestions` let you review all the stuff `Spam Learner` has catched and stored. You can inspect it, add it to `Spam Pattern` and clear the file if necessary.

### Spam Patterns
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/efa4b8ac-4ed3-4093-b996-8f6c4341e579" /></p>

`Spam Patterns` let you edit the current content of `spam.json` fast and easily if you need to add/remove something quick. Just don't forget to hit `Save` ;)

## Permit
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/c66f757e-ed9a-4c94-8ff4-518dcb516594" /></p>

`Permit` allows you or your moderators to give a time restricted permit to other users to send links in chat.
The Permit ends automatically and can be revoked manually by you or your moderators. Always one user per permit only.

Optionally, you can create a custom reward redeem in twitch, so users can redeem themselves a time restricted permit.
*(This features is considered as WIP as i'm not an affiliate)*

## Other Modules
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/07e4fa78-87da-4c74-9ad5-fcfb9cfd6788" /></p>
I decided to "hide" some Modules in this tab because they are considered as "optional" and are off by default.

### TwitchWarn
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/02cbb537-cea0-4ccf-80c4-7f30ba1d66d0" /></p>

Twitch added a feature some time ago that allows broadcasters/moderators to "warn" a user. A user that got "warned" is blocked from participating your chat for 5 seconds.
Similar like during a timeout, the user sees a message and must accept the prompt befor being able to write in chat again. Every warn a user receives is tracked by twitch
and you and your moderators can see them in the users moderator history.

**TwitchSentry** goes one step further and offers to implement escalation steps, like a "3-Strikes Rule". A user collect warns till a threashold is reached.
Reaching the threshold, the user receives a "final warning". Exeeding the threshold, will result in a timeout or ban, based on your settings.

### Twitch's AutoMod
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/58dfc924-c8fb-4a3f-af56-39c263721177" /></p>

Twitch has their own auto moderation called "Twitch AutoMod", that catch and block suspicious messages before they reach your chat and only you and your moderators can see them.
Handling those messages can be tedious, that's where `AutoMod` step in and automatically deny/allow all messages that got held back by twitch.

### Check Link
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/cbe23410-5411-4f06-bb51-1d3260975dd3" /></p>

`Check Link` serves two causes: It's triggered by `Link Filter` as a second filter to check if a URL found in a message is save
and secondly, any user can test any URL with `!checklink <url>` to check if Virus Total or IPQS find a reason to reconsider using it.
*Both solutions require a registered account but are free to use.*

### Voting
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/75446814-113f-48df-8658-6a004edade40" /></p>

I think one of the coolest features **TwitchSentry** has: Let your chat decide the fate of harming subjects in the chat.
A user can start a vote against another user with `!vote @userName`. Voting requires a unique amount of voters within a short timeframe to either ban or timeout the target, based on your settings.
This Module offers separate lists to exempt certain groups or users from being voted. **All roles above VIP are generally excluded and unvotable.**


### Action-Log
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/d7156eb6-3e7f-485c-b895-893f2f2727ed" /></p>

This is your action history. All actions that involve users, will be seen here and you can filter through all modules and instances to exactly see what has happend.

---

[Frequently Asked Questions](https://github.com/aaskjer/TwitchSentry/blob/main/FAQ.md)
