from typing import List

import discord
from discord.ext import commands

from config import BOT_TOKEN, DEFAULT_PREFIX, ID1, ID2

OWNER_ID = [ID1, ID2]

intents = discord.Intents.all()

client = commands.Bot(
    command_prefix=commands.when_mentioned_or(DEFAULT_PREFIX),
    intents=intents,
    case_insensitive=True,
)

extensions = [
    "cogs.utils",
    "cogs.guild",
    "cogs.error",
    "cogs.moderation",
    "cogs.fun",
    "cogs.misc",
    "cogs.snipe",
    "jishaku",
]

for ext in extensions:
    client.load_extension(ext)


@client.command()
async def reload(ctx, cog_name: List[str]):
    for id in OWNER_ID:
        if ctx.message.author.id == id:
            client.reload_extension(f"cogs.{cog_name}")
            await ctx.send(f"sreloaded cogs.{cog_name}")


client.run(BOT_TOKEN)