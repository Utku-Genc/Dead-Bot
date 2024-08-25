import discord
from discord.ext import commands
from random import choice
import asyncpraw as praw
import time

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(
            client_id='fPlHja1jVastdAJOw9lhOA',
            client_secret='Vya-GdejUT3wULMTV2CixbIsha5P3w',
            user_agent='script:DeadChat:v1.0 (by u/Utku_Genc)'
        )
        self.cache = {}
        self.cache_expiry = 3600  # Cache duration in seconds (1 hour)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} cog yüklendi.")

    async def get_cached_posts(self, subreddit_name, limit=1000):
        current_time = time.time()

        if (subreddit_name in self.cache and 
            current_time - self.cache[subreddit_name]['timestamp'] < self.cache_expiry):
            return self.cache[subreddit_name]['posts']

        subreddit = await self.reddit.subreddit(subreddit_name)
        posts_list = []

        async for post in subreddit.hot(limit=limit):
            if post.author is not None and any(post.url.endswith(ext) for ext in [".png", ".jpeg", ".jpg", ".gif"]):
                author_name = post.author.name
                post_like = post.score
                posts_list.append((post.url, author_name, post_like))
            elif post.author is None:
                author_name = "Anonim"
                posts_list.append((post.url, author_name, post_like))

        self.cache[subreddit_name] = {
            'posts': posts_list,
            'timestamp': current_time
        }

        return posts_list

    @commands.command()
    async def memes(self, ctx: commands.Context):
        posts_list = await self.get_cached_posts("memes")
        if posts_list:
            random_post = choice(posts_list)
            memes_embed = discord.Embed(
                title="Random Memes",
                description="r/memes sunucusundan bazı random memeler",
                color=discord.Color.random()
            )
            memes_embed.set_author(name=f"Memes isteyen {ctx.author.name}", icon_url=ctx.author.avatar)
            memes_embed.set_image(url=random_post[0])
            memes_embed.add_field(name="Beğeni Sayısı", value=f"{random_post[2]}", inline=False)
            memes_embed.set_footer(text=f"Post sahibi {random_post[1]} ", icon_url=None)
            await ctx.send(embed=memes_embed)
        else:
            await ctx.send("Memes bulunamadı. Daha sonra tekrar deneyin")

    @commands.command()
    async def zargonya(self, ctx: commands.Context):
        posts_list = await self.get_cached_posts("ZargoryanGalaksisi")
        if posts_list:
            random_post = choice(posts_list)
            memes_embed = discord.Embed(
                title="Random Memes",
                description="r/ZargoryanGalaksisi sunucusundan bazı random memeler",
                color=discord.Color.random()
            )
            memes_embed.set_author(name=f"Memes isteyen {ctx.author.name}", icon_url=ctx.author.avatar)
            memes_embed.set_image(url=random_post[0])
            memes_embed.add_field(name="Beğeni Sayısı", value=f"{random_post[2]}", inline=False)
            memes_embed.set_footer(text=f"Post sahibi {random_post[1]} ", icon_url=None)
            await ctx.send(embed=memes_embed)
        else:
            await ctx.send("Memes bulunamadı. Daha sonra tekrar deneyin")
    
    @commands.command()
    async def kgbtr(self, ctx: commands.Context):
        posts_list = await self.get_cached_posts("KGBTR")
        if posts_list:
            random_post = choice(posts_list)
            memes_embed = discord.Embed(
                title="Random Memes",
                description="r/KGBTR sunucusundan bazı random memeler",
                color=discord.Color.random()
            )
            memes_embed.set_author(name=f"Memes isteyen {ctx.author.name}", icon_url=ctx.author.avatar)
            memes_embed.set_image(url=random_post[0])
            memes_embed.add_field(name="Beğeni Sayısı", value=f"{random_post[2]}", inline=False)
            memes_embed.set_footer(text=f"Post sahibi {random_post[1]} ", icon_url=None)
            await ctx.send(embed=memes_embed)
        else:
            await ctx.send("Memes bulunamadı. Daha sonra tekrar deneyin")

    @commands.command()
    async def hentai(self, ctx: commands.Context, count: int = 1):
        posts_list = await self.get_cached_posts("Hentai")
        if posts_list:
            for _ in range(count):
                random_post = choice(posts_list)
                memes_embed = discord.Embed(
                    title="Random Hentai",
                    description="r/Hentai sunucusundan bazı random hentailer 🙂",
                    color=discord.Color.random()
                )
                memes_embed.set_author(name=f"Hentai isteyen {ctx.author.name}", icon_url=ctx.author.avatar)
                memes_embed.set_image(url=random_post[0])
                memes_embed.add_field(name="Beğeni Sayısı", value=f"{random_post[2]}", inline=False)
                memes_embed.set_footer(text=f"Post sahibi {random_post[1]}", icon_url=None)
                await ctx.send(embed=memes_embed)
        else:
            await ctx.send("Hentai bulunamadı. Daha sonra tekrar deneyin")

    def cog_unload(self):
        self.bot.loop.create_task(self.reddit.close())

async def setup(bot):
    await bot.add_cog(Reddit(bot))
