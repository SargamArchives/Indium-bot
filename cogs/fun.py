import discord
from discord.ext import commands

from random import randrange
from datetime import date
from typing import Optional

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

    @commands.command()
    async def date(self, ctx: commands.context) -> None:
        await ctx.reply(date.today())

    @commands.command()
    async def device(
        self, ctx: commands.Context, user: Optional[discord.Member] = None
    ) -> None:
        if user is None:
            user = ctx.author
        comp_status = user.desktop_status
        mobile_status = user.mobile_status
        web_status = user.web_status

        embed = discord.Embed(
            title=f"{user.display_name}'s device status", colour=self.embed_color
        )
        embed.add_field(name="PC client", value=f"💻: {comp_status}", inline=True)
        embed.add_field(name="Web client", value=f"🌏: {web_status}", inline=False)
        embed.add_field(name="Mobile client", value=f"📱: {mobile_status}", inline=False)

        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
