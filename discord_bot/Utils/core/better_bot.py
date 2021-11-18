import logging
from itertools import cycle
from typing import Optional

import discord
from Config.config import ACTIVITY_STATUS, DEFAULT_PREFIX
from discord.ext import commands, tasks
from Utils.help_command import HelpCommand


class IndiumBot(commands.Bot):
    def __init__(self, load_jishaku: Optional[bool] = True):
        super().__init__(
            command_prefix=self.return_prefix(),
            intents=discord.Intents.all(),
            help_command=None,
            description="description",
            case_insensitive=True,
        )
        self._extensions = [
            "cogs.utils",
            "cogs.guild",
            "cogs.error",
            "cogs.moderation",
            "cogs.emoji",
            "cogs.fun",
            "cogs.misc",
            "cogs.snipe",
            "dch",
        ]
        if load_jishaku:
            self._extensions.append("jishaku")
        self._status = cycle(ACTIVITY_STATUS)
        self._load_extension()

    def return_prefix(self) -> None:
        return commands.when_mentioned_or(DEFAULT_PREFIX)

    @tasks.loop(seconds=10)
    async def change_status(self) -> None:
        self.next_status = discord.Activity(
            type=discord.ActivityType.watching, name=next(self._status)
        )
        await self.change_presence(activity=self.next_status)

    def _load_extension(self) -> None:
        for ext in self._extensions:
            self.load_extension(ext)

    async def on_ready(self):
        self.change_status.start()
        print(f"Logged in as {self.user.name}#{self.user.discriminator}")
