
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
        with db.atomic():
            hornycounter, _created = db.HornyCounter.get_or_create(user_id = user.id)
            hornycounter.count += 1
            new_count = hornycounter.count
            hornycounter.save()
        plural = 's' if new_count != 1 else ''
        await ctx.send(f'{user.display_name} has been horny {new_count} time{plural}')

        
