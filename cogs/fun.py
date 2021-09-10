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

    @commands.command()
    async def date(self, ctx: commands.context) -> None:
        await ctx.reply(date.today())

    @commands.command()
    async def device(
        self,
        ctx: commands.Context,
        user: Optional[Union[discord.Member, discord.User]] = None,
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

    @commands.command(name="serverinfo")
    async def server_info(self, ctx: commands.Context):
        guild: discord.Guild = ctx.guild
        name = guild.name
        owner = guild.owner
        server_icon = guild.icon_url
        catagories = len(guild.categories)
        text_channel = len(guild.text_channels)
        voice_channel = len(guild.voice_channels)
        members = guild.member_count
        id = guild.id
        created_at = guild.created_at.date()
        roles = len(guild.roles)
        embed = discord.Embed(color=self.embed_color)
        embed.set_author(name=f"{name}", icon_url=f"{server_icon}")
        embed.add_field(name="Server Owner", value=f"{owner}")
        embed.add_field(name="Channel Categories", value=f"{catagories}")
        embed.add_field(name="Text Channels", value=f"{text_channel}")
        embed.add_field(name="Voice Channels", value=f"{voice_channel}")
        embed.add_field(name="Member count", value=f"{members}")
        embed.add_field(name="Role count", value=f"{roles}")
        embed.set_thumbnail(url=server_icon)
        embed.set_footer(text=f"ID: {id} | Server Created at • {created_at}")
        await ctx.send(embed=embed)

    @commands.command(name="whois")
    async def who_is(self, ctx: commands.Context, member: Optional[discord.Member]):
        user = member or ctx.author
        permissions_filter = [
            "Administrator",
            "Manage Server",
            "Manage Roles",
            "Manage Channels",
            "Manage Messages",
            "Manage Webhooks",
            "Manage Nicknames",
            "Manage Emojis",
            "Kick Members",
            "Ban Members",
            "Mention Everyone",
        ]

        role = [role.mention for role in user.roles][1:]
        roles = " ".join(role)
        guild_permission = [
            (" ".join(permission[0].split("_"))).title()
            for permission in user.guild_permissions
            if permission[1]
        ]
        key_permissions = [
            perms for perms in guild_permission if perms in permissions_filter
        ]
        key_permissions = ", ".join(key_permissions)
        if user == ctx.guild.owner:
            acknowledgements = "Server Owner"
        elif "Administrator" in guild_permission:
            acknowledgements = "Administrator"
        elif "Manage Guild" in guild_permission:
            acknowledgements = "Moderator"
        else:
            acknowledgements = "Member"
        embed = discord.Embed(description=f"{user.mention}", color=self.embed_color)
        embed.set_author(
            name=f"{user.name}#{user.discriminator}", icon_url=f"{user.avatar_url}"
        )
        embed.set_thumbnail(url=f"{user.avatar_url}")

        embed.add_field(name="Joined at", value=f"{user.joined_at.date()}")
        embed.add_field(name="Registered", value=f"{user.created_at.date()}")

        embed.add_field(name=f"Roles {len(user.roles) - 1}", value=roles, inline=False)
        embed.add_field(
            name=f"Key User Permissions", value=key_permissions, inline=False
        )
        embed.add_field(name="Acknowledgement", value=acknowledgements, inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
