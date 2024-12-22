import logging
import asyncio

from http.client import RemoteDisconnected
from pybooru import PybooruHTTPError
from requests.exceptions import ConnectionError

import discord
from discord.ext import commands

from pybooru import Danbooru


class DanbooruCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.danbo = Danbooru('danbooru')

    async def get_posts(self, tag: str, tries=2) -> list:
        for attempt in range(tries):
            try:
                posts = await asyncio.to_thread(
                    self.danbo.post_list,
                    limit=10,
                    tags=tag,
                    random=True
                )
                return posts
            except ConnectionError as e:
                if attempt < tries - 1:
                    logging.error(
                        f"Connection error: {e}. Trying again in 3 seconds.."
                    )
                    await asyncio.sleep(3)
                else:
                    logging.error('Could not reconnect to the remote.')
                    return []
            except PybooruHTTPError as e:
                if '422' in e._msg:
                    logging.error("Invalid tag !")
                return []

    @commands.slash_command(name='danbooru', description='Pick random one image !')
    async def danbooru(
        self,
        ctx: discord.ApplicationContext,
        tag: str
    ):
        await ctx.defer()

        # Search the image
        logging.info(f'Searching for *{tag}*...')
        posts = await self.get_posts(tag)

        if not posts:
            logging.info(f'Could not find the tag *{tag}* !')
            await ctx.respond(f'Could not find the tag *{tag}*...')
            return

        # Find a correct image
        sent = False
        for post in posts:
            # Get variables
            file_url = post.get('file_url', 'Could not fetch the file...')
            id = post.get('id', '?')
            danbooru_url = f'https://danbooru.donmai.us/posts/{id}'

            # Ignore ecchi images
            if post['rating'] in {'q', 'e'}:  # rating:questionable or rating:explicit
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