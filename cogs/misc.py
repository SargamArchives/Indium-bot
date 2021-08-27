from os import name
import discord
from discord.errors import NoMoreItems
from discord.ext import commands
from discord.ext.commands import context
from discord.ext.commands.core import command

from datetime import date
from asyncio import sleep
from aiohttp import request, ClientSession
from typing import Optional

from config import API_KEY
from utils import CountryResponse


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
    async def avatar(self, ctx, user: Optional[discord.Member] = None):
        if user is None:
            user = ctx.author
        avatar_embed = discord.Embed(
            title=f"{user.name}#{user.discriminator}\nAvatar"
        )
        avatar_embed.set_image(url=user.avatar_url)
        await ctx.send(embed=avatar_embed)

    @commands.command()
    async def weather(self, ctx, name="nepal"):
        URL = f"https://api.openweathermap.org/data/2.5/weather?q={name}&appid={API_KEY}&units=metric"

        async with request("GET", URL) as response:
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
                )
                country_embed.add_field(
                    name="Capital",
                    value=f"{capital}",
                    inline=False
                )
                country_embed.add_field(
                    name="Currency",
                    value=f"{currency}",
                    inline=False
                )
                country_embed.add_field(
                    name="Region",
                    value=f"{continenet}",
                    inline=False
                )
                country_embed.add_field(
                    name="Population",
                    value=f"{population}",
                    inline=False
                )
                country_embed.set_thumbnail(
                    url=f"https://flagcdn.com/256x192/{flag}.png")
                await ctx.send(embed=country_embed)

    @commands.command(name="covid")  # TODO This code doesn't work well
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

    @commands.command(aliases=["compile", "run"])
    async def code_compile(self, ctx, *, code):
        print("running")
        code = code.lower().strip("`")
        index = code.find("\n")
        lang = ""
        for i in range(index):
            lang += code[i]
        code = code.replace(f"{lang}\n", "")
        data = {
            "language": lang,
            "source": f"{code}"
        }
        URL = "https://emkc.org/api/v1/piston/execute"
        async with request("POST", URL, data=data) as response:
            if response.status == 200:
                data = await response.json()
                if data["ran"] and data["output"]:
                    output = data['output']
                    output = output[:500]
                    lines = output.splitlines()
                    output = "\n".join(lines[:15])
                    code_embed = discord.Embed(
                        title=f"Ran your {data['language']} code",
                        description=f"Output\n{output}"
                    )
                    await ctx.send(embed=code_embed)
                else:
                    print(data)
            else:
                m = await ctx.send("**oh no**\nCould not compile your code! :(")
                await sleep(5)
                await m.delete()

    @command(name="nepse")
    async def nepse_command(self, ctx, company):
        today_date = date.today()
        url = "https://api.sheezh.com/nepse/v1/price"
        async with ClientSession() as session:
            async with session.post(
                url, json={"symbol": company.upper(), "date": str(today_date)}
            ) as resp:
                data = await resp.json()
                maxprice = data[0]["MaxPrice"]
                minprice = data[0]["MinPrice"]
                closingprice = data[0]["ClosingPrice"]
                tradedshares = data[0]["TradedShares"]
                previousclosing = data[0]["PreviousClosing"]

            async with session.post(
                "https://api.sheezh.com/nepse/v1/company", json={"symbol": company}
            ) as res:
                name = await res.json()
                companyName = name[0]["companyName"]
        embed = discord.Embed(
            title=f"Details for: {companyName}"
        )
        embed.add_field(
            name="Maximum Price",
            value=f"=Rs {maxprice}",
            inline=False
        )
        embed.add_field(
            name="Minimum Price",
            value=f"=Rs {minprice}",
            inline=False
        )
        embed.add_field(
            name="Closing Price",
            value=f"=Rs {closingprice}",
            inline=False
        )
        embed.add_field(
            name="Traded Shares",
            value=f"=Rs {tradedshares}",
            inline=False
        )
        embed.add_field(
            name="Previous Closing Price",
            value=f"=Rs {previousclosing}",
            inline=False
        )
        embed.set_thumbnail(
            url="https://cdn6.aptoide.com/imgs/a/8/4/a8435b6d8d3424dbc79a4ad52f976ad7_icon.png"
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Miscellaneous(client))
