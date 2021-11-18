import json
from random import choice, randrange
from typing import Optional

import discord
from Config.config import DEFAULT_EMBED_COLOR
from discord.ext import commands


class Fun(commands.Cog):
    """
    Some Fun commands
    """

    def __init__(self, client) -> None:
        self.client = client
        self.embed_color = DEFAULT_EMBED_COLOR
        with open("discord_bot/Utils/data/gifs.json", "r") as gifs:
            links = json.load(gifs)
        self.hug = links["hug"]
        self.kill = links["kill"]
        self.pat = links["pat"]
        self.lick = links["lick"]

    @commands.command()
    async def pp(self, ctx: commands.Context, user: Optional[discord.Member]) -> None:
        user = user or ctx.author
        pp_str = ["8", "", "D"]
        pp_str[-2] = "".join(["=" for _ in range(randrange(1, 10))])
        pp_str = "".join(pp_str)
        pp_embed = discord.Embed(
            title="PP size machine",
            description=f"{user.name}'s pp size:\n {pp_str}",
            colour=self.embed_color,
        )
        await ctx.send(embed=pp_embed)

    @commands.command()
    async def hug(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if member is not None:
            caption = f"{ctx.author.mention} hugged {member.mention}"
        else:
            caption = f"{ctx.author.mention} hugged themselves! 🤔"
        hug_embed = discord.Embed(color=self.embed_color, description=caption)
        hug_embed.set_image(url=choice(self.hug))
        await ctx.send(embed=hug_embed)

    @commands.command()
    async def pat(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if member is not None:
            caption = f"{ctx.author.mention} patted {member.mention}"
        else:
            caption = f"{ctx.author.mention} patted themselves! 🤔"
        pat_embed = discord.Embed(color=self.embed_color, description=caption)
        pat_embed.set_image(url=choice(self.pat))
        await ctx.send(embed=pat_embed)

    @commands.command()
    async def kill(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if member is not None:
            caption = f"{ctx.author.mention} killed {member.mention}! RIP"
        else:
            caption = f"{ctx.author.mention} killed themselves! 🤔"
        kill_embed = discord.Embed(color=self.embed_color, description=caption)
        kill_embed.set_image(url=choice(self.kill))
        await ctx.send(embed=kill_embed)

    @commands.command(help="Licks")
    async def lick(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if member is not None:
            caption = f"{ctx.author.mention} licked {member.mention}"
        else:
            caption = f"{ctx.author.mention} licked themselves! 🤔"
        lick_embed = discord.Embed(color=self.embed_color, description=caption)
        lick_embed.set_image(url=choice(self.lick))
        await ctx.send(embed=lick_embed)


def setup(client):
    client.add_cog(Fun(client))
