import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} kullanıma hazır")
    await bot.change_presence(activity=discord.Game("Selamlar Ben Dead Chat"))
    print("Botun durumu ayarlandı.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

async def Load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"{filename} eklendi.")
            except Exception as e:
                print(f"{filename} yüklenirken hata oluştu: {e}")

async def main():
    async with bot:
        await Load()  # Load the cogs when the bot starts
        await bot.start(TOKEN) # Start the bot


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
