import os
import logging

import discord
from discord.ext import commands
class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ping")
    async def ping(self, ctx: discord.ApplicationContext):
        if ctx.author.bot:
            print("omae dare")
        latency = round(self.bot.latency*1000, 2)
        await ctx.respond(f"{latency}ms かかりました!")

def setup(bot):
    bot.add_cog(PingCommand(bot))