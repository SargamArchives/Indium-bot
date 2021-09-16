from typing import Optional

import discord
from discord.ext import commands

from Config.config import DEFAULT_EMBED_COLOR


class GuildInfo(commands.Cog):
    """
    Some commands useful for guild
    """

    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
        self.embed_color = DEFAULT_EMBED_COLOR

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


def setup(client):
    client.add_cog(GuildInfo(client))
