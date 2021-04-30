
import re

import config
import discord
from discord.ext import commands


def setup(bot: commands.Bot):
    bot.add_cog(Leaguers(bot))


class Leaguers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_nocommand')
    async def single(self, message: discord.Message):
        if message.author.bot:
            return

        if not message.guild:
            return

        if message.guild.id != config.HH_SERVER:
            return

        print('a')
        if re.search(r'\bsingle\Wby\Wchoice', message.content, re.IGNORECASE):
            await message.channel.send(file=discord.File(config.SINGLE))

    @commands.Cog.listener('on_nocommand')
    async def leaguers(self, message: discord.Message):
        if message.author.id != config.MATIAS:
            return

        if not message.content:
            return

        if not message.guild:
            return

        role = message.guild.get_role(config.LEAGUE_ROLE)

        if role in message.role_mentions:
            await message.channel.send(config.LEAGUE_GIF)
