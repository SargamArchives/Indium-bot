from datetime import datetime

import discord
from Config.config import DEFAULT_EMBED_COLOR, DEFAULT_PREFIX
from discord.ext import commands
from Utils.helpers.helper import check_owner


class Utilis(commands.Cog):
    """
    some essential utility for bot
    """

    def __init__(self, client: discord.Client):
        self.client = client
        client.launch_time = datetime.utcnow()
        self.embed_color = DEFAULT_EMBED_COLOR

    @commands.command()
    @commands.check(check_owner)
    async def uptime(self, ctx: commands.Context) -> None:
        delta_uptime = datetime.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        uptime_embed = discord.Embed(
            title=f"Online since: {days}d, {hours}h, {minutes}m, {seconds}s",
            colour=self.embed_color,
        )
        await ctx.send(embed=uptime_embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.content == f"<@!{self.client.user.id}>":
            channel: discord.TextChannel = message.channel
            await channel.send(
                f"Hello, my prefix for this server is {DEFAULT_PREFIX} or <@!{self.client.user.id}>"
            )

    @commands.command()
    async def invite(self, ctx: commands.Context):
        invite_url = f"https://discord.com/api/oauth2/authorize?client_id={str(self.client.user.id)}&permissions=8&scope=bot"
        invite_embed = discord.Embed(
            title="Invite me 🥳",
            color=self.embed_color,
            description=f"Click [here]({invite_url}) to invite me.",
        )
        await ctx.send(embed=invite_embed)


def setup(client):
    client.add_cog(Utilis(client))
