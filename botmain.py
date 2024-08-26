# Version: 0.0.3
# Author: SkYri3l


import os
import sys
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from Bot_Commands import BotsCommand, handle_restart_status, change_status

# Empty variables
command_name = ''

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))  # Load the bot owner's ID

# Configure bot intents and commands
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
intents.dm_messages = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

# Function to check if the user is the bot owner
def is_bot_owner(ctx):
    return ctx.author.id == OWNER_ID

# LOADS ON BOT OPEN
@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")
    print('--' * 10)
    await handle_restart_status(bot)
    await change_status(bot)

# ADMIN COMMANDS
admin_group = app_commands.Group(name="admin", description="Admin Commands")
bot.tree.add_command(admin_group)

@bot.command()
async def sync(ctx: commands.Context) -> None:
    command_name ="Prefix Sync"
    """Sync commands"""
    BotsCommand.ctxuserid(ctx, command_name)
    if is_bot_owner(ctx):
        print('prefix Sync')
        await BotsCommand.Admin.sync2(bot, ctx)
    else:
        #CHECKS FOR PERMISSION
        await ctx.send("You do not have permission to use this command.")


@admin_group.command(name='sync', description='Sync Commands OwnerOnly')
async def sync(inter: discord.Interaction) -> None:
    command_name = "Slash Sync"
    BotsCommand.interuserid(inter, command_name)
    if inter.user.id == OWNER_ID:
        await BotsCommand.Admin.sync(bot, inter) 
    else:
        #CHECKS FOR PERMISSION
        await inter.response.send_message("You do not have permission to use this command.")

@admin_group.command(name="poweroff", description="Poweroff Bot OwnerOnly")
async def poweroff(inter: discord.Interaction) -> None:
    command_name = "Power Off Bot"
    BotsCommand.interuserid(inter, command_name)
    if inter.user.id == OWNER_ID:
        await BotsCommand.Admin.poweroff(bot, inter) 
    else:
        #CHECKS FOR PERMISSION
        await inter.response.send_message("You do not have permission to use this command.")

@admin_group.command(name="restart", description='Restart bot OwnerOnly')
async def restarting(inter: discord.Interaction) -> None:
    command_name = "restart"
    BotsCommand.interuserid(inter, command_name)
    if inter.user.id == OWNER_ID:
        await BotsCommand.Admin.bot_restart(bot, inter)
        username = inter.user.name
        user_id = inter.user.id
        print(f'User: {username}\n ID: {user_id}\n used slash command restart') 
    else:
        #CHECKS FOR PERMISSION
        await inter.response.send_message("You do not have permission to use this command.")

# DEFAULT USERS COMMANDS
@bot.tree.command(name="ping", description="Ping's bot latency")
async def ping(inter: discord.Interaction) -> None:
    command_name = "Ping"
    BotsCommand.interuserid(inter, command_name)  
    await BotsCommand.users.ping(inter, bot)
    

# Math Command Group
group = app_commands.Group(name="math", description="Math commands")
bot.tree.add_command(group)  # adds group commands into command tree

@group.command(name="add", description="Add two numbers")
async def add(inter: discord.Interaction, a: int, b: int) -> None:
    command_name = "add"
    BotsCommand.interuserid(inter, command_name)
    await BotsCommand.users.add(inter, a, b)

bot.run(TOKEN)
