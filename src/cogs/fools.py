from discord.channel import TextChannel
import config
import discord
import utils
from discord.ext import commands


def setup(bot: commands.Bot):
    bot.add_cog(Fools(bot))


class Fools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.disabled = False
        self.message = '''{mention}, your message does not comply with our updated server policies.
Continued violation of our rules will result in a PERMANENT BAN. As a reminder, your message must end with "I LOVE LEAGUE OF LEGENDS".

*I am a bot, and this action was performed automatically.*

I LOVE LEAGUE OF LEGENDS'''

    @commands.Cog.listener()
    async def on_nocommand(self, message: discord.Message):
        if self.disabled:
            return
        if not isinstance(message.channel, discord.TextChannel):
            return
        if message.channel.name != 'general':
            return
        if utils.filter_line(message.content).endswith('iloveleagueoflegends'):
            return
        await utils.try_delete(message)
        await message.channel.send(self.message.format(mention=message.author.mention), delete_after=8)

    @commands.command()
    async def disable_very_smoge_secret_command(self, ctx: commands.Context):
        self.disabled = True
        await ctx.send('New policy has been reverted. Sadge D:')