

import discord
from discord.ext import commands

import config
from utils import filter_line


def setup(bot: commands.Bot):
    bot.add_cog(Fatheroflies(bot))


class Fatheroflies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_nocommand(self, message: discord.Message):
        if message.author.bot or not message.content:
            return

        filtered = filter_line(message.content)
        try:
            idx = config.FATHER_SONG_FILTERED.index(filtered)
        except ValueError:
            # invalid line
            return

        idx = (idx + 1) % len(config.FATHER_SONG)
        line = config.FATHER_SONG[idx]
        await message.channel.send(line)
