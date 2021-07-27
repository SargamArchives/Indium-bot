import discord
from discord.ext import commands


class Utilis(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged in as bot")




def setup(client):
    client.add_cog(Utilis(client))
