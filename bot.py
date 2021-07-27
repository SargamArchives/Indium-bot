from operator import matmul
import os
from discord import guild, user
from discord.embeds import Embed
from discord.flags import alias_flag_value
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


intents = discord.Intents(messages=True, guilds=True,
                          reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix=">", intents=intents)


# Bots actual code
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


client.run(BOT_TOKEN)