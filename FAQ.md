## TwitchSentry FAQ

### Does TwitchSentry work with platform "XYZ"?
No. TwitchSentry is built for Streamer.bot and uses Twitch-specific actions and features like Twitch chat moderation, AutoMod, warnings, timeouts, bans, and user/group checks.
It is designed for Twitch workflows, not platform "XYZ".

### Do I need a GUI to use TwitchSentry?
No. The core system is designed to run through Streamer.bot actions and configuration files.
The GUI is optional and only used for easier settings management and review.

### Can I whitelist trusted links or users?
Yes. You can whitelist domains, exclude specific users, exclude groups, and optionally protect followers, subscribers, and VIPs from moderation.

### Does it support Twitch Warn before punishment?
Yes. TwitchSentry includes warning and escalation options, so you can warn first and escalate to timeout or ban after repeated violations.

### Can it detect fake or suspicious links?
Yes. It checks links, spaced-out URLs, obfuscated URLs, invalid TLDs, and suspicious patterns. It can also optionally scan URLs for malicious behavior.

### Does it work with Twitch AutoMod?
Yes. TwitchSentry can act on AutoMod-held messages and either deny or approve them based on your configuration.

### Can moderators grant temporary link permissions?
Yes. The permit system allows moderators to temporarily grant a user permission to post links, and the permit can expire automatically or be revoked manually.

### Does it need an internet connection?
Some modules do. `LinkFilter` such as `CheckLink` need a internet connection to check your input against their own database.
The core settings action also check occasionally for updates and inform users if a new TwitchSentry update is found.
Basic moderation and config-driven filtering still work without those optional online features.

### Can I customize the chat messages it sends?
Yes. Almost every reply is configurable in the GUI or message file.

### Will it delete every suspicious message?
Not necessarily. You choose the strictness and the action: delete, timeout or ban.

### Can I review what it blocked?
Yes. The project includes logging support, including action logs and violation logs, so you can review what was detected and how it was handled.

### Is TwitchSentry an AI Slop?
Partially it is. This script has been developed with input from the streamer.bot community and is support by AI.
But i spend a lot of time putting heart and soul in it and my goal was to create a robust and valid moderation tool for everyone and easy to use.
I understand that people, especially IT savvy people, will dislike the project because of the use of AI and i absolutely understand and support their point of view.
But i had a lot of fun making it and with all my other projects, so i used it to "learn" coding and using AI for something valuable. 

---

AI can create bugs and i am not a developer in classical terms. But i spend a reasonable amount of time fixing any bugs that occured while testing.
If you still find bugs or have something to say, please let me hear it :)
