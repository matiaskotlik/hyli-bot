import random

import config
import discord
from discord.channel import TextChannel
from discord.ext import commands
from utils import files_from_message, is_quotes_channel


def setup(bot: commands.Bot):
    bot.add_cog(Quote(bot))


class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.collection = bot.database.quotes

    @commands.Cog.listener()
    async def on_nocommand(self, message: discord.Message):
        if message.author.bot or not is_quotes_channel(message):
            return

        # is_quotes_channel above will fail if not in a guild, so message.guild is safe
        self.collection.insert_one({
            'message_id': message.id,
            'channel_id': message.channel.id,
            'guild_id': message.guild.id,
        })

        await message.reply('Saved!', delete_after=config.MESSAGE_TIMER)

    @commands.command()
    @commands.guild_only()
    async def quote(self, ctx: commands.Context):
        message = None
        while not message:
            count = self.collection.count_documents({'guild_id': ctx.guild.id})
            if count == 0:
                await ctx.reply('There\'s not any quotes right now. Try again later.', delete_after=config.MESSAGE_TIMER)
                return

            idx = random.randrange(count)
            try:
                quote = self.collection.find({'guild_id': ctx.guild.id})[idx]
            except IndexError:
                await ctx.reply('There was an error retrieving a quote. Try again later.', delete_after=config.MESSAGE_TIMER)
                return

            channel = ctx.guild.get_channel(quote['channel_id'])
            if not channel:
                # channel was deleted, delete all records from that channel
                self.collection.delete_many(
                    {'channel_id': quote['channel_id'],
                     'guild_id': quote['guild_id']})
                continue

            try:
                message = await channel.fetch_message(quote['message_id'])
            except discord.NotFound:
                # message was deleted
                self.collection.delete_one(quote)
                continue

        files = await files_from_message(message)
        await ctx.send(content=message.clean_content, files=files)
