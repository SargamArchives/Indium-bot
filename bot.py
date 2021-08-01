import discord
from discord.ext import commands
from config import BOT_TOKEN

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
    if ctx.message.author.id == 625651629743407104:
        client.reload_extension(f"cogs.{cog}")
        await ctx.send(f"reloaded cogs.{cog}")
    else:
        pass

client.run(BOT_TOKEN)