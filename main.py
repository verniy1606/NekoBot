import os
import logging

import discord
import google.generativeai as genai

GEMINI_TOKEN = os.getenv("GEMINI_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)

genai.configure(api_key=GEMINI_TOKEN)

bot = discord.Bot()

for filename in os.listdir("./commands"):
    if filename.endswith(".py"):
        bot.load_extension(f"commands.{filename[:-3]}")

@bot.event
async def on_ready():
    logging.info(f"{bot.user} is ready !")

bot.run(DISCORD_TOKEN)