from discord.ext import commands
import asyncpraw, discord, random, async_timeout
from mimetypes import guess_type

# reddit api details
red = asyncpraw.Reddit(
    client_id = 'id',
    client_secret = 'client secret',
    user_agent = 'user agent'
)
class reddit(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot:discord.Client = bot

    @commands.command(name="meme")
    async def get_random_meme(self, ctx:commands.Context):
        import asyncpraw.models
        subreddit:asyncpraw.models.Subreddit = await red.subreddit(random.choice(['unexpected', 'memes', 'dankmemes', 'MemeEconomy']))

        async with ctx.typing():
            MEME:asyncpraw.models.Submission = random.choice([i async for i in subreddit.top()])

        embed = discord.Embed(title = MEME.title, description = MEME.selftext, url=f"https://www.reddit.com/r/{subreddit.display_name}/comments/{MEME.id}")
        if MEME.media:
            return await ctx.send(f"https://www.reddit.com/r/{subreddit.display_name}/comments/{MEME.id}")
        else:
            try:
                if guess_type(MEME.url)[0].startswith('image'):
                    embed.set_image(url= MEME.url)
            except AttributeError:
                pass
        embed.set_footer(text=f'👍🏻 : {MEME.ups} \n💬 : {MEME.num_comments}')
        
        return await ctx.send(embed=embed)

    @commands.command(name="subreddit")
    async def subreddit(self, ctx:commands.Context, *, sub:str=None):
        if not sub:
            return await ctx.send("subreddit search required.")
        try:
            import asyncpraw.models
            subreddit:asyncpraw.models.Subreddit = await red.subreddit(sub)

            async with ctx.typing():
                subs = subreddit.top(time_filter = 'day', limit= 25)
                subs = [i async for i in subs]

            def get_post_embed(ind:int):
                try:
                    p:asyncpraw.models.Submission = subs[ind]
                except IndexError:
                    return discord.Embed(title='Sorry, you have Exceeded the Limit!', colour=0)
                # p.load()
                em = discord.Embed(title = p.title, description = p.selftext, colour = random.randint(0, 16581375), url = 'https://www.reddit.com/r/' + str(subreddit) + '/comments/' + str(p))
                if p.media:
                    return
                else:
                    try:
                        if guess_type(p.url)[0].startswith('image'):
                            em.set_image(url=p.url)
                    except AttributeError:
                        pass

                em.set_footer(text=f'👍🏻 : {p.ups} \n💬 : {p.num_comments}', icon_url='https://upload.wikimedia.org/wikipedia/commons/5/56/Donald_Trump_official_portrait.jpg')
                return em

            postno = 0
            em = get_post_embed(postno)
            if em:
                message:discord.Message = await ctx.send(embed=em)
            else:
                message:discord.Message = await ctx.send(content=f"https://www.reddit.com/r/{subreddit.display_name}/comments/{subs[postno].id}")

            for r in ('⬅️', '👍','➡️', '❎', '📌'):
                await message.add_reaction(r)

            def check(reaction:discord.Reaction, user:discord.Member):
                if str(reaction) in ('🖕','⬅️', '👍','➡️', '❎', '📌') and reaction.message == message and user != self.bot.user:
                    return True
                else:
                    return False

            while True:
                try:
                    async with async_timeout.timeout(180): # timeout after 3 mins
                        reaction, user = await self.bot.wait_for('reaction_add', check=check)
                except:
                    print("Timeout")
                    break

                reaction:discord.Reaction
                user:discord.Member
                if str(reaction) == '➡️':
                    await reaction.remove(user)
                    postno += 1
                    em = get_post_embed(postno)
                    if em:
                        print("embed")
                        await message.edit(embed=em, content=None)
                    else:
                        print("direct")
                        await message.edit(content=f"https://www.reddit.com/r/{subreddit.display_name}/comments/{subs[postno].id}", embed=None)
                elif str(reaction) == '⬅️':
                    await reaction.remove(user)
                    postno -= 1
                    em = get_post_embed(postno)
                    if em:
                        await message.edit(embed=em, content=None)
                    else:
                        await message.edit(content=f"https://www.reddit.com/r/{subreddit.display_name}/comments/{subs[postno].id}", embed=None)
                elif str(reaction) == '👍':
                    await ctx.channel.send('`Successfully upvoted this post`', delete_after=5)
                    subs[postno].upvote()

                elif str(reaction) == '❎':
                    await message.delete()
                    break
                elif str(reaction) == '📌':
                    await user.send('Here is your Pinned Post! `:)`')
                    em = get_post_embed(postno)
                    if em:
                        await user.send(embed=em)
                    else:
                        await user.send(content=f"https://www.reddit.com/r/{subreddit.display_name}/comments/{subs[postno].id}")
                    await reaction.remove(user)
        except Exception as e:
            await ctx.send(f'Sorry, an error has occured:`{type(e)}` : `{e}`')
