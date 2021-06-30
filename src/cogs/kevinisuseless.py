import config
import discord
import utils
from discord.ext import commands


def setup(bot: commands.Bot):
    bot.add_cog(Kevin(bot))

class Kevin(commands.Cog, name="Kevin"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Says that kevin is useless")
    async def kevinisuseless(self, ctx: commands.Context, name: str = 'Kevin'):
        await ctx.send(f'{name} is useless')

