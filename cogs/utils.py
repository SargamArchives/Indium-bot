import discord
from discord import message
from discord.ext import commands


class Utilis(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged in as bot")

    @commands.command()
    async def ping(self, ctx):
        ping = 1000 * self.client.latency
        await ctx.send(f"Pong! {ping}")

    @commands.command(name="av")
    async def avatar(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        url = user.avatar_url
        avatar_embed = discord.Embed(
            title=f"{user.name}#{user.discriminator}\nAvatar"
        )
        avatar_embed.set_image(url = url)
        await ctx.send(embed=avatar_embed)

def setup(client):
    client.add_cog(Utilis(client))