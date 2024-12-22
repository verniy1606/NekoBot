import logging

import discord
from discord.ext import commands

from pybooru import Danbooru

class DanbooruCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.danbooru = Danbooru('danbooru')

    @commands.slash_command(name='danbooru', description='Pick random one image !')
    async def danbooru(
        self, 
        ctx: discord.ApplicationContext, 
        index: discord.Option(
            str,
            description='When *searchtype* is set to *artist*, this property is used to search an user',
            required=True
        ), # type: ignore
        searchtype: discord.Option(
            str,
            choices=[
                'artist',
                'global'
            ],
            description='just a test',
            required=True,
        ) # type: ignore
    ):
        await ctx.defer()

        tag = ''

        if searchtype == 'artist':
            artists = self.danbooru.artist_list(index)
            for artist in artists:
                tag = artist['name']
        elif searchtype == 'global':
            tag = index

        logging.info(f'Searching for *{tag}*...')

        posts = self.danbooru.post_list(limit=1, tags=tag, random=True)

        if not posts:
            logging.info(f'Could not find the tag *{tag}* !')

            await ctx.respond(f'Could not find the tag *{tag}*...')
            return

        for post in posts:
            file_url = post.get('file_url', 'Could not fetch the file...')
            rating = post.get('rating', '?')
            source = post.get('source', '?')
            id = post.get('id', '?')

            danbooru_url = f'https://danbooru.donmai.us/posts/{id}'
            
            if rating == 'q' or rating == 'e': # rating:questionable or rating:explicit
                logging.info(f'The image is too ecchi !: {danbooru_url}')

                await ctx.respond(f'This post is too ecchi for this bot ! Try again to fetch another image')
                return

            await ctx.respond(f'Here we go ! *{tag}* <:521089271:1320383029876883557> \n<{danbooru_url}> \n{file_url}')

            logging.info(f'The image was sent !: {danbooru_url}')

def setup(bot):
    bot.add_cog(DanbooruCommand(bot))