import discord, datetime
from discord.ext import commands
class BotsLog:
    log_file = "Logs/bot_logs.txt"  # Log file path
    command_usage = {}  # Dictionary to track command usage

    @staticmethod
    def interlog(inter: discord.Interaction, command_name: str, Perm: str):
        username = inter.user.name
        user_id = inter.user.id
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if inter.guild is None:
            location = "DM"
        else:
            location = f"Server: {inter.guild.name} (ID: {inter.guild.id}) | Channel: {inter.channel.name} (ID: {inter.channel.id})"
        
        log_entry = (f"Time: {current_time}\n"
                     f"Command: {command_name}\nUser: {username}\nID: {user_id}\n"
                     f"Perm: {Perm}\nLocation: {location}\n{'=='*10}\n")
        
        # Write log entry to file
        with open(BotsLog.log_file, 'a') as log:
            log.write(log_entry)
        
        # Update command usage count
        if user_id not in BotsLog.command_usage:
            BotsLog.command_usage[user_id] = {}
        
        if command_name not in BotsLog.command_usage[user_id]:
            BotsLog.command_usage[user_id][command_name] = 0
        
        BotsLog.command_usage[user_id][command_name] += 1

        print(log_entry)  # Still print to console if needed

    @staticmethod
    def ctxlog(ctx: commands.Context, command_name: str, Perm: str):
        user_id = ctx.message.author.id
        username = ctx.message.author.name
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if ctx.guild is None:
            location = "DM"
        else:
            location = f"Server: {ctx.guild.name} (ID: {ctx.guild.id}) | Channel: {ctx.channel.name} (ID: {ctx.channel.id})"
        
        log_entry = (f"Time: {current_time}\n"
                     f"Command: {command_name}\nUser: {username}\nID: {user_id}\n"
                     f"Perm: {Perm}\nLocation: {location}\n{'=='*10}\n")
        
        # Write log entry to file
        with open(BotsLog.log_file, 'a') as log:
            log.write(log_entry)
        
        # Update command usage count
        if user_id not in BotsLog.command_usage:
            BotsLog.command_usage[user_id] = {}
        
        if command_name not in BotsLog.command_usage[user_id]:
            BotsLog.command_usage[user_id][command_name] = 0
        
        BotsLog.command_usage[user_id][command_name] += 1

        print(log_entry)  # Still print to console if needed
