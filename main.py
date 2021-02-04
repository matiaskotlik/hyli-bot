from uwu import Uwuifier

import discord
from discord.ext import commands
import sys
import config

bot = commands.Bot(command_prefix=commands.when_mentioned_or(config.PREFIX),
                   help_command=None)

uwuifier = Uwuifier()


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    channel = message.channel
    if channel \
            and isinstance(channel, discord.TextChannel) \
            and config.UWU_PATTERN.match(channel.name):
        await uwuify(message)
        return

    # process other bot commands
    await bot.process_commands(message)


async def uwuify(message: discord.Message):
    content = message.content
    if content:
        uwu_content = uwuifier.uwuify_sentence(content)
        await message.channel.send(uwu_content)


@bot.event
async def on_command_error(ctx: commands.Context,
                           error: commands.CommandError):
    if isinstance(error, commands.errors.CommandNotFound):
        # invalid command. notify whoever sent it.
        await ctx.send(
            config.INVALID_COMMAND.format(author=ctx.author.mention),
            delete_after=config.MESSAGE_TIMER)
    elif isinstance(error, discord.errors.Forbidden):
        # don't have permissions
        await ctx.send(config.NO_PERMISSIONS.format(author=ctx.author.mention),
                       delete_after=config.MESSAGE_TIMER)
    else:
        print(
            error, file=sys.stderr
        )  # print out the error message to standard error (make the text red in pycharm)


if __name__ == '__main__':
    bot.run(config.BOT_TOKEN)
