import discord
from discord import message
from discord.ext import commands
from discord.ext.commands import context
from discord.ext.commands.cog import Cog

from typing import List

from config import BOT_TOKEN, ID1, ID2

OWNER_ID = [ID1, ID2]

intents = discord.Intents.all()

client = commands.Bot(
    command_prefix=commands.when_mentioned_or(">"),
    intents=intents
)

extensions = [
    "jishaku",
    "cogs.fun",
    "cogs.misc",
    "cogs.moderation",
    "cogs.utils",
    "cogs.error"
]

for ext in extensions:
    client.load_extension(ext)


@client.command()
async def reload(ctx, cog: List[str]):
    for id in OWNER_ID:
        if ctx.message.author.id == id:
            client.reload_extension(f"cogs.{cog}")
            await ctx.send(f"sreloaded cogs.{cog}")

client.run(BOT_TOKEN)