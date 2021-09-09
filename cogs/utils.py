import discord
from discord.ext import commands, tasks
from itertools import cycle
from datetime import datetime

from config import ID1, ID2, ACTIVITY_STATUS, DEFAULT_EMBED_COLOR, DEFAULT_PREFIX


class Utilis(commands.Cog):
    """
    some essential utility for bot
    """

    def __init__(self, client: discord.Client):
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
        activity = discord.Activity(
            type=discord.ActivityType.watching, name=next(self.status)
        )
        await self.client.change_presence(activity=activity)

    @commands.command()
    async def uptime(self, ctx: commands.Context):
        for id in self.owner_id:
            if ctx.message.author.id == id:
                delta_uptime = datetime.utcnow() - self.client.launch_time
                hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)
                days, hours = divmod(hours, 24)
                uptime_embed = discord.Embed(
                    title=f"Online since: {days}d, {hours}h, {minutes}m, {seconds}s",
                    colour=self.embed_color,
                )
                await ctx.send(embed=uptime_embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.content == f"<@!{self.client.user.id}>":
            channel: discord.TextChannel = message.channel
            await channel.send(
                f"Hello, my prefix for this server is {DEFAULT_PREFIX} or <@!{self.client.user.id}>"
            )

    @commands.command()
    async def invite(self, ctx: commands.Context):
        invite_url = f"https://discord.com/api/oauth2/authorize?client_id={str(self.client.user.id)}&permissions=8&scope=bot"

        invite_embed = discord.Embed(
            title="Invite me 🥳",
            color=self.embed_color,
            description=f"Click [here]({invite_url}) to invite me.",
        )
        await ctx.send(embed=invite_embed)


def setup(client):
    client.add_cog(Utilis(client))
