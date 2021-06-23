import config
import discord
import utils
from discord.ext import commands


def setup(bot: commands.Bot):
    bot.add_cog(Banger(bot))


class Banger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.doos = 6
        self.family = [
            'Baby',
            'Mommy',
            'Daddy',
            'Grandma',
            'Grandpa',
        ]
        self.repetitions = 3
    
    @commands.command()
    @commands.guild_only()
    async def baby(self, ctx: commands.Context, name: str = 'Violet'):
        lines = []
        for role in self.family:
            line = f'{role} {name}, ' + ', '.join(['doo'] * self.doos)
            for _ in self.repetitions:
                lines.append(line)

            lines.append(f'{role} {name}!')
        ctx.send('\n'.join(lines))

