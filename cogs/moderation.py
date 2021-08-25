import discord
from discord import channel
from discord.ext import commands
from asyncio import sleep

from discord.ext.commands import context


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        kick = discord.Embed(
            title=f":boot: Kicked {user.display_name}!",
            description=f"Reason: {reason}\nBy: {ctx.author.mention}"
        )
        await ctx.message.delete()
        await ctx.channel.send(embed=kick)
        await user.send(embed=kick)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, user: discord.Member, *, reason="No reason Provided"):
        await user.ban(reason=reason)
        ban = discord.Embed(
            title=f":hammer: Banned {user.name}!",
            description=f"Reson: {reason}\nBy: {ctx.author.mention}"
        )
        message = await ctx.send(embed=ban)
        await user.send(embed=ban)
        await sleep(10)
        await message.delete()

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context,  amount: int):
        if amount < 1:
            return
        await ctx.channel.purge(limit=amount + 1)
        purge = discord.Embed(
            title=f"Message deleted",
            description=f"{amount} message deleted by {ctx.author.mention}"
        )
        message = await ctx.channel.send(embed=purge)
        await sleep(5)
        await message.delete()


def setup(client):
    client.add_cog(Moderation(client))
