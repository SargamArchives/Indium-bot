import discord
from discord.ext import commands


class HelpCommand(commands.HelpCommand):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
