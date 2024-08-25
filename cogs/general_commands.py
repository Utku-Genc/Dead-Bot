import discord
from discord.ext import commands
from discord import app_commands


class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='bilgi', description='Sunucu ve kullanıcı bilgilerini gösterir.')
    async def bilgi(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user

        invite = await guild.text_channels[0].create_invite(max_age=3600, max_uses=1, reason="Bilgi komutu ile davet oluşturuldu.")
        roles = [role.mention for role in member.roles if role != guild.default_role]
        roles = ", ".join(roles) if roles else "Hiçbir rolü yok"

        embed = discord.Embed(
            title="Sunucu ve Kullanıcı Bilgileri",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="Sunucu Adı", value=guild.name, inline=True)
        embed.add_field(name="Sunucu ID", value=guild.id, inline=True)
        embed.add_field(name="Sunucu Sahibi", value=guild.owner.mention, inline=True)
        embed.add_field(name="Üye Sayısı", value=guild.member_count, inline=True)
        embed.add_field(name="Aktif Üye Sayısı", value=sum(1 for member in guild.members if member.status != discord.Status.offline), inline=True)
        embed.add_field(name="Oluşturulma Tarihi", value=guild.created_at.strftime('%d-%m-%Y %H:%M:%S'), inline=True)
        embed.add_field(name="Davet Linki", value=invite.url, inline=True)

        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="Kullanıcı Adı", value=member.name, inline=True)
        embed.add_field(name="Kullanıcı ID", value=member.id, inline=True)
        embed.add_field(name="Katılma Tarihi", value=member.joined_at.strftime('%d-%m-%Y %H:%M:%S'), inline=True)
        embed.add_field(name="Roller", value=roles, inline=True)

        embed.set_footer(text=f"Bilgileri gösteren: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='ping', description='Botun gecikme süresini gösterir.')
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! Gecikme süresi: {latency}ms")

    @app_commands.command(name='emojiler', description='Sunucudaki emojileri gösterir.')
    async def emojiler(self, interaction: discord.Interaction):
        guild = interaction.guild
        emojis = guild.emojis

        if not emojis:
            await interaction.response.send_message("Bu sunucuda emoji bulunmuyor.")
            return

        # 4096 karakter sınırına uymak için emojileri gruplara bölelim
        emoji_chunks = []
        chunk = ""
        for emoji in emojis:
            if len(chunk) + len(str(emoji)) + 1 > 1024:  # Her embed alanı için 1024 karakter sınırı
                emoji_chunks.append(chunk)
                chunk = str(emoji) + " "
            else:
                chunk += str(emoji) + " "

        if chunk:
            emoji_chunks.append(chunk)

        # Embed mesajlarını oluşturup gönderelim
        for i, chunk in enumerate(emoji_chunks):
            embed = discord.Embed(
                title=f"{guild.name} Sunucusundaki Emojiler - Bölüm {i + 1}",
                description=chunk,
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed) if i == 0 else await interaction.followup.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.errors.MissingPermissions):
            await ctx.send("Bu komutu kullanmak için gerekli izne sahip değilsiniz!")


async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))
