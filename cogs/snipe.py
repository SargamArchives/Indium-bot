from asyncio import sleep

import discord
from discord.ext import commands

from Config.config import DEFAULT_EMBED_COLOR


class Snipe(commands.Cog):
    """Cog that takes care of stuff that is related to sniped and edited messages"""
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
        self.embed_color = DEFAULT_EMBED_COLOR
        self.snipable_message = {}
        self.edited_message = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        print(message.content)
        self.snipable_message[message.channel.id] = message

        await sleep(120)
        del self.snipable_message[message.channel.id]

    @commands.Cog.listener()
    async def on_message_edit(
        self, before: discord.Message, after: discord.Message
    ) -> None:
        channel_id = before.channel.id
        self.edited_message[channel_id] = [before, after]
        await sleep(120)
        del self.edited_message[channel_id]

    @commands.command()
    async def edit(self, ctx: commands.Context) -> None:
        edit_embed = discord.Embed(color=self.embed_color)
        try:
            messages = self.edited_message[ctx.channel.id]
        except KeyError:
            edit_embed.add_field(name="Message Edit", value="There's nothing edited!")
            await ctx.send(embed=edit_embed)
            return
        before, after = messages
        author: discord.Member = messages[0].author
        edit_embed.set_author(
            name=f"{author.display_name}#{author.discriminator}",
            icon_url=author.avatar_url,
        )
        edit_embed.add_field(
            name=f"Message Edited\n\nBefore:", value=before.content, inline=False
        )
        edit_embed.add_field(name=f"After:", value=after.content, inline=False)
        await ctx.send(embed=edit_embed)

    @commands.command()
    async def snipe(self, ctx: commands.Context) -> None:
        snipe_embed = discord.Embed(
            color=self.embed_color,
        )
        try:
            message: discord.Message = self.snipable_message[ctx.channel.id]
        except KeyError:
            snipe_embed.add_field(
                name="Message Deleted", value="There's nothing to snipe!"
            )
            await ctx.send(embed=snipe_embed)
            return
        member: discord.Member = message.author
        snipe_embed.set_author(
            name=f"{message.author.display_name}#{message.author.discriminator}",
            icon_url=f"{member.avatar_url}",
        )
        snipe_embed.add_field(name="Message Deleted", value=f"{message.content}")
        await ctx.send(embed=snipe_embed)


def setup(client):
    client.add_cog(Snipe(client))
