import sys
import traceback

import discord
from aiohttp.client import ClientSession
from discord.ext import commands

import config


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = self.loop.run_until_complete(self.create_session())

    async def process_commands(self, message: discord.Message):
        if message.author.bot:
            return

        ctx = await self.get_context(message)
        if ctx.valid:
            await self.invoke(ctx)
        else:
            self.dispatch('nocommand', message)

    async def create_session(self):
        return ClientSession(loop=self.loop)

    async def close(self):
        await self.session.close()
        return await super().close()


if __name__ == '__main__':
    bot = Bot(command_prefix=commands.when_mentioned_or(config.PREFIX),
              help_command=None)

    bot.load_extension('uwu')
    bot.load_extension('banger')
    bot.load_extension('abhilmao')
    bot.load_extension('quote')

    @bot.event
    async def on_ready():
        print('Connected!')
        print(f'Username: {bot.user.name}')
        print(f'ID: {bot.user.id}')

    @bot.event
    async def on_command_error(ctx: commands.Context, exception: commands.CommandError):
        if isinstance(exception, commands.errors.CommandNotFound):
            # invalid command. ignore
            pass
            # await ctx.reply(
            #     config.INVALID_COMMAND,
            #     delete_after=config.MESSAGE_TIMER)
        elif isinstance(exception, discord.errors.Forbidden):
            # don't have permissions
            await ctx.reply(config.NO_PERMISSIONS, delete_after=config.MESSAGE_TIMER)
        else:
            print('Exception in command {}:'.format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(exception), exception, exception.__traceback__, file=sys.stderr)

    bot.run(config.BOT_TOKEN)
