
from pathlib import Path
import re
from typing import Optional, Union
import config
import discord
from discord.ext import commands



def setup(bot: commands.Bot):
    bot.add_cog(Leaguers(bot))


class Leaguers(commands.Cog, name="Meme Replies"):
    def __init__(self, bot):
        self.bot = bot
        self.replies: list[tuple[Optional[list[int]], Optional[list[int]], Union[re.Pattern, int], Union[Path, str]]] = [
            (None, [config.HH_SERVER], re.compile(r'\bsingle\W+by\W+choice\b', re.IGNORECASE), config.SINGLE),  # single by choice
            ([config.KEVIN, config.MATIAS, config.VIOLET], None, config.LEAGUE_ROLE, config.LEAGUE_GIF),  # league ping
        ]

    @commands.Cog.listener()
    async def on_nocommand(self, message: discord.Message):
        if not message.content:
            return

        if not message.guild:
            return

        for valid_users, valid_guilds, criteria, reply_content in self.replies:
            if valid_users and message.author.id not in valid_users:
                continue

            if valid_guilds and message.guild.id not in valid_guilds:
                continue

            if isinstance(criteria, re.Pattern):
                pattern = criteria
                if not pattern.search(message.content):
                    continue
            elif isinstance(criteria, int): # role
                role = message.guild.get_role(criteria)
                if role not in message.role_mentions:
                    continue
            else:
                print(f'Invalid critera for message reply {criteria}')
                return

            if isinstance(reply_content, Path):
                await message.channel.send(file=discord.File(reply_content))
            elif isinstance(reply_content, str):
                await message.channel.send(reply_content)
            else:
                print(f'Invalid reply_content for message reply {reply_content}')
                return

