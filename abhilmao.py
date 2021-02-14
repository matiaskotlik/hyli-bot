
import discord
from discord.ext import commands

import config


def setup(bot: commands.Bot):
    bot.add_cog(Abhilmao(bot))


class Abhilmao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id != config.ABHISHEK:
            return

        if not message.content:
            return

        if config.LMAO_PATTERN.match(message.content):
            await message.add_reaction(config.ABHI_LMAO)
