import discord
from discord.ext import commands
import random, string
import asyncio
import traceback
import sys

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command()
    @commands.cooldown(1, 900, commands.BucketType.guild)
    async def nitro(self, ctx):
        author = ctx.author

        num = 12
        role = discord.utils.get(ctx.guild.roles, name="Nitro_Cooldown")
        time = 900

        embed1 = discord.Embed(
            title="**Okilly Dokilly**",
            description="I'm sending you 10 unchecked nitro codes!\n\nUnchecked means that most will be invalid, and you have a chance of getting a valid one.",
            color=discord.Color.purple()
        )
        
        await ctx.send(embed=embed1)
        await ctx.send(author.mention)

        for n in range(int(num)):
            y = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(16))
            await author.send(f'https://discord.gift/{y}')

        await author.add_roles(role)
        if time:
            await asyncio.sleep(time)
            await author.remove_roles(role)


    #@commands.command()
    #@commands.is_owner()
    #async def mega_nitro(self, ctx):
       #author = ctx.author

        #num = 100


        #embed1 = discord.Embed(
            #title="**Okilly Dokilly**",
            #description="I'm sending you 100 unchecked nitro codes!\n\nUnchecked means that most will be invalid, and you have a chance of getting a valid one.",
            #color=discord.Color.purple()
        #)
        
        #await ctx.send(embed=embed1)
        #await ctx.send(author.mention)

        #for n in range(int(num)):
            #y = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(16))
            #await author.send(f'https://discord.gift/{y}')


    @nitro.error
    async def nitro_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed2 = discord.Embed(
                title="**Cooldown**",
                description=f"{int(error.retry_after)} Seconds",
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed2)
        else:
            error = getattr(error, 'original', error)
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(Moderation(bot))
