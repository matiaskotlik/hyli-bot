
import discord
from discord.ext import commands

import config


class Abhilmao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        content = message.content
        if message.author.id == config.ABHISHEK and content and content.strip().lower() == 'lmao':
            await message.add_reaction(config.ABHI_LMAO)
