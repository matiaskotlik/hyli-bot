from dataclasses import dataclass
import datetime
import collections

import config
import discord
from discord.ext import commands

@dataclass
class LoggedMessage:
    channel: int
    date: datetime.datetime
    text: str

    @classmethod
    def from_message(cls, message: discord.Message):
        channel = message.channel.id
        now = datetime.datetime.now()
        text = f"{message.author.display_name}: {message.content}"
        return LoggedMessage(channel, now, text)

def setup(bot: commands.Bot):
    bot.add_cog(Undelete(bot))

class Undelete(commands.Cog, name="Message Undeleter"):
    def __init__(self, bot):
        self.bot = bot
        self.log = []
        self.expire = datetime.timedelta(seconds = 30)
    
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return
        self.clean_log()
        self.log.append(LoggedMessage.from_message(message))

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.author.bot:
            return
        if before.content == after.content:
            return
        self.clean_log()
        self.log.append(LoggedMessage.from_message(before))
    
    def clean_log(self):
        now = datetime.datetime.now()
        self.log = [msg for msg in self.log if (now <= msg.date + self.expire)]

    @commands.command(brief="Undeletes a message")
    async def undelete(self, ctx: commands.Context):
        self.clean_log()
        messages = [msg for msg in self.log if (ctx.channel.id == msg.channel)]
        if not messages:
            await ctx.reply("Nothing here. Maybe check back later?", delete_after=config.MESSAGE_TIMER)
            return
        for message in messages:
            await ctx.send(message.text)