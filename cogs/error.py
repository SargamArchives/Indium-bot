import discord
from discord.ext import commands
from discord.ext.commands import cog


class Error(commands.Cog):
    
    # @commands.Cog.listener()
    # async def on_command_error(ctx, error):
    #     print("error")




    @commands.Cog.listener()
    async def on_error(self):
        print("errors")


def setup(client):
    client.add_cog(Error(client))
