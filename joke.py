import discord, requests
from discord.ext import commands

class Jokes(commands.Cog):
    def __init__(self, bot:discord.Client) -> None:
        self.bot = bot
    
    @commands.command(name="chuck norris", aliases=["chuck"])
    async def chuck_norris(self, ctx:commands.Context, norris:str=None):
        """chuck norris facts"""
        try:
            j = requests.get("https://api.chucknorris.io/jokes/random").json()["value"]
            return await ctx.send(f"`{j}`")
        except Exception as e:
            return await ctx.send(f"an unexpected error has occured: `{type(e)} : {e}`")
    
    @commands.command(name="dad joke", aliases=["dad"])
    async def dad_jokes(self, ctx:commands.Context, jokes:str=None):
        """dad jokes"""
        try:
            j = requests.get("https://icanhazdadjoke.com/", headers={"Accept":"application/json"}).json()["joke"]
            return await ctx.send(f"`{j}`")
        except Exception as e:
            return await ctx.send(f"an unexpected error has occured: `{type(e)} : {e}`")
