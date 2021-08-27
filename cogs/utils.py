import discord
from discord.ext import commands, tasks
from itertools import cycle
from datetime import datetime
from config import ID1, ID2, ACTIVITY_STATUS, DEFAULT_EMBED_COLOR


class Utilis(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.status = cycle(ACTIVITY_STATUS)
        client.launch_time = datetime.utcnow()
        self.owner_id = [ID1, ID2]
        self.embed_color = DEFAULT_EMBED_COLOR

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print("Logged in as bot")

    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(self.status)))

    @commands.command()
    async def uptime(self, ctx):
        for id in self.owner_id:
            if ctx.message.author.id == id:
                delta_uptime = datetime.utcnow() - self.client.launch_time
                hours, remainder = divmod(
                    int(delta_uptime.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)
                days, hours = divmod(hours, 24)
                uptime_embed = discord.Embed(title=f"Online since: {days}d, {hours}h, {minutes}m, {seconds}s",
                                             colour=self.embed_color
                                             )
                await ctx.send(embed=uptime_embed)


def setup(client):
    client.add_cog(Utilis(client))
