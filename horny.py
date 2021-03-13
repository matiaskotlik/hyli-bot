
import discord
from discord.ext import commands
import config
import database as db


def setup(bot: commands.Bot):
    bot.add_cog(Horny(bot))


class Horny(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def horny(self, ctx: commands.Context, user: discord.User):
        counter, _ = db.HornyCounter.get_or_create(user_id = user.id)
        counter.count += 1
        counter.save()
        await self.show(ctx, user, counter.count)

    @commands.command()
    @commands.is_owner()
    async def sethorny(self, ctx: commands.Context, user: discord.User, amount: int):
        counter, _created = db.HornyCounter.get_or_create(user_id = user.id)
        counter.count = amount
        counter.save()
        await self.show(ctx, user, amount)

    @commands.command(aliases=['hornycount'])
    async def hornystatus(self, ctx: commands.Context, user: discord.User):
        counter, _ = db.HornyCounter.get_or_create(user_id = user.id)
        await self.show(ctx, user, counter.count)

    async def show(self, ctx: commands.Context, user: discord.User, count: int):
        plural = 's' if count != 1 else ''
        await ctx.send(f'{user.display_name} has been horny {count} time{plural}')
