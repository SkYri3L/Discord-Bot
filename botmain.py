# Verison : 0.0.2
#Author : SkYri3L

import os
import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv
from Bot_Commands import BotsCommand, handle_restart_status, change_status

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Configure bot intents and commands
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.dm_messages = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

#LOADS ON BOT OPEN
@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")
    await handle_restart_status(bot)
    await change_status(bot)


#ADMIN COMMANDS

@bot.command()
async def sync(ctx: commands.Context) -> None:
    """Sync commands"""
    await BotsCommand.Admin.sync(bot, ctx.interaction) 

@bot.tree.command(name='sync', description='Sync Commands OwnerOnly')
async def sync(inter: discord.Interaction) -> None:
    await BotsCommand.Admin.sync(bot, inter) 

@bot.tree.command(name="poweroff", description="Poweroff Bot OwnerOnly")
async def poweroff(inter: discord.Interaction) -> None:
    await BotsCommand.Admin.poweroff(bot, inter) 

@bot.tree.command(name="restart", description='Restart bot OwnerOnly')
async def restarting(inter: discord.Interaction) -> None:
    await BotsCommand.Admin.bot_restart(bot, inter) 



#DEFAULT USERS COMMANDS

@bot.tree.command(name="ping", description="Ping's bot latency")
async def ping(inter: discord.Interaction) -> None:
    await BotsCommand.users.ping(inter, bot) 





bot.run(TOKEN)
