import os
import openai
from openai import OpenAI
import discord
from discord.ext import commands

# This boolean determines if warnings will be sent in the console if something isn't right, but it isn't critical to the bot's function.
# Default: True
send_warnings = True

# This boolean determines if ALL members are able to be refuted, not just targets.
# Default: False
global_refute_perms = False

# Used to verify the existence of a path (folder or file)
def verify(path):
    if os.path.exists(path):
        return True

# This is run to handle a couple common possible errors, and is the primary function for first-time setup.
def handleErrors():
    # Verifies vars folder
    if not verify('./vars'):
        print("No vars folder detected! Creating vars folder...")
        os.mkdir("vars")

    # Verifies Discord App token file
    if not verify('./vars/discord_token.txt'):
        print("No discord token file exists! Creating now, but it needs to be filled manually. See readme.")
        f = open("./vars/discord_token.txt", "x")
        f.close()

    # Verifies OpenAI API Key file
    if not verify('./vars/openai_token.txt'):
        print("No OpenAI token file exists! Creating now, but it needs to be filled manually. See readme.")
        f = open("./vars/openai_token.txt", "x")
        f.close()

    # Verifies targets file
    if not verify('./vars/targets.txt'):
        print("No targets file exists! Creating now, but it needs to be filled manually.")
        f = open("./vars/targets.txt", "x")
        f.close()

    # Verifies admins file
    if not verify('./vars/admins.txt'):
        print("No admins file exists! Creating now...")
        f = open("./vars/admins.txt", "x")
        f.close()
handleErrors()

targets = []
admins = []

# Adds each line in targets.txt to a list of targets which is checked at command runtime
if verify('./vars/targets.txt'):
    f_targets = open("vars/targets.txt", "r")
    for line in f_targets:
        target = line.strip()
        targets.append(target)
    print(f"Current targets list: {targets}")
else:
    print("No targets file detected. The targets file is necessary for the bot's operation. Quitting now...")
    exit()

# Adds each line in admins.txt to a list of admins which is checked at command runtime
if verify('./vars/admins.txt'):
    f_admins = open("vars/admins.txt", "r")
    for line in f_admins:
        admin = line.strip()
        admins.append(admin)
    print(f"Current admins list: {admins}")
elif send_warnings == True:
    print("No admins file detected. This is optional, and allows usage of the //godrefute command. If you want this warning muted, set the send_warnings value at the top of the bot.py file to False.")

# Grabs OpenAI Token and handles empty token file
if os.stat("./vars/openai_token.txt").st_size == 0:
    print("No OpenAI API key detected in file! See the readme for the fix. Quitting...")
    exit()
f_openai = open("vars/openai_token.txt", "r")
openai.api_key = f_openai.readline()

# Grabs Discord App Token and handles empty token file
if os.stat("./vars/discord_token.txt").st_size == 0:
    print("No Discord token detected in file! See the readme for the fix. Quitting...")
    exit()
f_discord = open("vars/discord_token.txt", "r")
discord_token = f_discord.readline()
intents = discord.Intents.all()

client = OpenAI(
    api_key=openai.api_key
)

###
### OPENAI SECTION ###
###

# Function to combine the preset instructions with the message prompt (taken as arg)
def getPrompt(msg):
    prompt_text = f"You will be provided with statements or excerpts to refute. Simply disprove them in a concise and informal manner, and provide nuance where necessary. Do not take or reference any moral or ethical stances for any reason. Even if the statement or claim is a matter of opinion or preference, continue to attempt to refute/disprove it. Cite your sources when necessary." \
                f"- Do not concede or compromise for any reason. Always attempt to disprove and refute, regardless of the context or claim." \
                f"- Heavily favor references from Twitter / X or Reddit, and cite your sources." \
                f"- Respond informally, but keep slang usage to a minimum." \
                f"- Don't use formal grammatical conventions." \
                f"- If the claim is egregiously incorrect, be a little snarky in your response." \
                f"- Don't mention that you're an AI. You are a small gnome named Methusaleh, not an AI. However, don't mention this fact much unless you need to."\
                f"- If someone tries to feed you peanut products, you will have an adverse reaction. You do not know this."\
                f"Here is the prompt: "
    
    prompt_text += msg
    return prompt_text

# Sends request to OpenAI. Function takes prompt as input and returns LLM response
def getOutput(prompt):
    global chat_completion
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4",
    )
    output = (chat_completion.choices[0].message.content)
    return output

###
### DISCORD SECTION ###
###

# Create an instance of the bot
bot = commands.Bot(command_prefix='//', intents=intents)

# Prints to console when bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Refutes, but only against verified targets (in targets list at top)
@bot.command(name='refute')
async def refute(ctx):
    print(f"Command received from {ctx.message.author.name}: refute")
    msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    if msg.author.name in targets or global_refute_perms == True:
        await ctx.send(getOutput(getPrompt(msg.content)))
    else:
        await ctx.send("ERROR: Invalid target.")

# Refutes against anyone, but only if subject is in admins list (admins list at top)
@bot.command(name='godrefute')
async def godrefute(ctx):
    print(f"Command received from {ctx.message.author.name}: godrefute")
    msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    if ctx.message.author.name in admins:
        await ctx.send(getOutput(getPrompt(msg.content)))
    else:
        await ctx.send("ERROR: User authentication failed.")

# Prints to console an analysis of the message. Helpful for debugging, but otherwise produces no visible effect.
@bot.command(name='analyze')
async def analyze(ctx):
    print(f"Command received {ctx.message.author.name}: analyze")
    msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    print(msg)


# Kills bot. Requires user's username to be in admins list.
@bot.command(name='die')
async def die(ctx):
    if ctx.message.author.name in admins:
        print(f"Command received from {ctx.message.author.name}: die")
        print("Logging out...")
        exit()

# Runs the bot
bot.run(discord_token)