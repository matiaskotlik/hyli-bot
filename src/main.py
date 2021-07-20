import datetime
import sys
import traceback

import discord
import humanize
from aiohttp.client import ClientSession
from discord.ext import commands

import config
import help
import database


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = self.loop.run_until_complete(self.create_session())
        self.client = database.get_client_connection()
        self.database = self.client.get_default_database()

    async def process_commands(self, message: discord.Message):
        if message.author.bot:
            self.dispatch('nocommand', message)
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
    intents = discord.Intents.default()
    intents.members = True
    intents.messages = True
    bot = Bot(command_prefix=commands.when_mentioned_or(config.PREFIX),
              help_command=help.HelpCommand(), allowed_mentions=discord.AllowedMentions.none(), intents=intents)

    bot.load_extension('cogs.uwu')
    bot.load_extension('cogs.banger')
    bot.load_extension('cogs.abhilmao')
    bot.load_extension('cogs.quote')
    bot.load_extension('cogs.fatheroflies')
    bot.load_extension('cogs.leaguers')
    bot.load_extension('cogs.gay')
    bot.load_extension('cogs.horny')
    bot.load_extension('cogs.shutup')
    bot.load_extension('cogs.sus')
    bot.load_extension('cogs.baby')
    bot.load_extension('cogs.kevinisuseless')
    bot.load_extension('cogs.undelete')
    bot.load_extension('cogs.camel')
    bot.load_extension('cogs.coinflip')

    @bot.command(brief="Load a module", hidden=True)
    @commands.is_owner()
    async def load(ctx: commands.Context, name: str):
        try:
            bot.load_extension(f'cogs.{name}')
        except Exception as e:
            await ctx.reply(f'Error: {e}')
        else:
            await ctx.reply('Loaded!', delete_after=config.MESSAGE_TIMER)

    @bot.command(brief="Unload a module", hidden=True)
    @commands.is_owner()
    async def unload(ctx: commands.Context, name: str):
        try:
            bot.unload_extension(f'cogs.{name}')
        except Exception as e:
            await ctx.reply(f'Error: {e}')
        else:
            await ctx.reply('Unloaded!', delete_after=config.MESSAGE_TIMER)

    @bot.command(brief="Reload a module", hidden=True)
    @commands.is_owner()
    async def reload(ctx: commands.Context, name: str):
        try:
            bot.reload_extension(f'cogs.{name}')
        except Exception as e:
            await ctx.reply(f'Error: {e}')
        else:
            await ctx.reply('Reloaded!', delete_after=config.MESSAGE_TIMER)

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
        elif isinstance(exception, commands.CheckFailure):
            # check fail
            pass
        elif isinstance(exception, commands.UserInputError):
            # arg fail
            pass
        elif isinstance(exception, commands.CommandOnCooldown):
            delta = humanize.precisedelta(
                datetime.timedelta(seconds=exception.retry_after))
            await ctx.reply(f'Try again in {delta}')
        else:
            print('Exception in command {}:'.format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(exception), exception, exception.__traceback__, file=sys.stderr)

    bot.run(config.BOT_TOKEN)
