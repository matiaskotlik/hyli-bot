import asyncio
import discord
from discord.ext import commands

import config


def setup(bot: commands.Bot):
    bot.add_cog(Gay(bot))


class Gay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gay(self, ctx: commands.Context):
        await ctx.message.delete()

        gay1 = await ctx.send(file=discord.File(config.GAY1))

        def check(msg):
            return msg.channel == ctx.channel

        try:
            new_message = await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            await gay1.delete()
        else:
            gay2 = await ctx.send(file=discord.File(config.GAY2))
