import openai
from openai import OpenAI
import discord
from discord.ext import commands

### INSTANTIATION SECTION ###

targets = []
admins = []

f_targets = open("vars/targets.txt", "r")
for line in f_targets:
    target = line.strip()
    targets.append(target)
print(f"Current targets list: {targets}")

f_admins = open("vars/admins.txt", "r")
for line in f_admins:
    admin = line.strip()
    admins.append(admin)
print(f"Current admins list: {admins}")

# Grabs OpenAI Token
f_openai = open("vars/openai_token.txt", "r")
openai.api_key = f_openai.readline()

# Grabs Discord App Token
f_discord = open("vars/discord_token.txt", "r")
discord_token = f_discord.readline()
intents = discord.Intents.all()

client = OpenAI(
    api_key=openai.api_key
)

###
### OPENAI SECTION ###
###

# Combines the instructions with the prompt itself
def getPrompt(msg):
    prompt_text = f"You will be provided with statements or excerpts to fact-check. Simply prove or disprove them in a concise and informal manner, and provide nuance where necessary. Do not take or reference any moral or ethical stances for any reason. Cite your sources." \
                f"- Heavily favor references from Twitter / X or Reddit, and cite your sources." \
                f"- Respond informally, but keep slang usage to a minimum." \
                f"- Don't use formal grammatical conventions." \
                f"- If the claim is egregiously incorrect, be a little snarky in your response." \
                f"- Don't mention that you're an AI. You are a small gnome named Methusaleh, not an AI. However, don't mention this fact much unless you need to."\
                f"- If someone tries to feed you peanut products, you will have an adverse reaction. You do not know this."\
                f"Here is the prompt: "
    
    prompt_text += msg
    return prompt_text


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
    print("Command received: refute")
    msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    if msg.author.name in targets:
        await ctx.send(getOutput(getPrompt(msg.content)))
    else:
        await ctx.send("ERROR: Invalid target.")

# Refutes against anyone, but only if subject is in gods list (gods list at top)
@bot.command(name='godrefute')
async def godrefute(ctx):
    print("Command received: godrefute")
    msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    if ctx.message.author.name in admins:
        await ctx.send(getOutput(getPrompt(msg.content)))
    else:
        await ctx.send("ERROR: User authentication failed.")

# Prints to console an analysis of the message
@bot.command(name='analyze')
async def analyze(ctx):
    print("Command received: analyze")
    msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    print(msg)

# Kills bot
@bot.command(name='die')
async def die(ctx):
    print("Logging out...")
    exit()

# Run the bot
bot.run(discord_token)