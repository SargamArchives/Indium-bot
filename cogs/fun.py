import discord
from discord.ext import commands

from random import randrange
from datetime import date
from typing import Optional, Union

from config import DEFAULT_EMBED_COLOR


class Fun(commands.Cog):
    """
    Some Fun commands
    """

    def __init__(self, client) -> None:
        self.client = client
        self.embed_color = DEFAULT_EMBED_COLOR

    @commands.command()
    async def pp(self, ctx, user: Optional[discord.Member] = None) -> None:
        if user is None:
            user = ctx.author
        pp_str = ["8", "", "D"]
        pp_str[-2] = "".join(["=" for _ in range(randrange(1, 10))])
        pp_str = "".join(pp_str)
        pp_embed = discord.Embed(
            title="PP size machine",
            description=f"{user.name}'s pp size:\n {pp_str}",
            colour=self.embed_color,
        )
        await ctx.send(embed=pp_embed)

    


def setup(client):
    client.add_cog(Fun(client))
