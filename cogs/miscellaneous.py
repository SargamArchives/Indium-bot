from itertools import count
from logging import captureWarnings
from os import name
from discord.embeds import Embed

from utils import CountryResponse
import discord
from discord.ext import commands
from asyncio import sleep
from aiohttp import request
from discord.ext.commands.core import command
from config import API_KEY

class Miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        ping = round(self.client.latency * 1000)
        ping_embed = discord.Embed(
            title=f"pong🏓",
            description=f"{ping}ms"
        )
        await ctx.send(embed=ping_embed)

    @commands.command(name="av")
    async def avatar(self, ctx, user: discord.Member = None):
        if user == None: user = ctx.author
        avatar_embed = discord.Embed(
            title=f"{user.name}#{user.discriminator}\nAvatar"
        )
        avatar_embed.set_image(url=user.avatar_url)
        await ctx.send(embed=avatar_embed)

    @commands.command()
    async def weather(self, ctx, name="nepal"):
        api_key = API_KEY
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
            else:
                covid_embed = discord.Embed(
                description=f"Couldnot find about your country:😢 {country}"
                )
                await ctx.send(embed=covid_embed)

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
                    url="https://www.fda.gov/files/Coronavirus_3D_illustration_by_CDC_1600x900.png"
                )
                await ctx.send(embed=covid_embed)

    @commands.command(aliases=["compile","run"])
    async def code_compile(self,ctx,*, code):
        print("running")
        code = code.lower().strip("`")
        print(code)
        index = code.find("\n")
        lang = ""
        for i in range(index):
            lang += code[i]
        code = code.strip(f"{lang}\n")
        
        data = {
            "language": lang,
            "source": f"{code}"
        }
        URL = "https://emkc.org/api/v1/piston/execute"
        async with request("POST",URL, data = data) as response:
            if response.status == 200:
                data = await response.json()
                if data["ran"]:
                    print(data)
                    code_embed = discord.Embed(
                        title=f"Ran your {data['language']} code \nin version {data['version']}",
                        description=f"Output\n`{data['output']}`"
                    )
                    await ctx.send(embed=code_embed)
            else:
                m = await ctx.send("**oh no**\nCould not compile your code! :(")
                await sleep(5)
                await m.delete()

                
def setup(client):
    client.add_cog(Miscellaneous(client))