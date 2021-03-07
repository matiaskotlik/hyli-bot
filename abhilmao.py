
import discord
from discord import permissions
from discord.ext import commands

import config


def setup(bot: commands.Bot):
    bot.add_cog(Abhilmao(bot))


class Abhilmao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.content:
            return 

        error = False
        for user_id, regex, reaction in config.REACTS:
            if user_id == message.author.id and regex.match(message.content):
                try:
                    await message.add_reaction(reaction)
                except discord.HTTPException:
                    # emoji does not exist in this server
                    pass
                except discord.Forbidden:
                    # permissions issue
                    error = True
        
        if error:
            message.channel.send(config.NO_PERMISSIONS)

