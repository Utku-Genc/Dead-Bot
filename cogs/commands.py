import discord
from discord.ext import commands
from discord import app_commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="destek", description="Yardım komutları")
    @app_commands.describe(category="Yardım kategorisi")
    @app_commands.choices(
        category=[
            app_commands.Choice(name="Genel", value="genel"),
            app_commands.Choice(name="Sunucu", value="sunucu"),
            app_commands.Choice(name="Eğlence", value="eglence"),
            app_commands.Choice(name="Moderasyon", value="moderasyon")
        ]
    )
    async def destek(self, interaction: discord.Interaction, category: str = None):
        if category is None:
            embed = discord.Embed(
                title="Destek",
                description=f"{interaction.user.name} aşağıdan komutlara ulaşabilirsin",
                color=discord.Color.random()
            )
            embed.set_author(name="Dead Community", icon_url=interaction.user.display_avatar.url)
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            embed.set_image(url=interaction.guild.icon.url)
            embed.add_field(
                name="Kategoriler:",
                value=(
                    f"**/destek kategori: Genel**\n"
                    f"**/destek kategori: Sunucu**\n"
                    f"**/destek kategori: Eğlence**\n"
                    f"**/destek kategori: Moderasyon**"
                ),
                inline=False
            )
            embed.add_field(
                name="» Linkler",
                value=(
                    "[Davet Et](https://discord.com/oauth2/authorize?client_id=860851471474360331&scope=bot&permissions=805314622)"
                    " **|** "
                    "[Sunucumuz](https://discord.gg/9aKzTnmDCb)"
                    " **|** "
                    "[Youtube](https://www.youtube.com/channel/UCk0GEKuvOPXu9BlCrXNva-A?sub_confirmation=1)"
                    " **|** "
                    "[Web Sitesi](https://i.hizliresim.com/eb1vz8z.png)"
                ),
                inline=False
            )
            embed.set_footer(text=f"Bu komutu kullanan kullanıcı {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)
            return

        if category.lower() == 'genel':
            embed = discord.Embed(
                title='Genel Komutlar',
                color=0x2667FF
            )
            embed.set_footer(text=f'Bu komutu kullanan kullanıcı: {interaction.user}', icon_url=interaction.user.display_avatar.url)
            

            embed.add_field(name=f"/bilgi <@kullanıcı>", value=" Sunucu ve kullanıcı bilgilerini gösterir.", inline=False)
            embed.add_field(name=f"/ping", value=" Botun gecikme süresini gösterir.", inline=False)
            embed.add_field(name=f"/emojiler", value=" Sunucudaki emojileri gösterir.", inline=False)
            embed.add_field(name="» Linkler", value=(
                "[Davet Et](https://discord.com/oauth2/authorize?client_id=860851471474360331&scope=bot&permissions=805314622) | "
                "[Sunucumuz](https://discord.gg/9aKzTnmDCb) | "
                "[Youtube](https://www.youtube.com/channel/UCk0GEKuvOPXu9BlCrXNva-A?sub_confirmation=1) | "
                "[Web Sitesi](https://i.hizliresim.com/eb1vz8z.png)"
            ))
            await interaction.response.send_message(embed=embed)
            return

        if category.lower() == 'sunucu':
            embed = discord.Embed(
                title='Sunucu Komutlar',
                color=0x2667FF
            )
            embed.set_author(name='Sunucu', icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=f'Bu komutu kullanan kullanıcı {interaction.user}', icon_url=interaction.user.display_avatar.url)
            commands_list = [f':white_small_square: - **/{cmd.name}** {cmd.help}' for cmd in self.bot.commands if cmd.cog_name == 'Sunucu']
            embed.description = "\n".join(commands_list)
            embed.add_field(name="» Linkler", value=(
                "[Davet Et](https://discord.com/oauth2/authorize?client_id=860851471474360331&scope=bot&permissions=805314622) | "
                "[Sunucumuz](https://discord.gg/9aKzTnmDCb) | "
                "[Youtube](https://www.youtube.com/channel/UCk0GEKuvOPXu9BlCrXNva-A?sub_confirmation=1) | "
                "[Web Sitesi](https://i.hizliresim.com/eb1vz8z.png)"
            ))
            await interaction.response.send_message(embed=embed)
            return

        if category.lower() == 'eglence':
            embed = discord.Embed(
                title='Eğlence Komutlar',
                color=0x2667FF
            )
            embed.set_author(name='Eğlence', icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=f'Bu komutu kullanan kullanıcı {interaction.user}', icon_url=interaction.user.display_avatar.url)
            commands_list = [f':white_small_square: - **/{cmd.name}** {cmd.help}' for cmd in self.bot.commands if cmd.cog_name == 'Eğlence']
            embed.description = "\n".join(commands_list)
            embed.add_field(name="» Linkler", value=(
                "[Davet Et](https://discord.com/oauth2/authorize?client_id=860851471474360331&scope=bot&permissions=805314622) | "
                "[Sunucumuz](https://discord.gg/9aKzTnmDCb) | "
                "[Youtube](https://www.youtube.com/channel/UCk0GEKuvOPXu9BlCrXNva-A?sub_confirmation=1) | "
                "[Web Sitesi](https://i.hizliresim.com/eb1vz8z.png)"
            ))
            await interaction.response.send_message(embed=embed)
            return

        if category.lower() == 'moderasyon':
            embed = discord.Embed(
                title="Moderasyon Komutları",
                description="Aşağıda moderasyon komutlarının listesi ve kullanımları bulunmaktadır.",
                color=discord.Color.blue()
            )
            embed.add_field(name=f"/ban <@kullanıcı>", value="Belirtilen kullanıcıyı sunucudan banlar.", inline=False)
            embed.add_field(name=f"/kick <@kullanıcı>", value="Belirtilen kullanıcıyı sunucudan atar.", inline=False)
            embed.add_field(name=f"/timeout <@kullanıcı> <süre>", value="Belirtilen kullanıcıya zaman aşımı uygular. Süre formatı: 1h, 1m, 1s", inline=False)
            embed.add_field(name=f"/userinfo <@kullanıcı>", value="Kullanıcının bilgilerini gösterir. Son mesajını da içerir.", inline=False)
            embed.add_field(name=f"/sil <sayı>", value="Belirtilen sayıda mesajı siler.", inline=False)
            embed.set_footer(text=f"Bu komutu kullanan kullanıcı {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
            embed.add_field(name="» Linkler", value=(
                "[Davet Et](https://discord.com/oauth2/authorize?client_id=860851471474360331&scope=bot&permissions=805314622) | "
                "[Sunucumuz](https://discord.gg/9aKzTnmDCb) | "
                "[Youtube](https://www.youtube.com/channel/UCk0GEKuvOPXu9BlCrXNva-A?sub_confirmation=1) | "
                "[Web Sitesi](https://i.hizliresim.com/eb1vz8z.png)"
            ))
            await interaction.response.send_message(embed=embed)
            return

        await interaction.response.send_message("Belirtilen kategori geçerli değil. Lütfen geçerli bir kategori belirtin: Genel, Sunucu, Eğlence, Moderasyon.")

async def setup(bot):
    await bot.add_cog(Commands(bot))
