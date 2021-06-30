

import random

from discord.ext import commands


def setup(bot: commands.Bot):
    bot.add_cog(Coinflip(bot))


class Coinflip(commands.Cog, name="Coin Flipper"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Flips a coin", aliases=["flip"])
    async def coinflip(self, ctx: commands.Context, *options):
        if not options:
            options = ['Heads', 'Tails']
        await ctx.reply(random.choice(options))

