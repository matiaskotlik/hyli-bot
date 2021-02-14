import functools
import asyncio
import discord

from discord.ext import commands
from discord.message import DeletedReferencedMessage


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
        if ref := ctx.message.reference:
            message = ref
        if isinstance(message, discord.MessageReference):
            message = ref.resolved

        if message == None or isinstance(message, discord.Message):
            pass # good
        else:
            raise commands.BadArgument()

        if not message:
            try:
                message = await ctx.channel.history(limit=1, before=ctx.message).flatten()[0]
            except IndexError:
                pass

        if not message:
            # this will either throw an exception or set message
            message = await super().convert(ctx, argument)

        return message
