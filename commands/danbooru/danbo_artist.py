import logging

import discord
from discord.ext import commands

from utils.api_danbooru import danbo_global

class DanboArtistCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name = 'danbo_artist', description = 'Find an artist by their name or media links !')
    async def danbo_artist(
        self, 
        ctx: discord.ApplicationContext, 
        artist_name: str
    ):
        artists = await danbo_global.get_artists(artist_name)
        
        if not artists:
            logging.info(f'Could not find the artist *{artist_name}* !')
            await ctx.respond(f'Could not find the artist ! ...')
            return
        
        # Have to do Multiple artists support
        embed = discord.Embed(
            title = artists[0].name,
            description = artists[0].danbo_url
        )

        await ctx.respond(f'Here is the result ! <:521089271:1320383029876883557>', embed = embed)
        return

def setup(bot):
    bot.add_cog(DanboArtistCommand(bot))