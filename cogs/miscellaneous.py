import discord
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        ping = 1000 * self.client.latency
        await ctx.send(f"Pong! {ping}")


def setup(client):
    client.add_cog(Fun(client))
