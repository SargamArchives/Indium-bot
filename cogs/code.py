from discord.ext import commands
from aiohttp import request
import json

class Code(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="run")
    async def code_runner(self, ctx, language, *, code):
        print("loaded")
        print(language)
        print(f"{code}")
        data1 = {
            'lang': 'C',
            'code': code,
            'input': '',
            'save': False
        }
        URL="https://ide.geeksforgeeks.org/main.php"
        async with request("POST", URL, data=data1) as response:
            if response.status == 200:
                # data = await response.json()
                # print(data)
                data = await response.read()
                hashrate = json.loads(data)
                print(hashrate)


def setup(client):
    client.add_cog(Code(client))