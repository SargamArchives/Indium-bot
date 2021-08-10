import discord
from discord import message
from discord.ext import commands, tasks
from itertools import cycle


class Utilis(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.status = cycle(
            ["minecraft",
             "among us"]
        )

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print("Logged in as bot")

    @tasks.loop(seconds=5)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(self.status)))


def setup(client):
    client.add_cog(Utilis(client))