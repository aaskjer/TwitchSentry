# Import of TwitchSentry

<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/c4a4960b-9c2f-4ce9-b24f-abb0f7407926" /></p>
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/3acc30c6-9728-4eba-b68e-77d13163bedb" /></p>

Boot up your copy of streamer.bot and click on **Import**. Drag the `TwitchSentry.sb` file into the new popup window like in the screenshot above.
Click on `Yes/Ok` on the following popup messages to succesfully import the project.

<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/823a293d-bc95-45f2-a11f-1ef2048f611f" /></p>

Like you see in the picture, enable all commands under `Commands` in streamer.bot.

---

# Initial Setup
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/c56165e8-798f-4e79-b105-fd13d1e66f1b" /></p>

After the import is done, go to the `[TS] - Settings` action and right-click on `Test` and then on `Test Trigger` to open up the settings GUI of **TwitchSentry**.
(this may take a second on first startup)

---

# Tab Explanations

## General 
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/5ed36086-e75d-471a-a7af-4514013232be" /></p>

Adjust as you like, the default settings should be a good start.
Note: Some Actions must be toggled ON first in order to use them.

The `General` tab as the name suggests, holds settings that are used across all actions as long they doesn't offer their own solution.

## Link Filter
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/aeb7dd37-1027-4f49-af96-bf0fb878f3ba" /></p>

Pretty much straight foreward so there are not much options to adjust. 
`Link Filter` keep your chat safe from any sort of classic URLs like: "Hey, check out [streamer.bot](https://streamer.bot) it's awesome!"
It respects exemptions made in the `General` tab and allows you to change all messages related to this feature.
Also you can optionally toggle `Check Harmful Domains` as a second safeguard. This will trigger `Check Link` to run and will also scan messages from trusted users/roles so nothing can slip through.
*(If you want to use `Check Harmful Domains` you need to toggle `Use Check Link` in the `Check Link` tab under `Other Modules`)*

## Spam Filter
### Spam Filter
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/f1bd0cef-e210-4c14-bf2e-647cc7d8aa82" /></p>

`Spam Filter` detects all the typical spam messages that occure in twitch chat, such as `"Cheap viewers  streamboo .com (remove the space)  @hAhstXIb"` and other typical scam.
You can toggle some detections if there are issues or you don't want to filter that strict.
The `Score Setting` is the new mechanic behind `Spam Filter` that weight all parts of a message against a score and if the score meets your threshold a message is removed.
While some patterns can accumulate score points, others won't. This way false-positives are basically impossible as they not just rely on specific keywords but everything together need to hit the threshold

### Spam Learner
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/60168af8-15d6-4078-ab7a-d0317c1fb204" /></p>

`Spam Learner` is still a WIP Project but does work very well already. It tracks every message that was deleted for any reason and uses a weigtes TF-IDF scoring for each recognized keyword, pattern, TLD and see
if they build up a history. Currently per default `Spam Learner` won't add proven sections to the `spam.json` which is used to track down spam in `Spam Filter`, so you need to manually review the `spam-suggestion.txt`
from time to time.

### Spam Patterns
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/b03b98c0-be3c-4c8c-a83a-36b213385d25" /></p>

`Spam Patterns` let you edit the current content of `spam.json` fast and easily if you need to add/remove something quick. Just don't forget to hit `Save` ;)

## Permit
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/c66f757e-ed9a-4c94-8ff4-518dcb516594" /></p>

`Permit` is also pretty straightforeward. You or your moderators can give a time restricted permit to other users to send links in chat.
The Permit ends automatically and can be revoked manually by you or your moderators.
Always only one user per permit.
Users or groups that are already exempt do not need a permit.

Optionally, you can create a custom reward redeem in twitch, so users can redeem themselves a time restricted permit.
*(This features is considered as WIP as i'm not an affiliate)*

## Other Modules
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/07e4fa78-87da-4c74-9ad5-fcfb9cfd6788" /></p>
I decided to "hide" some Modules in this tab because they are considered as "optional" and are off by default.

### TwitchWarn
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/02cbb537-cea0-4ccf-80c4-7f30ba1d66d0" /></p>

Twitch added a feature some time ago that allows broadcasters/moderators to "warn" a user. A user that got "warned" has to wait for a couple seconds 
and can read a reason for the warn that must be accepted before the user is able to participate in the stream chat again.

**TwitchSentry** steps in right there and offers to implement escalation steps, like a "3-Strikes Rule". A User collect warns till a threashold is reached.
After exceeding the threshold, the user gets a timeout or ban, based on your settings.

### Twitch's AutoMod
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/58dfc924-c8fb-4a3f-af56-39c263721177" /></p>

Twitch has their own auto moderation feature that catches suspicious messages before they reach your chat and your or your moderators can decide what happens with them.
But sometimes there is no reason to wager the option if you allow or deny a message, that's where `AutoMod` step in and automatically deny/allow all messages that got
held back by twitch. Also messages of users that got generally restricted by twitch will be handled.

### Check Link
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/cbe23410-5411-4f06-bb51-1d3260975dd3" /></p>

`Check Link` serves two causes: It get triggered by `Link Filter` as a second filter and to check if a found message is save
and secondly, any user can test any URL with it `!checklink <url>` if Virus Total or IPQS find a reason to reconsider using the URL.
Both solutions require a registered account but are free to use.

### Voting
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/75446814-113f-48df-8658-6a004edade40" /></p>

I think one of the coolest features **TwitchSentry** has: Let your chat decive the fate of harming subjects in the chat.
Users can vote against another user with `!vote @userName` and they need a unique amount of votes within a short timeframe to either ban or timeout the target, based on your settings.
This Module offers separate lists to exempt certain groups or users from being voted. **All roles above VIP are generally excluded and unvotable.**


### Action-Log
<p align="center"><img alt="grafik" src="https://github.com/user-attachments/assets/d7156eb6-3e7f-485c-b895-893f2f2727ed" /></p>

This is your action history. All actions, that involve users, will be seen here and you can filter through all modules and instances to exactly see what has happend.

---

[Frequently Asked Questions](https://github.com/aaskjer/TwitchSentry/blob/main/FAQ.md)
