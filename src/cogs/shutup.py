import asyncio
import random
import sys
from typing import Optional

import config
import discord
import utils
from discord.ext import commands


async def get_channel_with_name(guild: discord.Guild, name: str):
    # find channel with matching name
    for channel in guild.voice_channels:
        if utils.filter_line(channel.name) == utils.filter_line(name):
            return channel
    raise discord.ChannelNotFound(name)


class BetterVoiceChannelConverter(commands.VoiceChannelConverter):
    async def convert(self, ctx, argument):
        # try normal voicechannel converter
        try:
            channel = await super().convert(ctx, argument)
        except discord.DiscordException:
            channel = await get_channel_with_name(ctx.guild, argument)
        return channel


def setup(bot: commands.Bot):
    bot.add_cog(Shutup(bot))


class Shutup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def shutup(self, ctx: commands.Context, channel: Optional[BetterVoiceChannelConverter]):
        try:
            await ctx.message.delete()
        except discord.errors.DiscordException:
            await ctx.send(config.NO_PERMISSIONS, delete_after=config.MESSAGE_TIMER)
            return

        files = list(config.SHUTUP_PATH.glob('**/*.mp3'))
        if not files:
            ctx.send('Can\'t find any files to play.',
                     delete_after=config.MESSAGE_TIMER)
            return

        filename = random.choice(files)

        if not await self.ensure_voice(ctx, channel):
            return

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename))
        try:
            ctx.voice_client.play(source, after=self.after_playing(ctx))
        except discord.ClientException:
            # sometimes we get disconnected during/right before playing the track
            pass

    def after_playing(self, ctx):
        def _after_playing(err):
            async def __after_playing(err):
                if err:
                    return print(f'Player error: {err}', file=sys.stderr)
                await ctx.voice_client.disconnect()
            coro = __after_playing(err)
            future = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
            try:
                future.result()
            except Exception as err:
                print(f'Error in after_playing: {err}', file=sys.stderr)
        return _after_playing

    async def ensure_voice(self, ctx: commands.Context, channel: Optional[discord.VoiceChannel]):
        if channel:
            if ctx.voice_client:
                await channel.connect()
            else:
                await ctx.voice_client.move_to(channel)
        elif not ctx.voice_client:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Not connected to a voice channel.", delete_after=config.MESSAGE_TIMER)
                return False
        elif ctx.voice_client.is_playing():
            # already playing
            return False
        return True
