
from typing import Optional

import config
import discord
import utils
from discord.ext import commands
from pymongo import ReturnDocument
from utils import get_implied_message


def setup(bot: commands.Bot):
    bot.add_cog(Horny(bot))


class Horny(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.collection = bot.database.hornycounter

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(15, 60 * 60 * 2, commands.BucketType.user)
    @commands.guild_only()
    async def horny(self, ctx: commands.Context, user: discord.Member = None):
        user = user or (await utils.get_implied_message(ctx)).author
        record = self.collection.find_one_and_update(
            {'user_id': user.id, 'guild_id': ctx.guild.id},
            {'$inc': {'count': 1}},
            upsert=True, return_document=ReturnDocument.AFTER)

        await self.show(ctx, user, record['count'])

    @commands.command(aliases=['tophornies'])
    @commands.guild_only()
    async def tophorny(self, ctx: commands.Context):
        records = self.collection \
            .find({'guild_id': ctx.guild.id}) \
            .sort([('count', -1)]) \
            .limit(6)

        lines = [self.format_user_count(await self.get_nickname(ctx.guild, record['user_id']), record['count'])
                 for record in records]
        message = 'Most horny people:\n' + '\n'.join(lines)
        await ctx.send(message)

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def sethorny(self, ctx: commands.Context, user: discord.Member, amount: int):
        record = self.collection.find_one_and_update(
            {'user_id': user.id, 'guild_id': ctx.guild.id},
            {'$set': {'count': amount}},
            upsert=True, return_document=ReturnDocument.AFTER)

        await self.show(ctx, user, record['count'])

    @commands.command(aliases=['hornycount', 'hournycount'])
    @commands.guild_only()
    async def hornystatus(self, ctx: commands.Context, user: discord.Member):
        record = self.collection.find_one_and_update(
            {'user_id': user.id},
            {'$setOnInsert': {'count': 0}},
            upsert=True, return_document=ReturnDocument.AFTER)
        await self.show(ctx, user, record['count'])

    def format_user_count(self, name: str, count: int):
        plural = 's' if count != 1 else ''
        return f'{name} has been horny {count} time{plural}'

    async def get_nickname(self, guild: discord.Guild, user_id: int):
        try:
            user = self.bot.get_user(user_id) or await self.bot.fetch_user(user_id)
        except discord.NotFound:
            return '<Deleted User>'

        member = guild.get_member(user.id)
        try:
            name = member.nick or member.name  # if no nick, default to name
        except AttributeError:
            name = f'{user.name}#{user.discriminator}'
        return name

    async def show(self, ctx: commands.Context, user: discord.Member, count: int):
        await ctx.send(self.format_user_count(await self.get_nickname(ctx.guild, user.id), count))
