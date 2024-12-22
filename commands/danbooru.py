import os
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

        logging.info(tag)

        posts = self.danbooru.post_list(limit=1, tags=tag, random=True)
        logging.info(f'posts: {posts}')

        if not posts:
            await ctx.respond(f'Could not find the tag *{tag}*...')
            return

        for post in posts:
            result = post.get('file_url', 'Could not fetch the file...')
            rating = post.get('rating', '?')
            source = post.get('source', '?')
            
            if rating == 'q' or rating == 'e': # rating:questionable or rating:explicit
                await ctx.respond(f'This post is too ecchi for this bot ! try again to fetch another image')
                return

            await ctx.respond(f'Here we go ! *{tag}* <:521089271:1320383029876883557> \n<https://danbooru.donmai.us/posts/{post['id']}> \n{result} \n[source](<{source}>)')

            logging.info(result)

def setup(bot):
    bot.add_cog(DanbooruCommand(bot))