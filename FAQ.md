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
Some modules do. Link scanning such as VirusTotal need a internet connection to check your input against their own database, depending on what you enable.
The settings action also check occasionally for updates and inform users if a new TwitchSentry update is found.
Basic moderation and config-driven filtering still work without those optional online features.

### Can I customize the chat messages it sends?
Yes. Most moderation replies, warnings, permit messages, voting messages, and scan responses are configurable in the message files.

### Will it delete every suspicious message?
Not necessarily. You choose the strictness and the action: delete, timeout or ban.

### Can I review what it blocked?
Yes. The project includes logging support, including action logs and violation logs, so you can review what was detected and how it was handled.
