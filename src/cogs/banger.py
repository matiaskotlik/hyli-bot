import config
import discord
import utils
from discord.ext import commands


def setup(bot: commands.Bot):
    bot.add_cog(Banger(bot))


class Banger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def banger(self, ctx: commands.Context):
        await utils.try_delete(ctx)
        await ctx.send(file=discord.File(config.BANGER))
