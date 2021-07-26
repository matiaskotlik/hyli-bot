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
    @commands.guild_only()
    async def camel(self, ctx: commands.Context, user: discord.User):
        await utils.try_delete_cmd(ctx)
        if ctx.guild.get_member(user.id) is None:
            await ctx.send("That user isn't in this server", delete_after=config.MESSAGE_TIMER)
            return

        await ctx.send("Sending camel...", delete_after=config.MESSAGE_TIMER)

        await self.send_camel(user)

    async def send_camel(self, user: discord.User):
        await user.send(file=discord.File(config.CAMEL))
        await asyncio.sleep(5)
        async with user.typing():
            await asyncio.sleep(3)
        await user.send("Sorry wrong person")
