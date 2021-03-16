import re

import config
import discord
from discord.ext import commands


def is_uri(string: str):
    return string and re.match(r'^https?://', string) != None


def channel_matches(regex: re.Pattern):
    def predicate(ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage

        channel = ctx.channel

        if isinstance(channel, discord.TextChannel) and regex.match(channel.name):
            return True
        return False

    return commands.check(predicate)