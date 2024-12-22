import logging

import discord
from discord.ext import commands

import google.generativeai as genai

class GeminiCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
        self.chat = self.model.start_chat()

    @commands.slash_command(name="gemini")
    async def gemini(self, ctx: discord.ApplicationContext, content: str):
        await ctx.defer()
        
        message = await self.chat.send_message_async(content)
        logging.info(f'{ctx.user} said "{content}": Gemini replied "{message.text}"')
        await ctx.respond(message.text)

def setup(bot):
    bot.add_cog(GeminiCommand(bot))