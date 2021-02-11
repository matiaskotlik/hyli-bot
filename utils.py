import discord
from discord import Colour, Embed
from discord.ext import commands
import random
import config
import re


def random_color():
    """A factory method that returns a :class:`Colour` with a random hue.
    .. note::
        The random algorithm works by choosing a colour with a random hue but
        with maxed out saturation and value.
    """
    return Colour.from_hsv(random.random(), 1, 1)

def no_bot():
    def predicate(ctx):
        return not ctx.author.bot
    return commands.check(predicate)

def channel_matches(regex: re.Pattern):
    def predicate(ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage

        channel = ctx.channel

        if isinstance(channel, discord.TextChannel) and regex.match(
                channel.name):
            return True
        return False

    return commands.check(predicate)


def is_uwu_channel(message: discord.Message):
    # this will filter guilds for us too
    return message and message.channel \
            and isinstance(message.channel, discord.TextChannel) \
            and config.UWU_PATTERN.match(message.channel.name)
