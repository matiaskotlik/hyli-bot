import random
import re

import config
import discord
from discord import Colour, Embed
from discord.ext import commands


def channel_matches(regex: re.Pattern):
    def predicate(ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage

        channel = ctx.channel

        if isinstance(channel, discord.TextChannel) and regex.match(channel.name):
            return True
        return False

    return commands.check(predicate)


def is_uwu_channel(message: discord.Message):
    # this will filter guilds for us too
    return message and message.channel \
        and isinstance(message.channel, discord.TextChannel) \
        and config.UWU_PATTERN.match(message.channel.name)
