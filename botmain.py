# Version: 0.0.3
# Author: SkYri3l

import os, sys, discord
from botlog import BotsLog
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from Bot_Commands import BotsCommand, handle_restart_status, change_status

# Empty variables
command_name = ''
Perm = ''
default = "defualt"

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

###

# ADMIN COMMANDS
admin_group = app_commands.Group(name="admin", description="Admin Commands")
bot.tree.add_command(admin_group)

#Sync Commands (prefix)
@bot.command()
async def sync(ctx: commands.Context) -> None:
    command_name ="Prefix Sync"
    """Sync commands"""
    if is_bot_owner(ctx):
        print('prefix Sync')
        await BotsCommand.Admin.sync2(bot, ctx)
        Perm = True
    else:
        await ctx.send("You do not have permission to use this command.")
        Perm = False
    BotsLog.ctxlog(ctx, command_name, Perm)

#Shows botlogs
@admin_group.command(name="showlogs", description="Show recent bot logs")
async def show_logs(inter: discord.Interaction) -> None:
    command_name = "Show Logs"
    if inter.user.id == OWNER_ID:
        embed = discord.Embed(title="Bot Logs", description="Command Usage Statistics", color=discord.Color.dark_purple())

        for user_id, commands in BotsLog.command_usage.items():
            user_name = await bot.fetch_user(user_id)  # Get the username from the user ID
            command_stats = "\n".join([f"{cmd}: {count} times" for cmd, count in commands.items()])
            
            embed.add_field(name=f"{user_name}", value=f"```{command_stats}```", inline=False)
        
        await inter.response.send_message(embed=embed)
        Perm = True
    else:
        await inter.response.send_message("You do not have permission to use this command.")
        Perm = False
    BotsLog.interlog(inter, command_name, Perm)

#Sync's Commands
@admin_group.command(name='sync', description='Sync Commands OwnerOnly')
async def sync(inter: discord.Interaction) -> None:
    command_name = "Slash Sync"
    if inter.user.id == OWNER_ID:
        await BotsCommand.Admin.sync(bot, inter) 
        Perm = True
    else:
        await inter.response.send_message("You do not have permission to use this command.")
        Perm = False
    BotsLog.interlog(inter, command_name, Perm)

#Poweroff Commands
@admin_group.command(name="poweroff", description="Poweroff Bot OwnerOnly")
async def poweroff(inter: discord.Interaction) -> None:
    command_name = "Power Off Bot"
    if inter.user.id == OWNER_ID:
        await BotsLog.Admin.poweroff(bot, inter) 
        Perm = True
    else:
        await inter.response.send_message("You do not have permission to use this command.")
        Perm= False
    BotsLog.interlog(inter, command_name, Perm)

#Restarts Bot 
@admin_group.command(name="restart", description='Restart bot OwnerOnly')
async def restarting(inter: discord.Interaction) -> None:
    command_name = "restart"
    if inter.user.id == OWNER_ID:
        await BotsCommand.Admin.bot_restart(bot, inter)
        username = inter.user.name
        user_id = inter.user.id
        Perm = True
    else:
        await inter.response.send_message("You do not have permission to use this command.")
        Perm = False
    BotsLog.interlog(inter, command_name, Perm)


#
@admin_group.command(name="Make Roles", description="Creates a role and add's it to a user")
async def mkrole(inter: discord.Interaction, rname: str, rcolour: int, ) -> None:
    command_name = "Make Role"
    if inter.user.id == OWNER_ID:
        await BotsCommand.admin.makerole(bot, inter, rname, rcolour)
        username = inter.user.name
        user_id = inter.user.id
        Perm = True
    else:
        await inter.response.send_message("You do not have permission to use this command.")
        Perm = False
    BotsLog.interlog(inter, command_name, Perm)

#


###


# DEFAULT USERS COMMANDS

#Ping slash commands
@bot.tree.command(name="ping", description="Ping's bot latency")
async def ping(inter: discord.Interaction) -> None:
    command_name = "Ping"
    Perm = default
    BotsLog.interlog(inter, command_name, Perm)  
    await BotsCommand.users.ping(inter, bot)
    

# Math Command Group
group = app_commands.Group(name="math", description="Math commands")
bot.tree.add_command(group)  # adds group commands into command tree

@group.command(name="add", description="Add two numbers")
async def add(inter: discord.Interaction, a: int, b: int) -> None:
    command_name = "add"
    Perm = default
    BotsLog.interlog(inter, command_name, Perm)
    await BotsCommand.users.add(inter, a, b)

bot.run(TOKEN)
