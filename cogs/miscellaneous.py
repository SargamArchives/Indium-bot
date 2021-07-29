from itertools import count
from logging import captureWarnings
from os import getenv
import discord
from discord.ext import commands
from aiohttp import request
from discord.ext.commands.core import command
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
                weather_data = data["weather"]
                wind_data = data["wind"]
                image_url = 11
                weather = discord.Embed(
                    title=f"Weather report: {name}",
                    description=f"Status: {weather_data[0]['main']}\nDescription: {weather_data[0]['description']}\nWind Speed: {wind_data['speed']}km/hr\n"
                )
                weather.set_image(
                    url=f"http://openweathermap.org/img/wn/{weather_data[0]['icon']}@2x.png")
                await ctx.send(embed=weather)
            else:
                await ctx.send("Can't find information about your city :(")

    @commands.command(name="country")
    async def country(self, ctx, country="nepal"):
        URL = f"https://restcountries.eu/rest/v2/name/{country}"
        async with request("GET", URL, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                capital = data[0]["capital"]
                currency = data[0]["currencies"][0]["name"]
                flag = data[0]["altSpellings"][0].lower()
                continenet = data[0]["region"]
                population = data[0]["population"]
                country_embed = discord.Embed(
                    title=f"Country: {country}",
                    description=f"Capital: {capital}\nCurrency: {currency}\nRegion: {continenet}\nPopulation: {population}"
                )
                country_embed.set_image(
                    url=f"https://flagcdn.com/256x192/{flag}.png")
                await ctx.send(embed=country_embed)


def setup(client):
    client.add_cog(Fun(client))
