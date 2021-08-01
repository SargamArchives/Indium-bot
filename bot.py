import discord
from discord.ext import commands
from config import BOT_TOKEN, ID1, ID2

OWNER_ID = [ID1, ID2]

intents = discord.Intents(
                        messages=True,
                        guilds=True,
                        reactions=True,
                        members=True,
                        presences=True
                        )

client = commands.Bot(
                    command_prefix=">",
                    intents=intents
                    )

extensions = [
    "jishaku",
    "cogs.fun",
    "cogs.miscellaneous",
    "cogs.moderation",
    "cogs.utils",
]

for ext in extensions:
    client.load_extension(ext)

@client.command()
async def reload(ctx, cog):
    for id in OWNER_ID:
        if ctx.message.author.id == id:
            client.reload_extension(f"cogs.{cog}")
            await ctx.send(f"reloaded cogs.{cog}")

client.run(BOT_TOKEN)
