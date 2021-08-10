import discord
from discord.ext import commands
from random import randrange

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pp(self, ctx, user: discord.Member = None):
        if user == None: user = ctx.author
        pp_str = "8"
        for _ in range(randrange(10)):
            pp_str += "="
        pp_str += "D"
        pp_embed = discord.Embed(
            title="PP size machine",
            description=f"{user.name}'s pp size:\n {pp_str}"
        )
        await ctx.send(embed=pp_embed)

def setup(client):
    client.add_cog(Fun(client))
