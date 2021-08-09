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

    @commands.command()
    async def ping(self, ctx):
        ping = 1000 * self.client.latency
        await ctx.send(f"Pong! {ping}")

    @commands.command(name="av")
    async def avatar(self, ctx, user: discord.Member = None):
        if user == None: user = ctx.author
        avatar_embed = discord.Embed(
            title=f"{user.name}#{user.discriminator}\nAvatar"
        )
        avatar_embed.set_image(url=user.avatar_url)
        await ctx.send(embed=avatar_embed)

def setup(client):
    client.add_cog(Utilis(client))