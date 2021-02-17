import asyncio
from io import BytesIO
import functools
import re

import discord
from discord.ext import commands
from discord.message import DeletedReferencedMessage

import config


async def files_from_message(message: discord.Message) -> list[discord.File]:
    files = []
    for attachment in message.attachments:
        with BytesIO() as fp:
            await attachment.save(fp)
            fp.seek(0)
            new_file = discord.File(fp, filename=attachment.filename)
            files.append(new_file)
    return files


def is_uwu_channel(message: discord.Message):
    return channel_matches(message, config.UWU_PATTERN)


def is_quotes_channel(message: discord.Message):
    return channel_matches(message, config.QUOTES_PATTERN)


def channel_matches(message: discord.Message, pattern: re.Pattern):
    # this will filter guilds for us too
    return message and message.channel \
        and isinstance(message.channel, discord.TextChannel) \
        and pattern.match(message.channel.name)


def run_in_executor(_func):  # https://stackoverflow.com/a/64506715
    @functools.wraps(_func)
    def _run_in_executor(*args, **kwargs):
        loop = asyncio.get_event_loop()
        func = functools.partial(_func, *args, **kwargs)
        return loop.run_in_executor(executor=None, func=func)
    return _run_in_executor


class SmartMessageConverter(commands.MessageConverter):
    async def convert(self, ctx, argument):
        print('tryin...')
        # try replies

        if not message:
            # this will either throw an exception or set message
            message = await super().convert(ctx, argument)

        return message
