import asyncio
from asyncio import sleep
from datetime import date
from typing import Optional, Union

import discord
from aiohttp import ClientSession, request
from discord.ext import commands

from config import API_KEY, DEFAULT_EMBED_COLOR
from utils import CountryResponse


class Miscellaneous(commands.Cog):
    """
    Some Miscellaneous commands
    """

    def __init__(self, client: commands.Bot):
        self.client = client
        self.embed_color = DEFAULT_EMBED_COLOR
        self.embed = discord.Embed(colour=self.embed_color)

    @commands.command()
    async def ping(self, ctx):
        ping = round(self.client.latency * 1000)
        ping_embed = discord.Embed(
            title=f"pong🏓", description=f"{ping}ms", colour=self.embed_color
        )
        await ctx.send(embed=ping_embed)

    @commands.command(name="av")
    async def avatar(
        self, ctx: commands.Context, user: Optional[discord.User] = None
    ) -> None:
        if user is None:
            user = ctx.author
        avatar_embed = discord.Embed(
            title=f"{user.name}#{user.discriminator}\nAvatar", colour=self.embed_color
        )
        avatar_embed.set_image(url=user.avatar_url)
        await ctx.send(embed=avatar_embed)

    # TODO Fix this thing someday

    @commands.command()
    async def weather(self, ctx, name: str = "nepal"):
        URL = f"https://api.openweathermap.org/data/2.5/weather?q={name}&appid={API_KEY}&units=metric"

        async with request("GET", URL) as response:
            if response.status == 200:
                data = await response.json()

                weather_data = data["weather"]
                wind_data = data["wind"]
                status = weather_data[0]["main"]
                description = weather_data[0]["description"]
                wind_speed = wind_data["speed"]

                weather = discord.Embed(
                    title=f"Weather report: {name.title()}", colour=self.embed_color
                )
                weather.add_field(name="Status", value=f"{status}", inline=False)
                weather.add_field(
                    name="Description", value=f"{description}", inline=False
                )
                weather.add_field(
                    name="Wind Speed", value=f"{wind_speed}km/hr", inline=False
                )
                weather.set_thumbnail(
                    url=f"http://openweathermap.org/img/wn/{weather_data[0]['icon']}@2x.png"
                )
                await ctx.send(embed=weather)
            else:
                weather_fail_embed = self.embed
                weather_fail_embed.title = "Oh no"
                weather_fail_embed.description = (
                    "Could not find informatin about your city"
                )
                await ctx.send(embed=weather_fail_embed)

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
                    title=f"Country: {country}", colour=self.embed_color
                )
                country_embed.add_field(
                    name="Capital", value=f"{capital}", inline=False
                )
                country_embed.add_field(
                    name="Currency", value=f"{currency}", inline=False
                )
                country_embed.add_field(
                    name="Region", value=f"{continenet}", inline=False
                )
                country_embed.add_field(
                    name="Population", value=f"{population}", inline=False
                )
                country_embed.set_thumbnail(
                    url=f"https://flagcdn.com/256x192/{flag}.png"
                )
                await ctx.send(embed=country_embed)

    @commands.command(name="covid")  # TODO This code doesn't work well
    async def corona(self, ctx, country="nepal"):
        URL = f"https://api.covid19api.com/live/country/{country}/status/confirmed"
        async with request("GET", URL) as response:
            if response.status == 200:
                data = await response.json()
                todays_data = data[len(data) - 1]
                confirmed = todays_data["Confirmed"]
                deaths = todays_data["Deaths"]
                active = todays_data["Active"]

                covid_embed = discord.Embed(
                    title=f"Covid stats for: {country}", colour=self.embed_color
                )
                covid_embed.add_field(
                    name="Total Confirmed", value=f"{confirmed}", inline=False
                )
                covid_embed.add_field(
                    name="Total Deaths", value=f"{deaths}", inline=False
                )
                covid_embed.add_field(
                    name="Total Active", value=f"{active}", inline=False
                )
                covid_embed.set_thumbnail(
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
        data = {"language": lang, "source": f"{code}"}
        URL = "https://emkc.org/api/v1/piston/execute"
        async with request("POST", URL, data=data) as response:
            if response.status == 200:
                data = await response.json()
                if data["ran"] and data["output"]:
                    output = data["output"]
                    output = output[:500]
                    lines = output.splitlines()
                    output = "\n".join(lines[:15])
                    code_embed = discord.Embed(
                        title=f"Ran your {data['language']} code",
                        description=f"Output\n{output}",
                        colour=self.embed_color,
                    )
                    await ctx.send(embed=code_embed)
                else:
                    print(data)
            else:
                m = discord.Embed(
                    title=f"Oh no",
                    description=f"Could not compile your code! :(",
                    colour=self.embed_color,
                )
                await sleep(10)
                await m.delete()

    @commands.command(name="nepse")
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
            title=f"Details for: {companyName}", colour=self.embed_color
        )
        embed.add_field(name="Maximum Price", value=f"=Rs {maxprice}", inline=False)
        embed.add_field(name="Minimum Price", value=f"=Rs {minprice}", inline=False)
        embed.add_field(name="Closing Price", value=f"=Rs {closingprice}", inline=False)
        embed.add_field(name="Traded Shares", value=f"=Rs {tradedshares}", inline=False)
        embed.add_field(
            name="Previous Closing Price", value=f"=Rs {previousclosing}", inline=False
        )
        embed.set_thumbnail(
            url="https://cdn6.aptoide.com/imgs/a/8/4/a8435b6d8d3424dbc79a4ad52f976ad7_icon.png"
        )
        await ctx.send(embed=embed)

    @commands.command(name="define")
    async def define_urban(self, ctx, search_query):
        URL = f"https://urbanscraper.herokuapp.com/search/{search_query}"
        async with request("GET", url=URL) as response:
            if response.status == 200:
                request_data = await response.json()
                term = request_data[0]["term"].title()
                definition = request_data[0]["definition"]
                example = request_data[0]["example"]
                embed = self.embed
                embed.title = f"{term}"
                embed.add_field(name=f"Definition", value=f"{definition}", inline=False)
                embed.add_field(name=f"Example", value=f"{example}", inline=False)
                await ctx.send(embed=embed)
                embed.clear_fields()
            else:
                request_data = await response.json()
                m = await ctx.send(request_data["message"])
                asyncio.sleep(5)
                await m.delete()

    
    @commands.command()
    async def device(
        self,
        ctx: commands.Context,
        user: Optional[Union[discord.Member, discord.User]] = None,
    ) -> None:
        if user is None:
            user = ctx.author
        comp_status = user.desktop_status
        mobile_status = user.mobile_status
        web_status = user.web_status

        embed = discord.Embed(
            title=f"{user.display_name}'s device status", colour=self.embed_color
        )
        embed.add_field(name="PC client", value=f"💻: {comp_status}", inline=True)
        embed.add_field(name="Web client", value=f"🌏: {web_status}", inline=False)
        embed.add_field(name="Mobile client", value=f"📱: {mobile_status}", inline=False)

        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Miscellaneous(client))
