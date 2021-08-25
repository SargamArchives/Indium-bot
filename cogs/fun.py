import asyncio
import re
import discord
from discord import colour
from discord.ext import commands
from random import randrange
from datetime import date
from discord.ext.commands import context
from discord.ext.commands.context import Context
from discord.ext.commands.core import command
import time
from discord.ext.commands.errors import DisabledCommand
from multidict import CIMultiDict


class Fun(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @commands.command()
    async def pp(self, ctx, user: discord.Member = None) -> None:
        if user is None:
            user = ctx.author
        pp_str = "8"
        for _ in range(randrange(10)):
            pp_str += "="
        pp_str += "D"
        pp_embed = discord.Embed(
            title="PP size machine",
            description=f"{user.name}'s pp size:\n {pp_str}"
        )
        await ctx.send(embed=pp_embed)

    @commands.command()
    async def date(self, ctx: commands.context) -> None:
        await ctx.reply(date.today())

    @commands.command()
    async def device(self, ctx: commands.context, user: discord.Member = None) -> None:
        if user is None:
            user = ctx.author
        comp_status = user.desktop_status   
        mobile_status = user.mobile_status
        web_status = user.web_status
        
        embed = discord.Embed(
            title = f"{user.display_name}'s device status",
            colour = 0x01a6ff,
        )

        embed.add_field(
            name = "PC client", 
            value = f"💻: {comp_status}",
            inline =True)

        embed.add_field(
            name = "Web client", 
            value = f"🌏: {web_status}",
            inline = False)

        embed.add_field(
            name = "Mobile client", 
            value = f"📱: {mobile_status}",
            inline = False)

        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed = embed)
        
        
def setup(client):
    client.add_cog(Fun(client))