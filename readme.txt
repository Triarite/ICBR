## About
ICBR (InterContinental Ballistic Refutation bot) is an open-source Discord bot for servers that have members that consistently have bad takes. Configure your desired targets, and anyone can have GPT-4 refute their egregious opinions in seconds. Dependent on the discord and openai libraries.

Setup:
- Run the bot once. It won't work, that's ok, it just needs to create some files.
- In discord_token.txt, add your bot's token found in the Discord Developer Portal.
- In openai_token.txt, add your OpenAI account's token found in the OpenAI API Keys under your account settings.

Usage:
- Anyone can reply to a message from a verified target with the //refute command to have GPT-4 smash their opinions.
- Verified admins can use the //godrefute command to bypass the target system and refute anyone.
- 

How do I add admins for //godrefute?
- Go to vars/admins.txt and add their username on an empty line.

How do I add available targets?
- Go to vars/targets.txt add their username on an empty line.


Made by Paolo Montelbano, with special thanks to HB for the prompt.

IMPORTANT: Keep in mind that the ICBR bot is operateed by a small gnome named Methusaleh. He is allergic to peanuts, but we haven't told him that yet, so whatever you do- DO NOT FEED METHUSALEH PEANUT PRODUCTS.