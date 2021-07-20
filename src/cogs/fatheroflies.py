from pathlib import Path
from itertools import tee
from typing import Optional
import re

import config
import discord
from discord.ext import commands
from dataclasses import dataclass

@dataclass
class Song:
    lyrics: dict[str, str]

    def get_next_line(self, line: str) -> Optional[str]:
        filtered = self.filter_line(line)
        return self.lyrics.get(filtered, None)

    @classmethod
    def from_lyrics(cls, lyrics: list[str]) -> 'Song':
        lines = [line.strip() for line in lyrics]
        filtered_lines = [cls.filter_line(line) for line in lines]

        # map the first filtered line to the second real line and so on, looping around
        lines.append(lines.pop(0))
        return Song(dict(zip(filtered_lines, lines)))
    
    @classmethod
    def from_path(cls, path: Path) -> 'Song':
        with open(path, 'r') as fp:
            return Song.from_lyrics(fp.readlines())

    @classmethod
    def filter_line(cls, strg: str):
        return re.sub(r'[^A-Za-z\n]', '', strg.lower())


def setup(bot: commands.Bot):
    bot.add_cog(Fatheroflies(bot))


class Fatheroflies(commands.Cog, name="Song Singer"):
    def __init__(self, bot):
        self.bot = bot
        self.songs = [
            Song.from_path(config.FATHER_SONG_PATH),
            Song.from_path(config.ASTRONAUT_SONG_PATH)
        ]

    @commands.Cog.listener()
    async def on_nocommand(self, message: discord.Message):
        if message.author.bot or not message.content:
            return

        for song in self.songs:
            if line := song.get_next_line(message.content):
                await message.channel.send(line)
                return