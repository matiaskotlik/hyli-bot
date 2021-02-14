import sys
from io import BytesIO
from pathlib import Path

import aiohttp

import config
import discord
from discord.errors import HTTPException
from discord.ext import commands
from discord.message import Message, MessageReference

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
    async def uwuify(self, ctx: commands.Context):
        last_message = None

        if ref := ctx.message.reference:
            if isinstance(ref, Message):
                last_message = ref
            elif isinstance(ref, MessageReference) and isinstance(ref.resolved, Message):
                last_message = ref.resolved

        if not last_message:
            last_message = await ctx.channel.history(limit=1, before=ctx.message).flatten()
            try:
                last_message = last_message[0]
            except IndexError:
                pass

        # passing None to this is fine
        await self.uwuify_message(last_message)

    async def uwuify_message(self, message: Message):
        if not message:
            return

        uwu_content = ''
        if message.content and not is_uri(message.content):
            uwu_content = self.uwuifier.uwuify_sentence(message.content)

        uwu_files = []
        attachments = [(a.proxy_url, a.filename, a.is_spoiler())
                       for a in message.attachments if a.width]
        embeds = [(e.thumbnail.url, e.url, False) for e in message.embeds if e.thumbnail]
        for url, filename, spoiler in attachments + embeds:
            image_out = BytesIO()
            await self.petpet.petify(url, image_out)
            image_out.seek(0)

            # change extension to .gif
            new_filename = Path(filename).with_suffix('.gif').name
            discord_file = discord.File(fp=image_out,
                                        filename=new_filename,
                                        spoiler=spoiler)
            uwu_files.append(discord_file)

        if uwu_content or uwu_files:
            try:
                await message.channel.send(content=uwu_content, files=uwu_files)
            except HTTPException:
                await message.channel.send(config.SEND_ERROR.format(author=message.author.mention))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:  # abort if bot sent the message
            return

        ctx = await self.bot.get_context(message)
        if ctx.valid:  # abort on command
            return

        if is_uwu_channel(message):
            await self.uwuify_message(message)
