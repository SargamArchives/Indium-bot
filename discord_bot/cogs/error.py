import traceback
from asyncio import sleep

import discord
from Config.config import DEFAULT_EMBED_COLOR
from discord.ext import commands
from discord.ext.commands.errors import (BadArgument, BotMissingPermissions,
                                         CommandNotFound, MissingPermissions,
                                         MissingRequiredArgument, MissingRole)


class Error(commands.Cog):
    """
    Error handler for bot commands
    """

    def __init__(self, client: commands.Bot) -> None:
        super().__init__()
        self.client = (client,)
        self.embed_color = DEFAULT_EMBED_COLOR

    @commands.Cog.listener()
    async def on_command_error(
        self,
        ctx: commands.Context,
        error: commands.CommandError,
    ) -> None:
        if isinstance(error, CommandNotFound):
            return

        if isinstance(error, BadArgument):
            message = await ctx.send("Please supply correct arguments ✅")
            await sleep(5)
            await message.delete()

        if isinstance(error, MissingRequiredArgument):
            message = await ctx.send("Please pass all required arguments ✅")
            await sleep(5)
            await message.delete()

        if isinstance(error, MissingPermissions):
            message = await ctx.send("You are missing role permissions")
            await sleep(5)
            await message.delete()

        if isinstance(error, BotMissingPermissions):
            error_embed = discord.Embed(
                description="❎ I don't have permissions to Manage Messages.",
                colour=self.embed_color,
            )
            await ctx.send(embed=error_embed)

        if isinstance(error, MissingRole):
            await ctx.send(
                "❎ You are missing role permissions good sir.", delete_after=5
            )

        else:
            await ctx.send("An unknown error occured.", delete_after=5.0)
            await ctx.send(error, delete_after=5.0)
            print(traceback.print_exc)


def setup(client):
    client.add_cog(Error(client))
