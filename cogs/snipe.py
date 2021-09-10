import discord
from  discord.ext import commands

from asyncio import sleep

from config import DEFAULT_EMBED_COLOR

class Snipe(commands.Cog):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
        self.embed_color = DEFAULT_EMBED_COLOR
        self.snipable_message = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot: 
            return

        self.snipable_message[message.channel.id] = message
        await sleep(120)
        del self.snipable_message[message.channel.id]

    @commands.command(alias=["s"])
    async def snipe(self, ctx: commands.Context):
        snipe_embed = discord.Embed(
            color=self.embed_color,
        )
        try:
            message: discord.Message = self.snipable_message[ctx.channel.id]
        except KeyError:
            snipe_embed.add_field(name="Message Deleted", value="There's nothing to snipe!")
            await ctx.send(embed=snipe_embed)
            snipe_embed.remove_field()
            return
        member: discord.Member = message.author
        snipe_embed.set_author(name=f"{message.author.display_name}#{message.author.discriminator}", icon_url=f"{member.avatar_url}")
        snipe_embed.add_field(name="Message Deleted", value=f"{message.content}")
        await ctx.send(embed=snipe_embed)


def setup(client):
    client.add_cog(Snipe(client))