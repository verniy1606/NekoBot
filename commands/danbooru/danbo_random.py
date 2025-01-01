import logging

import discord
from discord.ext import commands

from utils.api_danbooru import danbo_global, DanboArtist

class DanboRandomCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name = 'danbo_random', description = 'Pick random one image !')
    async def danbo_random(
        self,
        ctx: discord.ApplicationContext,
        tag: str
    ):
        await ctx.defer()

        # Search the image
        logging.info(f'Searching for *{tag}*...')
        posts = await danbo_global.get_posts_by_tag(tag, limit = 5, random = True)

        if not posts:
            logging.info(f'Could not find the tag *{tag}* !')
            await ctx.respond(f'Could not find the tag ! ...')
            return

        # Find a correct image
        sent = False
        for post in posts:
            # Ignore ecchi images
            if post.rating in {'q', 'e'}:  # rating:questionable or rating:explicit
                logging.info(f'The image is too ecchi !: {post.danbo_url}')
                continue

            # Prepare variables
            commentary = await danbo_global.get_commentary(post.id)
            artist: DanboArtist = (await danbo_global.get_artists(post.tag_string_artist))[0]

            embed = discord.Embed(
                title = post.danbo_url,
                description = f'[{artist.name}]({artist.danbo_url})',
                color = discord.Colour.nitro_pink()
            )
            embed.set_image(url = post.file_url)
            embed.add_field(name = commentary.title, value = commentary.description)

            # Send to discord
            await ctx.respond(f'Here we go ! *{tag}* <:521089271:1320383029876883557>', embed = embed)
            logging.info(f'The image was sent !: {post.danbo_url}')

            sent = True
            break

        if not sent:
            await ctx.respond(f'These posts were too ecchi for this bot ! Try again to fetch another images')

def setup(bot):
    bot.add_cog(DanboRandomCommand(bot))