import discord
import time

# Read token from file
with open ("token.txt", "r") as file:
    bot_token = file.read().strip() # removeds any whitespace


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('!powerdown'):
        await message.channel.send('Bot shutting down')
        await client.close()


client.run(bot_token)
