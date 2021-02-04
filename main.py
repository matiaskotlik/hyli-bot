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
        await uwuify_clone(message)
        return

    # process other bot commands
    await bot.process_commands(message)


@bot.command()
async def uwuify(ctx: commands.Context):
    last_message = await ctx.channel.history(limit=1, before=ctx.message).flatten()
    try:
        last_message = last_message[0]
    except IndexError:
        # no message to uwuify
        ctx.send(config.NO_MESSAGE.format(ctx.author.mention))
        return
    print(last_message.author, last_message.content)
    
    await uwuify_message(last_message)


async def uwuify_message(message: discord.Message):
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
