import config
import discord
import utils
import datetime
from discord.ext import commands

def setup(bot: commands.Bot):
    bot.add_cog(Undelete(bot))

class Undelete(commands.Cog, name="Message Undeleter"):
    def __init__(self, bot):
        self.bot = bot
        self.log = []
        self.expire = datetime.timedelta(seconds = 15)

    def format_message(self, message: discord.Message) -> str:
        return f"{message.author.display_name}: {message.content}"
    
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return
        self.clean_log()
        self.log.append((datetime.datetime.now(), self.format_message(message)))
    
    def clean_log(self):
        now = datetime.datetime.now()
        self.log = [(date, message) for date, message in self.log if (now <= date + self.expire)]

    @commands.command(brief="Undeletes a message, temporarily")
    async def undelete(self, ctx: commands.Context):
        self.clean_log()
        if not self.log:
            await ctx.reply("Nothing here. Maybe check back later?", delete_after=config.MESSAGE_TIMER)
            return
        for _, message in self.log:
            await ctx.send(message, delete_after=config.MESSAGE_TIMER)

