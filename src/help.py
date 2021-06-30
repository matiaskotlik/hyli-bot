import discord
from discord.ext import commands

class HelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()

    async def command_callback(self, ctx, *, command=None):
        await self.prepare_help_command(ctx, command)
        mapping = self.get_bot_mapping()
        return await self.send_bot_help(mapping)

    def get_ending_note(self):
        return ""