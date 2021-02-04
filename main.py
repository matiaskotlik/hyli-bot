from discord.errors import HTTPException
from discord.ext.commands.core import guild_only
from uwu import Uwuifier

import discord
from discord.ext import commands
import sys
import config

bot = commands.Bot(command_prefix=commands.when_mentioned_or(config.PREFIX),
                   help_command=None)

uwuifier = Uwuifier()


def is_uwu_channel(message: discord.Message):
    # this will filter guilds for us too
    return message and message.channel \
            and isinstance(message.channel, discord.TextChannel) \
            and config.UWU_PATTERN.match(message.channel.name)


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if is_uwu_channel(message):
        await uwuify_message(message)
        return

    # process other bot commands
    await bot.process_commands(message)


@bot.command()
@guild_only()
# don't run command in uwu channel
@commands.check(lambda ctx: not is_uwu_channel(ctx))
async def uwuify(ctx: commands.Context):
    last_message = await ctx.channel.history(limit=1,
                                             before=ctx.message).flatten()
    try:
        last_message = last_message[0]
    except IndexError:
        last_message = None

    await uwuify_message(last_message)


async def uwuify_message(message: discord.Message):
    if message and message.content:
        uwu_content = uwuifier.uwuify_sentence(message.content)
        try:
            await message.channel.send(uwu_content)
        except HTTPException:
            await message.channel.send(
                config.SEND_ERROR.format(author=message.author.mention))


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
