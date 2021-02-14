import sys
from io import BytesIO
from pathlib import Path
from typing import Optional, Union
from utils import SmartMessageConverter

import aiohttp
from discord.ext.commands.errors import BadArgument

import config
import discord
from discord.errors import HTTPException
from discord.ext import commands
from discord.message import Message

from .petpet import Petpet
from .utils import is_uwu_channel, is_uri
from .uwuifier import Uwuifier


def setup(bot: commands.Bot):
    bot.add_cog(Uwu(bot))


class Uwu(commands.Cog):
    def __init__(self, bot, uwuifier: Uwuifier = None, petpet: Petpet = None):
        self.bot = bot
        self.uwuifier = uwuifier or Uwuifier()
        self.petpet = petpet or Petpet(self.bot.session)

    @commands.command()
    @commands.guild_only()
    async def uwuify(self, ctx: commands.Context, target: Union[Message, discord.User, discord.Member] = None):
        target = target or await self.locate_uwu_message(ctx)
        if isinstance(target, Message):
            await self.uwuify_message(ctx, target)
        elif isinstance(target, discord.User) or isinstance(target, discord.Member):
            await self.uwuify_user(ctx, target)
        else:
            raise commands.BadArgument()  # unreachable

    async def locate_uwu_message(self, ctx: commands.Context) -> Message:
        message = None
        if ref := ctx.message.reference:
            message = ref
        if isinstance(message, discord.MessageReference):
            message = ref.resolved

        if isinstance(message, Message):
            return message
        elif message == None:
            try:
                return (await ctx.channel.history(limit=1, before=ctx.message).flatten())[0]
            except IndexError:
                pass

        raise commands.BadArgument()

    async def uwuify_user(self, channel, user: Union[discord.User, discord.Member]):
        await channel.send(files=await self.transform_files([str(user.avatar_url)]))

    async def uwuify_message(self, channel, message: Message):
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
            try:
                await channel.send(content=uwu_content, files=uwu_files)
            except HTTPException:
                await channel.send(config.SEND_ERROR.format(author=message.author.mention))

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
    async def on_message(self, message: Message):
        if message.author.bot:  # abort if bot sent the message
            return

        ctx = await self.bot.get_context(message)
        if ctx.valid:  # abort on command
            return

        if is_uwu_channel(message):
            await self.uwuify_message(message.channel, message)
