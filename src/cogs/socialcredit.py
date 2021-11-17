import re

from urllib.parse import urlparse

import config
import discord
import utils
from discord.ext import commands
from pymongo import ReturnDocument


def setup(bot: commands.Bot):
    bot.add_cog(SocialCredit(bot))


class SocialCredit(commands.Cog, name="Social Credit"):
    PATTERNS = [
        ['glory (to |for )(the )?(ccp|chinese|china|communism)', 10],
        ['(all )?hail (the )?ccp', 10],
        ['((all )?(praise|hail) (to )?|i love)(xi|xi jinping|mao|mao zhedong)', 10],
        ['i love china', 10],
        ['china num(ber|bah|) (one|1)($|\s)', 10],
        ['comrade', 5],
        ['taiwan', -10],
        ['corona', -10],
        [f'@&{config.LEAGUE_ROLE}', -15],
        ['(winnie the )?pooh', -20],
        ['wuhan', -20],
        ['(china|chinese) virus', -20],
        ['ti[a@]n[a@]nmen square', -30],
        ['fr[e3][e3] h[o0]ng k[o0]ng', -30],
    ]
    
    GOOD = 'Good work comrade! +{} social credit score!'
    BAD = 'Not acceptable! {} social credit score!'
    
    BOT_CHANNEL = re.compile('^(|.*[^a-z])(bot)(|[^a-z].*)$', re.IGNORECASE)
    
    def __init__(self, bot):
        self.bot = bot
        self.collection = bot.database.socialcredit

    @commands.command(brief="Check social credit score")
    @commands.guild_only()
    async def credit(self, ctx: commands.Context, user: discord.Member = None):
        user: discord.Member = user or ctx.author
        record = self.collection.find_one_and_update(
            {'user_id': user.id, 'guild_id': ctx.guild.id},
            {'$setOnInsert': {'count': 0}},
            upsert=True, return_document=ReturnDocument.AFTER)

        await self.show(ctx, user, record['count'])
        
    @commands.Cog.listener()
    async def on_nocommand(self, message: discord.Message):
        if message.author.bot or message.guild == None:
            return
        
        
        # check patterns
        for (pattern, score) in self.PATTERNS:
            if re.search(pattern, message.content, re.IGNORECASE):
                await self.add_credit(message, score)
                return
        
        # check for gif-posting
        try:
            url = urlparse(message.content)
        except ValueError:
            pass
        else:
            if url and url.hostname == 'tenor.com':
                await self.add_credit(message, -30)
                return
                
    async def add_credit(self, message: discord.Message, score: int):
        self.collection.find_one_and_update(
            {'user_id': message.author.id, 'guild_id': message.guild.id},
            {'$inc': {'count': score}},
            upsert=True, return_document=ReturnDocument.AFTER)
            
        if (score > 0):
            await message.reply(self.GOOD.format(score), delete_after=config.MESSAGE_TIMER)
        else:
            await message.reply(self.BAD.format(score), delete_after=config.MESSAGE_TIMER)

        bot_channel = self.BOT_CHANNEL.match(message.channel.name)
        if bot_channel:
            await message.delete()
        
    def format_user_count(self, name: str, count: int):
        plural = 's' if count != 1 else ''
        return f"{name}'s social credit score is {count}"

    async def show(self, ctx: commands.Context, user: discord.Member, count: int):
        await ctx.send(self.format_user_count(await utils.get_nickname(self.bot, ctx.guild, user.id), count))
