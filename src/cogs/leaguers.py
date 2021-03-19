
import discord
from discord.ext import commands

import config


def setup(bot: commands.Bot):
    bot.add_cog(Leaguers(bot))


class Leaguers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id != config.MATIAS:
            return

        if not message.content:
            return

        if not message.guild:
            return

        role = message.guild.get_role(config.LEAGUE_ROLE)

        if role in message.role_mentions:
            await message.channel.send(config.LEAGUE_GIF)
