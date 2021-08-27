import discord
from discord.ext import commands

from asyncio import sleep

from config import DEFAULT_EMBED_COLOR


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = (client,)
        self.embed_color = DEFAULT_EMBED_COLOR

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(
        self,
        ctx: commands.Context,
        user: discord.Member,
        *,
        reason="No reason provided",
    ):

        await user.kick(reason=reason)
        kick = discord.Embed(
            title=f":boot: Kicked {user.display_name}!",
            description=f"Reason: {reason}\nBy: {ctx.author.mention}",
            colour=self.embed_color,
        )
        await ctx.message.delete()
        await ctx.channel.send(embed=kick)
        await user.send(embed=kick)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context,
        user: discord.Member,
        *,
        reason: str = "No reason Provided",
    ):

        await user.ban(reason=reason)
        ban = discord.Embed(
            title=f":hammer: Banned {user.name}!",
            description=f"Reson: {reason}\nBy: {ctx.author.mention}",
            colour=self.embed_color,
        )
        message = await ctx.send(embed=ban)
        await user.send(embed=ban)
        await sleep(10)
        await message.delete()

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: int):
        if amount < 1:
            return
        await ctx.channel.purge(limit=amount + 1)
        purge = discord.Embed(
            title=f"Message deleted",
            description=f"{amount} message deleted by {ctx.author.mention}",
            colour=self.embed_color,
        )
        message = await ctx.channel.send(embed=purge)
        await sleep(10)
        await message.delete()


def setup(client):
    client.add_cog(Moderation(client))
