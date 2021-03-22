import asyncio
import random
import sys
from typing import Optional

import config
import discord
import utils
from discord.ext import commands


def setup(bot: commands.Bot):
    bot.add_cog(Shutup(bot))


class Shutup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def shutup(self, ctx: commands.Context, channel: discord.VoiceChannel = None):
        await utils.try_delete(ctx)

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
                #await ctx.voice_client.disconnect() disconnect from voice after playing track
            coro = __after_playing(err)
            future = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
            try:
                future.result()
            except Exception as err:
                print(f'Error in after_playing: {err}', file=sys.stderr)
        return _after_playing

    async def ensure_voice(self, ctx: commands.Context, channel: discord.VoiceChannel = None):
        if channel:
            if ctx.voice_client:
                await ctx.voice_client.move_to(channel)
            else:
                await channel.connect()
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
