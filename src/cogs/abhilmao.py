
import re

import config
import discord
from discord import permissions
from discord.ext import commands


def setup(bot: commands.Bot):
    bot.add_cog(Abhilmao(bot))


class Abhilmao(commands.Cog, name="Reactions"):
    def __init__(self, bot):
        self.bot = bot
        self.reacts: list[tuple[Optional[list[int]], re.Pattern, list[str]]] = [
            ([config.ABHISHEK], re.compile(r'\blmf?a+o+\b', re.IGNORECASE), ['<:lmao:804387193506103316>']),  # abhishek lmao
            ([config.RAGHAV], re.compile(r'\bcum(ming)?\b', re.IGNORECASE), ['<:cum:819649767666614303>']),  # raghav cum
            ([config.VIOLET], re.compile(r'\bmm+\s+penis\b', re.IGNORECASE), ['🤤', '🍆']),  # violet mmm penis
            ([config.VIOLET], re.compile(r'\byu+bee\b', re.IGNORECASE), ['😺', '🐝']),  # violet yubee
            ([config.MATIAS], re.compile(r'\bju?n?gl?e?\W*(dif|gap)', re.IGNORECASE), ['<:jgdif:818221968297295928>']),  # matias jgdif
            # ([config.MATIAS], re.compile(r'\bju?n?gl?e?\W*(dif|gap)', re.IGNORECASE), ['🇯', '🇬', '🇩', '🇮', '🇫']),  # matias jgdif
            ([config.ZAPATA], re.compile(r'\b(fem)?(boy\W*)?cock\b', re.IGNORECASE), ['🍆']),  # zapata eggplant
            (None, re.compile(r'\bsmoger?\b', re.IGNORECASE), [r'<:sadge:753638806460039218>', '🚬']),  # smoge
        ]



    @commands.Cog.listener()
    async def on_nocommand(self, message: discord.Message):
        if not message.content:
            return

        error = False
        for valid_ids, pattern, reactions in self.reacts:
            # valid_ids = None means any user is fine for this reaction
            if valid_ids and message.author.id not in valid_ids:
                continue

            if not pattern.search(message.content):
                continue

            for r in reactions:
                try:
                    await message.add_reaction(r)
                except discord.HTTPException:
                    # emoji does not exist in this server
                    if message.guild is not None:
                        print(f'Tried to react with invalid emoji {r} in server {message.guild.name} (message.guild.id)')
                except discord.Forbidden:
                    # permissions issue
                    error = True

        if error:
            message.channel.send(config.NO_PERMISSIONS)
