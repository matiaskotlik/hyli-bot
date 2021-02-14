import discord
from discord.ext import commands

def setup(bot: commands.Bot):
    bot.add_cog(Banger(bot))

class Banger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def banger(self, ctx: commands.Context):
        await ctx.send(file=discord.File('banger.png'))
