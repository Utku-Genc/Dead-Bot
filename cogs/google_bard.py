import io
import discord
import google.generativeai as genai
from discord.ext import commands
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_KEY = os.getenv("GOOGLE_KEY")

# Configure Google Bard API with the API key
genai.configure(api_key=GOOGLE_KEY)

class GoogleBard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # Check if the bot was mentioned in the message
        if self.bot.user.mentioned_in(message):
            try:
                # Remove bot mention from the message content
                content = message.content.replace(self.bot.user.mention, "").strip()

                # Remove mentions of other users from the message content
                for user in message.mentions:
                    if user != self.bot.user:
                        content = content.replace(user.mention, "").strip()

                # Ensure the bot is mentioned in the response
                response_mentions = [user.mention for user in message.mentions if user != self.bot.user]
                if message.mentions:
                    response_mentions.append(message.author.mention)

                response_text = ""

                # Handle messages with attachments (e.g., images)
                if message.attachments:
                    for attachment in message.attachments:
                        if any(attachment.filename.lower().endswith(ext) for ext in ['png', 'jpg', 'jpeg', 'gif']):
                            img_data = await attachment.read()
                            img = Image.open(io.BytesIO(img_data))

                            # Construct the request content
                            request_content = content if content else "Bu fotoğraf nedir? Detaylı bir şekilde açıklar mısın?"

                            # Send the image and/or text to Google Bard API
                            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                            response = model.generate_content([request_content, img])

                            # Check if the response contains valid content
                            if response and hasattr(response, 'parts') and response.parts:
                                response_text = response.parts[0].text if response.parts[0].text else "Geçerli bir yanıt alınamadı."
                            else:
                                response_text = "Geçerli bir yanıt alınamadı. Lütfen güvenlik değerlendirmelerini kontrol edin."

                # Handle text messages only
                else:
                    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                    response = model.generate_content([content])

                    # Check if the response contains valid content
                    if response and hasattr(response, 'parts') and response.parts:
                        response_text = response.parts[0].text if response.parts[0].text else "Geçerli bir yanıt alınamadı."
                    else:
                        response_text = "Geçerli bir yanıt alınamadı. Lütfen güvenlik değerlendirmelerini kontrol edin."

                # Construct the full message with mentions
                mention_text = ' '.join(response_mentions)
                full_message = f"{mention_text}\n\n{response_text}"

                # Split the message if it's too long
                if len(full_message) > 2000:
                    for i in range(0, len(full_message), 1900):
                        part = full_message[i:i+1900]
                        if i == 0:
                            await message.reply(part)
                        else:
                            await message.channel.send(f"{part}\n\n{mention_text}")
                else:
                    await message.reply(full_message)

                # Add a reaction to the user's message to indicate it was answered
                await message.add_reaction('✅')

            except Exception as e:
                await message.channel.send(f"Bir hata oluştu: {str(e)}")

async def setup(bot):
    await bot.add_cog(GoogleBard(bot))
