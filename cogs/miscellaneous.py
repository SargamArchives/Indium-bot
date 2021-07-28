from os import getenv
import discord
from discord.ext import commands
from aiohttp import request
from dotenv import load_dotenv



class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def weather(self, ctx, name="nepal"):
        load_dotenv()
        api_key = getenv("API_KEY")
        URL = f"https://api.openweathermap.org/data/2.5/weather?q={name}&appid={api_key}&units=metric"

        async with request("GET", URL, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                print(data)
                weather_data = data["weather"]
                wind_data = data["wind"]
                image_url = 11
                weather = discord.Embed(
                    title=f"Weather report: {name}",
                    description=f"Status: {weather_data[0]['main']}\nDescription: {weather_data[0]['description']}\nWind Speed: {wind_data['speed']}km/hr\n"
                )
                weather.set_image(url = f"http://openweathermap.org/img/wn/{weather_data[0]['icon']}@2x.png")
                await ctx.send(embed=weather)
            else:
                await ctx.send("Can't find information about your city :(")




def setup(client):
    client.add_cog(Fun(client))
