import re

import config
import discord
import tweepy
import tweepy.asynchronous
import utils
from discord.ext import commands


def setup(bot: commands.Bot):
    bot.add_cog(Simp(bot))

class Simp(commands.Cog, name="Simp"):
    USERS = [
        617815341, # floaromaa
        3361070973, # juliamajch
        306539878, # yeonari_
        4194407652, # plooful
        785927446310719488, # yoojpls
    ]
    SIMP_PATTERN = re.compile(r'^(|.*[^a-z])simp(ing)?(|[^a-z].*)$', re.IGNORECASE)
    def __init__(self, bot):
        self.bot = bot
        self.stream = ForwardingStream(
            config.TWITTER_API_KEY, config.TWITTER_API_KEY_SECRET,
            config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET,
            callback=self.on_twitter_event
        )
        self.last_post = None
        self.stream.filter(follow=self.USERS)
        # self.stream.filter(track=["art"]) # for testing
        self.channels: list[discord.TextChannel] = []
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.channels = [
            channel 
            for guild in self.bot.guilds 
            for channel in guild.text_channels if self.SIMP_PATTERN.match(channel.name)
        ]
        
    async def on_twitter_event(self, tweet):
        # no replies
        if tweet.in_reply_to_status_id:
            return
        
        # no rt's
        if tweet.is_quote_status:
            return
        
        # only if has media
        if 'media' not in tweet.entities:
            return
        
        if self.last_post == tweet.id_str:
            return
        else:
            self.last_post = tweet.id_str
        
        tweet_url = f'http://twitter.com/simp/status/{tweet.id_str}'
        
        for channel in self.channels:
            await channel.send(tweet_url)

class ForwardingStream(tweepy.asynchronous.AsyncStream):
    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop('callback')
        super().__init__(*args, **kwargs)
        
    async def on_status(self, status):
        await self.callback(status)
