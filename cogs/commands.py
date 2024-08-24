import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send(f"Hello, {ctx.author.mention}!")

    @commands.command(aliases=["yardım", "yardim"])
    async def destek(self, ctx):
        embeded_message = discord.Embed(
            title="Destek",
            description=f"{ctx.author.name} aşağıdan komutlara ulaşabilirsin",
            color=discord.Color.random(),
        )
        embeded_message.set_thumbnail(url=ctx.author.avatar)
        embeded_message.add_field(name="2.Başlık", value="İçeriği", inline=False)
        embeded_message.set_image(url=ctx.guild.icon)
        embeded_message.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon)
        await ctx.send(embed=embeded_message)

    @commands.command(aliases=["gecikme"])
    async def ping(self, ctx):
        ping_embeded_message = discord.Embed(
            title="Ping",
            description=f"{ctx.author.name} botun gecikme değerine aşağıdan ulaşabilirsin",
            color=discord.Color.random(),
        )
        
        ping_embeded_message.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        ping_embeded_message.set_footer(text=f"Kullanan: {ctx.author.name}", icon_url=ctx.author.avatar)
        await ctx.send(embed=ping_embeded_message)

async def setup(bot):
    await bot.add_cog(Commands(bot))
