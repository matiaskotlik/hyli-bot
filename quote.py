import discord
from discord.channel import TextChannel
from discord.ext import commands
from peewee import *

import config
import database as db
from utils import files_from_message, is_quotes_channel


def setup(bot: commands.Bot):
    bot.add_cog(Quote(bot))


class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_nocommand(self, message: discord.Message):
        if message.author.bot or not is_quotes_channel(message):
            return

        quote = db.Quote.create(
            message_id=message.id, channel_id=message.channel.id, guild_id=message.guild.id)

        await message.reply('Saved!', delete_after=config.MESSAGE_TIMER)

    @commands.command()
    @commands.guild_only()
    async def quote(self, ctx: commands.Context):
        message = None
        while not message:
            try:
                quote = db.Quote \
                    .select() \
                    .where(db.Quote.guild_id == ctx.guild.id) \
                    .order_by(fn.Random()) \
                    .get()
                channel = ctx.guild.get_channel(quote.channel_id)
                if not channel:
                    raise discord.NotFound()
                message = await channel.fetch_message(quote.message_id)
            except discord.NotFound:
                quote.delete_instance()
            except db.Quote.DoesNotExist:
                await ctx.reply('There\'s not any quotes right now. Try again later.', delete_after=config.MESSAGE_TIMER)
                return

        files = await files_from_message(message)
        await ctx.send(content=message.clean_content, files=files)
