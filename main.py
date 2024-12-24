import os
import logging
from pathlib import Path

import discord
import google.generativeai as genai

from utils.api_danbooru import DanbooruClient

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
bot.danbo = DanbooruClient()

command_path = Path('./commands')

for filepath in command_path.rglob('*.py'):
    relative_path = filepath.relative_to(command_path).with_suffix('')

    module_name = f'commands.{relative_path.as_posix().replace('/', '.')}'
    bot.load_extension(f"{module_name}")

@bot.event
async def on_ready():
    logging.info(f"{bot.user} is ready !")

bot.run(DISCORD_TOKEN)