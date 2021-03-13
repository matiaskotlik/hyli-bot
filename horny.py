
import discord
from discord.ext import commands
import config
from typing import Optional
import database as db


def setup(bot: commands.Bot):
    bot.add_cog(Horny(bot))


class Horny(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def horny(self, ctx: commands.Context, user: discord.User):
        counter, _ = db.HornyCounter.get_or_create(user_id=user.id)
        counter.count += 1
        counter.save()
        await self.show(ctx, user, counter.count)

    @commands.command(aliases=['tophornies'])
    async def tophorny(self, ctx: commands.Context):
        query = db.HornyCounter.select().where(db.HornyCounter.count > 0).order_by(-db.HornyCounter.count).limit(5)
        async def format_line(counter: db.HornyCounter):
            user = self.bot.get_user(counter.user_id) or await self.bot.fetch_user(counter.user_id)
            return self.format_user_count(ctx.guild, user, counter.count)
        message = 'Most horny people:\n'
        message += '\n'.join([await format_line(counter) for counter in query])
        await ctx.send(message)
    
    @commands.command()
    @commands.is_owner()
    async def sethorny(self, ctx: commands.Context, user: discord.User, amount: int):
        counter, _created = db.HornyCounter.get_or_create(user_id=user.id)
        counter.count = amount
        counter.save()
        await self.show(ctx, user, amount)

    @commands.command(aliases=['hornycount'])
    async def hornystatus(self, ctx: commands.Context, user: discord.User):
        counter, _ = db.HornyCounter.get_or_create(user_id=user.id)
        await self.show(ctx, user, counter.count)

    def format_user_count(self, guild: discord.Guild, user: discord.User, count: int):
        plural = 's' if count != 1 else ''
        try:
            member = guild.get_member(user.id)
            name = member.nick or member.name # if no nick, default to name
        except AttributeError:
            name = f'{user.name}#{user.discriminator}'
        return f'{name} has been horny {count} time{plural}'

    async def show(self, ctx: commands.Context, user: discord.User, count: int):
        await ctx.send(self.format_user_count(ctx.guild, user, count))
