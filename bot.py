import os
import discord
from discord.ext import commands
from config import BOT_TOKEN



intents = discord.Intents(messages=True, guilds=True,
                          reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix=">", intents=intents)
client.load_extension("jishaku")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


client.run(BOT_TOKEN)