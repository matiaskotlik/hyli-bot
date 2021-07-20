import asyncio
import config
import discord
import utils
from discord.ext import commands


def setup(bot: commands.Bot):
    bot.add_cog(Camel(bot))


class Camel(commands.Cog, name="Camel"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(brief="Accidently send someone a sexy camel")
    async def camel(self, ctx: commands.Context, user: discord.Member = None):
        await utils.try_delete_cmd(ctx)
        if user:
            await ctx.send("Sending camel...", delete_after=config.MESSAGE_TIMER)

            await user.send(file=discord.File(config.CAMEL))
            await asyncio.sleep(5)
            async with user.typing():
                await asyncio.sleep(3)
            await user.send("Sorry wrong person")
        else:
            await ctx.send("Who do you want to send the camel to?", delete_after=config.MESSAGE_TIMER)
