import discord
from discord.ext import commands

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ping")
    async def ping(self, ctx: discord.ApplicationContext):
        latency = round(self.bot.latency*1000, 2)
        await ctx.respond(f"It took {latency}ms !")

def setup(bot):
    bot.add_cog(PingCommand(bot))