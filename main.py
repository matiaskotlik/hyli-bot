import sys
import traceback

import discord
from discord.ext import commands

import config
from banger import Banger
from uwu import Uwu

if __name__ == '__main__':
    bot = commands.Bot(command_prefix=commands.when_mentioned_or(
        config.PREFIX), help_command=None)

    bot.add_cog(Uwu(bot))
    bot.add_cog(Banger(bot))

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
            # await ctx.send(
            #     config.INVALID_COMMAND.format(author=ctx.author.mention),
            #     delete_after=config.MESSAGE_TIMER)
        elif isinstance(exception, discord.errors.Forbidden):
            # don't have permissions
            await ctx.send(config.NO_PERMISSIONS.format(author=ctx.author.mention),
                           delete_after=config.MESSAGE_TIMER)
        else:
            print('Exception in command {}:'.format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(exception), exception, exception.__traceback__, file=sys.stderr)

    bot.run(config.BOT_TOKEN)
