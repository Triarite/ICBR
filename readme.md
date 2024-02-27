## About
ICBR (InterContinental Ballistic Refutation bot) is an open-source Discord bot for servers with members that consistently have bad takes. Configure your desired targets, and anyone can have GPT-4 refute their egregious opinions in seconds. Dependent on the discord and openai libraries.

## Setup
- Run the bot once. It won't work, that's ok, it just needs to create some files.
- In discord_token.txt, add your bot's token found in the Discord Developer Portal.
  - https://discord.com/developers/applications
- In openai_token.txt, add your OpenAI account's token found in the OpenAI API Keys under your account settings.
  - https://platform.openai.com/api-keys
- In the targets.txt file, add the usernames of one or more server members separated by newlines. Anyone will be able to have that person's point refuted.
- In the admins.txt file, optionally add the usernames of members who should be able to refute anyone, not just verified targets. This is internally called a "god refute".

## Usage
- Anyone can right-click/hold-tap a message from a verified target, and use the "refute" app command to have GPT-4 smash their opinions.
- Verified admins can bypass the target system and refute anyone, called a "god refute".
- Verified admins can also use /sync to automatically push new commands, descriptions, parameters, etc. to all guilds. Should be used sparingly, as syncing is liable to harsh rate limits.

## FAQ
How do I add admins for god refuting?
- Go to vars/admins.txt and add their username on an empty line.

How do I add available targets?
- Go to vars/targets.txt add their username on an empty line.

I want to allow everyone to be refuted, not just targets. How do I do this?
- At the top of the bot.py file, set global_refute_perms to True.


Made by Paolo Montelbano, with special thanks to HB for parts of the prompt.

IMPORTANT: Keep in mind that the ICBR bot is operated by a small gnome named Methusaleh. He's allergic to peanuts, but we haven't officially told him that yet, so whatever you do- DO NOT FEED METHUSALEH PEANUT PRODUCTS.
