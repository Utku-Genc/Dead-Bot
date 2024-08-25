import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} kullanıma hazır")
    await bot.change_presence(activity=discord.Game("Selamlar, Ben Dead Chat"))
    print("Botun durumu ayarlandı.")
    # Kullanıcı İsmini alıyoruz
    username = bot.user.name
    # Sunucu sayısını alıyoruz
    guild_count = len(bot.guilds)
    # Kullanıcı sayısını alıyoruz
    user_count = len(set(bot.get_all_members()))
    # Prefix'i alıyoruz (komut ön eki)
    prefix = bot.command_prefix
    # Durum
    status = "Bot Çevrimiçi!"

    # Bilgileri yazdırıyoruz
    print(f"Kullanıcı İsmi     : {username}")
    print(f"Sunucular          : {guild_count}")
    print(f"Kullanıcılar       : {user_count}")
    print(f"Prefix             : {prefix}")
    print(f"Durum              : {status}")

    # Slash komutlarını senkronize et
    try:
        await bot.tree.sync()
        print("Slash komutları tüm sunuculara kaydedildi.")
    except Exception as e:
        print(f"Slash komutları kaydedilemedi. Hata: {e}")

async def Load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"{filename} yüklendi.")
            except Exception as e:
                print(f"{filename} yüklenirken hata oluştu: {e}")

async def main():
    async with bot:
        await Load()  # Load the cogs when the bot starts
        await bot.start(TOKEN) # Start the bot

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
