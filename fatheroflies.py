

import discord
from discord.ext import commands

import config


def setup(bot: commands.Bot):
    bot.add_cog(Fatheroflies(bot))


class Fatheroflies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.content:
            return

        if config.FATHER_PATTERN.match(message.content):
            await message.channel.send(config.FATHER_REPLY)
