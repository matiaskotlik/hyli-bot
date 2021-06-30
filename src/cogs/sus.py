import random
import config
import utils
import datetime
import discord

from discord.ext import commands


def setup(bot: commands.Bot):
    bot.add_cog(Sus(bot))


class Sus(commands.Cog, name="Sus Detector"):
    def __init__(self, bot):
        self.bot = bot
        self.hornies = [
            '{} is very horny!',
            '{} is extra horny today!',
            'watch out! {} is *omega* horny!',
            'but how fkn horny is {} today?!',
            '{} is super super horny rn, careful',
            '{} is like, super horny',
            '{} == horny',
        ]

        self.nothornies = [
            '{} isn\'t that horny today',
            'sorry but {} is *not* horny',
            '{} is very *un*horny right now...',
        ]


        self.sussies = [
            '{} is very sus!',
            '{} is extra sus today!',
            'watch out! {} is *omega* sus!',
            'but how fkn sus is {} today?!',
            '{} is super super sus rn, careful',
            '{} is like, super sus',
            '{} == sus',
            'lots of sus on {}...'
        ]

        self.notsussies = [
            '{} isn\'t that sus today',
            'sorry but {} is *not* sus at all',
            '{} is very *un*sus right now...',
        ]

    def user_is_horny(self, user: discord.Member):
        role = discord.utils.get(user.roles, name='horny')
        if role is not None:
            return True # some people are always horny :shrug:
        return self.user_rng(user)
    
    def user_is_sus(self, user: discord.Member):
        return self.user_rng(user)

    def user_rng(self, user: discord.Member):
        today = datetime.date.today()
        seed = f'{today}{user.id}'
        rng = random.Random()
        rng.seed(seed)
        return rng.choice((True, False))

    @commands.command(brief="Tells you if a gamer is horny")
    @commands.guild_only()
    async def ishorny(self, ctx: commands.Context, user: discord.Member):
        horny = self.user_is_horny(user)
        name = await utils.get_nickname(self.bot, ctx.guild, user.id)
        options = self.hornies if horny else self.nothornies
        strg = random.choice(options)
        await ctx.reply(strg.format(name))
    
    @commands.command(brief="Tells you if a gamer is sus", aliases=["sus"])
    @commands.guild_only()
    async def issus(self, ctx: commands.Context, user: discord.Member):
        sus = self.user_is_sus(user)
        name = await utils.get_nickname(self.bot, ctx.guild, user.id)
        options = self.sussies if sus else self.notsussies
        strg = random.choice(options)
        await ctx.reply(strg.format(name))

