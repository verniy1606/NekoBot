import logging

import discord
from discord.ext import commands

from utils.api_danbooru import DanbooruClient

class DanbooruCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.danbo = Danbooru('danbooru')
        self.danbo = DanbooruClient()

    @commands.slash_command(name='danbooru', description='Pick random one image !')
    async def danbooru(
        self,
        ctx: discord.ApplicationContext,
        tag: str
    ):
        await ctx.defer()

        # Search the image
        logging.info(f'Searching for *{tag}*...')
        posts = await self.danbo.get_posts_by_tag(tag, limit=5, random=True)

        if not posts:
            logging.info(f'Could not find the tag *{tag}* !')
            await ctx.respond(f'Could not find the tag *{tag}*...')
            return

        # Find a correct image
        sent = False
        for post in posts:
            # Get variables
            file_url = post.get('file_url', 'Requires a gold account to see this post, so we could not fetch the file...')
            id = post.get('id', '?')
            rating = post.get('rating', '?')

            danbooru_url = f'https://danbooru.donmai.us/posts/{id}'

            # Ignore ecchi images
            if rating in {'q', 'e'}:  # rating:questionable or rating:explicit
                logging.info(f'The image is too ecchi !: {danbooru_url}')
                continue

            # Send to discord
            await ctx.respond(f'Here we go ! *{tag}* <:521089271:1320383029876883557> \n<{danbooru_url}> \n{file_url}')
            logging.info(f'The image was sent !: {danbooru_url}')

            sent = True
            break

        if not sent:
            await ctx.respond(f'This post is too ecchi for this bot ! Try again to fetch another image')

def setup(bot):
    bot.add_cog(DanbooruCommand(bot))