
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
        for valid_ids, pattern, reactions in config.REACTS:
            # valid_ids = None means any user is fine for this reaction
            if valid_ids and message.author.id not in valid_ids: 
                continue

            if not pattern.search(message.content):
                continue

            for r in reactions:
                try:
                    await message.add_reaction(r)
                except discord.HTTPException:
                    # emoji does not exist in this server
                    if message.guild:
                        print(f'Tried to react with invalid emoji {r} in server {message.guild.name}')
                except discord.Forbidden:
                    # permissions issue
                    error = True
        
        if error:
            message.channel.send(config.NO_PERMISSIONS)

