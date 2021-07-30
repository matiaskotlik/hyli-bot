from pathlib import Path

from discord.ext.commands.core import Command
import config
import discord
import utils
from discord.ext import commands


def setup(bot: commands.Bot):
    bot.add_cog(Banger(bot))


class Banger(commands.Cog, name="Meme Generator"):
    def __init__(self, bot):
        self.bot = bot
        self.bindings = [
            ('hush', config.HUSH), 
            ('awesome', config.AWESOME), 
            ('mad', config.MAD), 
            ('banger', config.BANGER), 
            ('nerd', config.NERD)
        ]
        for name, image_path in self.bindings:
            self.add_binding(name, image_path)

    def add_binding(self, name: str, image: Path):
        async def func(self, ctx):
            await self.send_image(ctx, image)
        command = Command(func=func, name=name, brief=f"Sends a {name.capitalize()}")
        command.cog = self
        self.bot.add_command(command)

    async def send_image(self, ctx: commands.Context, image: Path):
        await utils.try_delete_cmd(ctx)
        try:
            message = await utils.get_implied_message(ctx, False)
        except commands.BadArgument:
            message = None
        await ctx.send(file=discord.File(image), reference=message)
