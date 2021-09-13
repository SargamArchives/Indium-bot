from io import BytesIO

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands.core import command

from config import DEFAULT_EMBED_COLOR


class Emoji(commands.Cog):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
        self.embed_color = DEFAULT_EMBED_COLOR

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def createemoji(self, ctx: commands.Context, url: str, *, name: str) -> None:
        guild = ctx.guild
        if ctx.author.guild_permissions.manage_emojis:
            async with aiohttp.ClientSession() as ses:
                async with ses.get(url) as r:

                    try:
                        img_or_gif = BytesIO(await r.read())
                        b_value = img_or_gif.getvalue()
                        if r.status in range(200, 299):
                            emoji = await guild.create_custom_emoji(
                                image=b_value, name=name
                            )
                            embed = discord.Embed(
                                title="Successfully created emoji",
                                description=f"<:{name}:{emoji.id}>",
                                color=self.embed_color
                            )
                            await ctx.send(embed=embed)
                            await ses.close()
                        else:
                            await ctx.send(
                                f"Error when making request | {r.status} response."
                            )
                            await ses.close()

                    except discord.HTTPException:
                        await ctx.send("File size is too big!")

    @commands.command()
    async def delete_emoji(self, ctx: commands.Context, emoji: discord.Emoji) -> None:
        await ctx.send(f"Deleted: {emoji}")
        await emoji.delete()


def setup(client):
    client.add_cog(Emoji(client))
