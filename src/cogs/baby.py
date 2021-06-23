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
    async def baby(self, ctx: commands.Context, *args):
        name = commands.clean_content(' '.join(args) or 'Violet')
        sections = []
        for role in self.family:
            section = []
            line = f'{role} {name}, ' + ', '.join(['doo'] * self.doos)
            for _ in range(self.repetitions):
                section.append(line)

            section.append(f'{role} {name}!')
            sections.append('\n'.join(section))

        try:
            await ctx.send('\n\n'.join(sections))
        except HTTPException:
            await ctx.reply(config.SEND_ERROR)

