# A simple Discord Bot
A simple discord bot written in python which can surf subreddits, send a random meme, jokes and also weather of a given place.
### Weather
Uses the [weatherapi](https://weatherapi.com) api.

#### commands

`./weather <name of location>`  
Fetches the weather data of the given location and prettyfies it into a `discord.Embed`

![weather](https://github.com/MonstrousMidget9/simple-discord-bot/blob/main/readme/weather.png?raw=true)

### Reddit
Uses the [asyncpraw](https://asyncpraw.readthedocs.io/en/stable/) reddit api wrapper.
 
#### commands
`./meme`  
Fetch a random meme from a random meme subreddit's top posts of all time.

![meme](https://github.com/MonstrousMidget9/simple-discord-bot/blob/main/readme/_meme.png?raw=true)

`./subreddit <subreddit name>`  
Browse through the top posts of the day and control using discord reactions.  
Upvote and Pin the posts you like to your dm channel.

![subreddit](https://github.com/MonstrousMidget9/simple-discord-bot/blob/main/readme/subreddit.gif?raw=true)

### Jokes
Uses the [icanhazdadjoke](https://icanhazdadjoke.com/) and the [Chuck Norris](https://api.chucknorris.io/) api to fetch a fetch a random dad joke and some funny chuck norris facts.

#### commands

`./chuck norris`  
for a random chuck norris joke.

`./dad joke`  
for a random dad joke.

![jokes](https://github.com/MonstrousMidget9/simple-discord-bot/blob/main/readme/_jokes.png?raw=true)

### Requirements
```
pip install discord
pip install asyncpraw
```
