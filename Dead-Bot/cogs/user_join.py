import discord
from discord.ext import commands
import os
import random

class UserJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('UserJoin is ready')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.system_channel

        # user_join_img klasöründen rastgele bir resim seç
        image_list = [img for img in os.listdir("./cogs/user_join_img") if img.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        randomized_image = random.choice(image_list)
        image_url = f"attachment://{randomized_image}"

        embeded_message = discord.Embed(
            title="➤ Kardeşim, HOŞGELDİN!",
            description=f"{member.name}, **{member.guild.name}** sunucumuza katıldı!",
            color=discord.Color.random(),
        )
        embeded_message.set_author(name="Dead Community", url="https://discord.gg/Ts5saJp", icon_url="https://uploads.disquscdn.com/images/5e26d0ab8df126513c809b0899c13ae041d0b41cba81cead337eb8f905508f66.gif")
        embeded_message.set_thumbnail(url=member.avatar.url)
        embeded_message.add_field(name="➤ Davet Linki", value="[Sunucumuza Katıl!](https://discord.gg/Ts5saJp)", inline=False)
        embeded_message.add_field(name="Vergi", value="Ver", inline=False)
        embeded_message.set_footer(text=f"{member.guild.name}", icon_url=member.guild.icon.url)

        # Resmi gönder
        image_path = f"./cogs/user_join_img/{randomized_image}"
        img_file = discord.File(image_path, filename=randomized_image)
        
        # Embed mesajını ve resmi gönder
        embeded_message.set_image(url=image_url)
        await channel.send(embed=embeded_message, file=img_file)

async def setup(bot):
    await bot.add_cog(UserJoin(bot))
