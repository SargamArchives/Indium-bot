from itertools import count
from logging import captureWarnings
from os import getenv
from dotenv.main import with_warn_for_invalid_lines

from yarl import URL
from utils import CountryResponse
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
                country_data = await response.json()
                country_data = CountryResponse(**country_data[0])
                capital = country_data.capital
                currency = country_data.currencies[0].get("name")
                flag = country_data.alt_spellings[0].lower()
                continenet = country_data.region
                population = country_data.population

                country_embed = discord.Embed(
                    title=f"Country: {country}",
                    description=f"Capital: {capital}\nCurrency: {currency}\nRegion: {continenet}\nPopulation: {population}"
                )
                country_embed.set_image(
                    url=f"https://flagcdn.com/256x192/{flag}.png")
                await ctx.send(embed=country_embed)

    @commands.command(name="covid") #TODO This code doesn't work well
    async def corona(self, ctx, country="nepal"):
        URL = f"https://api.covid19api.com/live/country/{country}/status/confirmed"
        async with request("GET", URL) as response:
            if response.status == 200:
                data = await response.json()
                todays_data = data[len(data) - 1]
                Confirmed = todays_data["Confirmed"]
                Deaths = todays_data["Deaths"]
                Active = todays_data["Active"]
                covid_embed = discord.Embed(
                    title=f"Covid stats for: {country}",
                    description=f"**Total Confirmed**: {Confirmed}\n**Total Deaths**: {Deaths}\n**Total Active**: {Active}"
                )
                covid_embed.set_image(
                    url="https://www.shorturl.at/osCH3"
                )
                await ctx.send(embed=covid_embed)

def setup(client):
    client.add_cog(Fun(client))
