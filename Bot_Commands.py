import os
import sys
import platform
import discord
from discord.ext import commands

# File to store the restart status
RESTART_STATUS_FILE = "restart_status.txt"
Status_Name = 'Your tears'
act_type = discord.ActivityType.listening


if platform.system() == "Windows":
    os.system("cls")
else:
    os.system("clear")


class BotsCommand:
    class Admin:

        #Powersoff Bot
        @staticmethod
        async def poweroff(bot, inter:discord.Interaction) -> None:
            await inter.response.send_message("Powering off Bot")
            await bot.close()

        #Sync's Commands global to discord
        @staticmethod
        async def sync(bot, inter: discord.Interaction) -> None:
            try:
                synced = await bot.tree.sync()
                await inter.response.send_message(f"Synced {len(synced)} commands globally")
                print(f"Synced {len(synced)} commands globally")
            except Exception as e:
                await inter.response.send_message(f"Failed to sync commands: {e}")
                print(f"Error syncing commands: {e}")

        #Restarts the bot
        @staticmethod
        async def bot_restart(bot, inter: discord.Interaction) -> None:
            await inter.response.send_message("Restarting bot...")
            print("Restarting bot...")

            restart_context = "dm" if isinstance(inter.channel, discord.DMChannel) else "server"
            with open(RESTART_STATUS_FILE, 'w') as f:
                f.write(f"{inter.user.id},{inter.channel.id if restart_context == 'server' else 'None'},{restart_context}")

            await bot.close()
            if platform.system() == "Windows":
                os.system("cls")
            else:
                os.system("clear")
            os.execv(sys.executable, ['python'] + sys.argv) 

    class users:
        #Pings bots latency
        @staticmethod
        async def ping(inter: discord.Interaction, bot) -> None:
            await inter.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")
            print(f"Ping is {round(bot.latency * 1000)}ms")



#NOT COMMANDS 


async def change_status(bot) -> None:
    await bot.change_presence(activity=discord.Activity(type=act_type, name=Status_Name))
    print('Status has been set to "', str(act_type).replace('ActivityType.', ''),'to', Status_Name,'"')

async def handle_restart_status(bot) -> None:
    if os.path.exists(RESTART_STATUS_FILE):

        try:
            with open(RESTART_STATUS_FILE, 'r') as f:
                user_id, channel_id, context = f.read().strip().split(',')
                user_id = int(user_id)
                channel_id = int(channel_id) if channel_id != 'None' else None

            os.remove(RESTART_STATUS_FILE)

            if context == "dm":
                user = bot.get_user(user_id)
                if user:
                    try:
                        await user.send("Bot has been restarted.")
                    except discord.Forbidden:
                        print("Failed to notify user about bot restart. The user might have DMs disabled.")
                else:
                    print("User not found in cache. Trying to fetch user...")
                    user = await bot.fetch_user(user_id)
                    if user:
                        try:
                            await user.send("Bot has been restarted.")
                        except discord.Forbidden:
                            print("Failed to notify user about bot restart after fetch. The user might have DMs disabled.")

            elif context == "server":
                channel = bot.get_channel(channel_id)
                if channel:
                    try:
                        await channel.send("Bot has been restarted.")
                    except discord.NotFound:
                        print("Failed to notify channel about bot restart. The channel might not be available.")
                else:
                    print("Channel not found in cache. Trying to fetch channel...")
                    channel = await bot.fetch_channel(channel_id)
                    if channel:
                        try:
                            await channel.send("Bot has been restarted.")
                        except discord.NotFound:
                            print("Failed to notify channel about bot restart after fetch. The channel might not be available.")

        except Exception as e:
            print(f"Error handling restart notification: {e}")
