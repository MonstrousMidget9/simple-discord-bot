from discord.ext import commands
import reddit, weather, joke

bot = commands.Bot(command_prefix='./')
token = "bot token"

@bot.event
async def on_ready():
    print('\nBot is ready as  :', bot.user , '\n')

bot.add_cog(reddit.reddit(bot))
bot.add_cog(joke.Jokes(bot))
bot.add_cog(weather.weather(bot))
bot.run(token)