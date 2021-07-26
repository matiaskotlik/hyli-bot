import sys
from io import BytesIO
from pathlib import Path
from typing import Union

import aiohttp
import config
import discord
from discord.errors import HTTPException
from discord.ext import commands
from discord.ext.commands.errors import BadArgument
from discord.message import Message
from utils import get_implied_message, is_uri, is_uwu_channel

from .petpet import Petpet
from .uwuifier import Uwuifier


def setup(bot: commands.Bot):
    bot.add_cog(Uwu(bot))


class Uwu(commands.Cog, name="UwU"):
    def __init__(self, bot, uwuifier: Uwuifier = None, petpet: Petpet = None):
        self.bot = bot
        self.uwuifier = uwuifier or Uwuifier()
        self.petpet = petpet or Petpet(self.bot.session)

    @commands.command(brief="Uwuifies a message or gamer")
    async def uwuify(self, ctx: commands.Context, target: discord.Member = None):
        target = target or await get_implied_message(ctx)
        if isinstance(target, Message):
            await self.uwuify_message(ctx, ctx.channel, target)
        elif isinstance(target, discord.Member):
            await self.uwuify_user(ctx, target)
        else:
            # unreachable
            raise Exception(
                f"target is not valid type: {type(target)} {target}")

    async def uwuify_user(self, channel, user: Union[discord.User, discord.Member]):
        await channel.send(files=await self.transform_files([str(user.avatar_url)]))

    async def uwuify_message(self, origin, channel: discord.TextChannel, message: Message):
        if not message:
            return

        uwu_content = ''
        content = message.clean_content
        if content and not is_uri(content):
            uwu_content = self.uwuifier.uwuify_sentence(content)

        attachments = [a.proxy_url for a in message.attachments if a.width]
        embeds = [e.thumbnail.url for e in message.embeds if e.thumbnail]
        uwu_files = await self.transform_files(attachments + embeds)

        if uwu_content or uwu_files:
            await channel.send(content=uwu_content, files=uwu_files)

    async def transform_files(self, urls):
        files = []
        for url in urls:
            image_out = BytesIO()
            await self.petpet.petify(url, image_out)
            image_out.seek(0)

            # change extension to .gif
            new_filename = Path(url).with_suffix('.gif').name
            discord_file = discord.File(fp=image_out,
                                        filename=new_filename)
            files.append(discord_file)
        return files

    @commands.Cog.listener()
    async def on_nocommand(self, message: Message):
        if message.author.bot or not is_uwu_channel(message):
            return

        await self.uwuify_message(message, message.channel, message)
