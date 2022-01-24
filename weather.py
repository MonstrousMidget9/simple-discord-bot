import requests, discord, json
from discord.ext import commands

class weather(commands.Cog):
    def __init__(self, bot:discord.Client) -> None:
        self.bot = bot
    
    @commands.command(name="weather")
    async def weather(self, ctx:commands.Context, *, search:str=None):
        """get weather of a place"""
        if not search:
            return await ctx.send("location search required.")
        try:
            data = {
                'key' : 'KEY', # your key
                'q' : search
            }
            async with ctx.typing():
                req = requests.get('https://api.weatherapi.com/v1/current.json', params=data)
            weather = req.json()
            try:
                em = discord.Embed(title=f"{weather['location']['name']}, {weather['location']['country']}", description = f"{weather['location']['region']}\n\nweather: **{weather['current']['condition']['text']}**\n\nLocal Time : {weather['location']['localtime']}\nLatitude : {weather['location']['lat']}\nLongitude : {weather['location']['lon']}")
                em.add_field(name='Temp:', value=f"°C : {weather['current']['temp_c']}\n°F : {weather['current']['temp_f']}", inline=False)
                em.add_field(name='Humidity:', value=f"{weather['current']['humidity']-10}%", inline=False)
                em.add_field(name='Rainfall:', value=f"{weather['current']['precip_mm']} mm", inline=False)
                em.add_field(name='Pressure:', value=f"{int(weather['current']['pressure_mb']*100)} Pa\n{weather['current']['pressure_in']*2.54} cm", inline=True)
                em.add_field(name='Wind:', value=f"kmph : {weather['current']['wind_kph']}\nmph : {weather['current']['wind_mph']}\nDir : {weather['current']['wind_dir']}", inline=True)
                em.add_field(name='Cloud:', value=f"{weather['current']['cloud']}%", inline=True)
                em.set_thumbnail(url='https:' + weather['current']['condition']['icon'])
                await ctx.send(embed=em)
            except KeyError:
                await ctx.send(f"`{weather['error']['message']}`")
            # await ctx.send('```json\n' + json.dumps(req.json(), indent='    ') + '```')
        except Exception as e:
            return await ctx.send(f"an unexpected error has occured: `{type(e)} : {e}`")