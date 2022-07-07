# Libs
from io import IncrementalNewlineDecoder
import discord
from discord.abc import Connectable
from discord.ext import commands
import json
from pathlib import Path
import logging
import datetime
import os
from discord.state import ConnectionState

from discord_components import *

import cogs._json

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

def get_prefix(bot, message):
    data = cogs._json.read_json('prefixes')
    if not str(message.guild.id) in data:
        return commands.when_mentioned_or('?')(bot, message)
    return commands.when_mentioned_or(data[str(message.guild.id)])(bot, message)

#Defining a few things
secret_file = json.load(open(cwd+'/bot_config/secrets.json'))
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_id=655443924948877323)
bot.remove_command("help")
bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)

bot.blacklisted_users = []
bot.cwd = cwd

bot.version = '7'

bot.colors = {
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_NAVY': 0x2C3E50
}
bot.color_list = [c for c in bot.colors.values()]

@bot.event
async def on_ready():
    # On ready, print some details to standard out
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: -\n-----")
    await bot.change_presence(activity=discord.Game(name=f"Hi, my name's {bot.user.name}.\nUse prefix ? to interact with me!\n Made by 0x47#2579")) # This changes the bots 'activity'

@bot.event
async def on_message(message):
    #Ignore messages sent by yourself
    if message.author.id == bot.user.id:
        return

    #A way to blacklist users from the bot by not processing commands if the author is in the blacklisted_users list
    if message.author.id in bot.blacklisted_users:
        return

    #Whenever the bot is tagged, respond with its prefix
    if f"<@!{bot.user.id}>" in message.content:
        data = cogs._json.read_json('prefixes')
        if str(message.guild.id) in data:
            prefix = data[str(message.guild.id)]
        else:
            prefix = '?'
        prefixMsg = await message.channel.send(f"My prefix here is `{prefix}`")
        await prefixMsg.add_reaction('👀')

    await bot.process_commands(message)







    
@bot.group(invoke_without_command=True)
async def help(ctx):

    embed = discord.Embed(
        title=f"**Help**", 
        description="user ?help <commands> for extended information", 
        color=discord.Color.purple()
    )

    embed.add_field(name="help", value="Takes you here")
    embed.add_field(name="nitro",value="Generate unchecked nitro codes", inline=False)
    embed.add_field(name="**Under Construction**", value="\nAll commands under this aren't finished and under Construction", inline=False)
    embed.add_field(name="buy",value="?claim (gamepass id here)", inline=False)
    embed.add_field(name="roblox",value="Generate a roblox account", inline=False)

    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/904750355424870401/69bdb799325be5a653b6930bab5010af.png")

    embed.set_footer(text="The Prefix is ?",icon_url="https://cdn.discordapp.com/avatars/904750355424870401/69bdb799325be5a653b6930bab5010af.png")

    await ctx.send(
        embed=embed,
    )
    

#fix ,`create_channel`,`create_category`,`delete_channel`,`delete_category` commands

#Moderation
@help.command()
async def nitro(ctx):
    embed = discord.Embed(
        title=f"Description", 
        description="Kicks a member from the guild", 
        color=discord.Color.dark_blue()
    )

    embed.add_field(name="**Syntax**", value="?kick <member> [reason]")

    await ctx.send(embed=embed)    

@help.command()
async def ban(ctx):
    embed = discord.Embed(
        title=f"Description", 
        description="Bans a member from the guild", 
        color=discord.Color.dark_blue()
    )

    embed.add_field(name="**Syntax**", value="?ban <member> [reason]")

    await ctx.send(embed=embed)    

@help.command()
async def unban(ctx):
    embed = discord.Embed(
        title=f"Description", 
        description="Unbans a member from the guild", 
        color=discord.Color.dark_blue()
    )

    embed.add_field(name="**Syntax**", value="?unban <memberId>")

    await ctx.send(embed=embed)    

@help.command()
async def purge(ctx):
    embed = discord.Embed(
        title=f"Description", 
        description="Deletes messages in the same channel", 
        color=discord.Color.dark_blue()
    )

    embed.add_field(name="**Syntax**", value="?purge <amout>")

    await ctx.send(embed=embed)   


@help.command()
async def mute(ctx):
    embed = discord.Embed(
        title=f"Description", 
        description="Mutes member in guild", 
        color=discord.Color.dark_blue()
    )

    embed.add_field(name="**Syntax**", value="?mute <member> [reason]")

    await ctx.send(embed=embed)   







if __name__ == '__main__':
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
    bot.run(bot.config_token)