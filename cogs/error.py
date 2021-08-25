import re
import discord
from discord.ext import commands
from discord.ext.commands import cog
from asyncio import sleep
from discord.ext.commands import errors
from discord.ext.commands.errors import BadArgument, BotMissingPermissions, CommandNotFound, MissingPermissions, MissingRequiredArgument, MissingRole

import traceback


class Error(commands.Cog):
    """
    Error handler for bot commands
    """
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
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
                description="❎ I don't have permissions to Manage Messages."
            )
            await ctx.send(embed=error_embed)

        if isinstance(error, MissingRole):
            message = await ctx.send("❎ You are missing role permissions good sir.")
            sleep(5)
            await message.delete()

        else:
            m = await ctx.send("An unknown error occured.")
            n = await ctx.send(error)
            await sleep(5)
            await m.delete()
            await n.delete()
            print(traceback.print_exc)


def setup(client):
    client.add_cog(Error(client))
