import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from datetime import timedelta


class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ban', description='Belirtilen kullanıcıyı banlar.')
    @app_commands.describe(member='Kullanıcıyı belirtin', reason='Sebep belirtin')
    @commands.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if member == interaction.user:
            await interaction.response.send_message("Kendinizi banlayamazsınız!", ephemeral=True)
            return
        if member.guild_permissions.administrator:
            await interaction.response.send_message("Bir yöneticiyi banlayamazsınız!", ephemeral=True)
            return
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member.mention} kullanıcısı banlandı! Sebep: {reason}")

    @app_commands.command(name='kick', description='Belirtilen kullanıcıyı sunucudan atar.')
    @app_commands.describe(member='Kullanıcıyı belirtin', reason='Sebep belirtin')
    @commands.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if member == interaction.user:
            await interaction.response.send_message("Kendinizi atamazsınız!", ephemeral=True)
            return
        if member.guild_permissions.administrator:
            await interaction.response.send_message("Bir yöneticiyi atamazsınız!", ephemeral=True)
            return
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member.mention} kullanıcısı sunucudan atıldı! Sebep: {reason}")

    @app_commands.command(name='timeout', description='Belirtilen kullanıcıya zaman aşımı uygular.')
    @app_commands.describe(member='Kullanıcıyı belirtin', duration='Zaman aşımı süresi (dakika)', reason='Sebep belirtin')
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = None):
        if member == interaction.user:
            await interaction.response.send_message("Kendinize zaman aşımı uygulayamazsınız!", ephemeral=True)
            return
        if member.guild_permissions.administrator:
            await interaction.response.send_message("Bir yöneticiyi zaman aşımına uğratamazsınız!", ephemeral=True)
            return

        # Süreyi datetime.timedelta formatına dönüştür
        duration_in_timedelta = discord.utils.utcnow() + timedelta(minutes=duration)

        try:
            await member.timeout(duration_in_timedelta, reason=reason)
            await interaction.response.send_message(f"{member.mention} kullanıcısına {duration} dakika zaman aşımı uygulandı! Sebep: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message("Bu komutu kullanmak için yeterli izne sahip değilim. Lütfen botun yetkilerini kontrol edin.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"Bir hata oluştu: {e}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Beklenmeyen bir hata oluştu: {e}", ephemeral=True)

    @app_commands.command(name='userinfo', description='Belirtilen kullanıcının bilgilerini gösterir.')
    @app_commands.describe(member='Kullanıcıyı belirtin')
    @commands.has_permissions(administrator=True)
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member):
        # Embed mesajı oluştur
        embed = discord.Embed(
            title=f"{member.name}'nin Bilgileri",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.avatar.url)
        
        # Kullanıcı bilgilerini ekle
        embed.add_field(name="Kullanıcı Adı", value=member.name, inline=True)
        embed.add_field(name="Kullanıcı ID", value=member.id, inline=True)
        embed.add_field(name="Katılma Tarihi", value=member.joined_at.strftime('%d-%m-%Y %H:%M:%S'), inline=True)
        embed.add_field(name="Hesap Oluşturulma Tarihi", value=member.created_at.strftime('%d-%m-%Y %H:%M:%S'), inline=True)
        
        # Kullanıcının rollerini listele
        roles = [role.mention for role in member.roles if role != interaction.guild.default_role]
        roles_text = ', '.join(roles) if roles else 'Rol bulunmuyor'
        
        embed.add_field(name="Roller", value=roles_text, inline=False)
        
        embed.set_footer(text=f"Bilgileri gösteren: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        
        # Embed mesajını gönder
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name='yaz', description='Belirtilen mesajı gönderir.')
    @app_commands.describe(mesaj='Gönderilecek mesaj')
    @commands.has_permissions(administrator=True)
    async def yaz(self, interaction: discord.Interaction, mesaj: str):
        if len(mesaj) < 1:
            await interaction.response.send_message('Yazmam için herhangi bir şey yazmalısın.', ephemeral=True)
            return

        # Botun mesajını gönderirken allowed_mentions ile @everyone gibi etiketleri içermesine izin ver
        await interaction.response.send_message(mesaj, allowed_mentions=discord.AllowedMentions(everyone=True, roles=True))

    @app_commands.command(name='temizle', description='Belirtilen sayıda mesajı siler.')
    @app_commands.describe(amount='Silinecek mesaj sayısı')
    @commands.has_permissions(administrator=True)
    async def temizle(self, interaction: discord.Interaction, amount: int):
        """Belirtilen sayıda mesajı siler."""
        if amount <= 0:
            await interaction.response.send_message("Silinecek mesaj sayısı 0'dan büyük olmalıdır.", ephemeral=True)
            return

        await interaction.response.defer()  # Yanıtı ertele

        # Mesajları sil
        await interaction.channel.purge(limit=amount)

        # Geri bildirim mesajı gönder
        try:
            response_message = await interaction.followup.send(f"{amount} mesaj silindi.")
            # Mesajı 5 saniye beklet ve ardından sil
            await asyncio.sleep(5)
            await response_message.delete()
        except discord.NotFound:
            # Eğer mesajı bulamazsa, mesaj zaten silinmiş demektir.
            pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.errors.MissingPermissions):
            await ctx.send("Bu komutu kullanmak için gerekli izne sahip değilsiniz!")



async def setup(bot):
    await bot.add_cog(ModerationCommands(bot))
