
import logging

import discord
from discord.ext import commands

from utils.api_danbooru import DanboPost, DanboArtist, DanboCommentary, danbo_global

async def build_embed_by_tag(danbo_tag: str) -> discord.Embed | None:
    # Search for the tag
    logging.info(f'Searching for *{danbo_tag}*...')
    posts = await danbo_global.get_posts_by_tag(danbo_tag, limit = 5, random = True)
    
    if not posts:
        logging.info(f'Could not find the tag *{danbo_tag}* !')
        # return discord.Embed(title = 'Could not find the tag !')
        return None
    
    # Prepare variables
    chosen_post: DanboPost
    post_commentary: DanboCommentary
    post_artist: DanboArtist

    # Find one safe post from the posts
    chosen = False
    for post in posts:
        # Ignore unsafe images
        if post.rating in {'q', 'e'}:  # rating:questionable or rating:explicit
            logging.info(f'The image is too ecchi !: {post.danbo_url}')
            continue
        
        chosen_post = post  
        post_commentary = await danbo_global.get_commentary(post.id)
        post_artist: DanboArtist = (await danbo_global.get_artists(post.tag_string_artist))[0]
        logging.info(f'Found a post !: {post.danbo_url}')

        chosen = True
        break

    if not chosen:
        logging.info('These posts were too ecchi for this bot ! Try again to fetch another posts !')
        return discord.Embed(title = 'Try again to fetch another posts !')

    # Prepare for the embed
    embed = discord.Embed(
        title = chosen_post.danbo_url,
        description = f'[{post_artist.name}]({post_artist.danbo_url})',
        color = discord.Colour.nitro_pink()
    )
    embed.set_image(url = chosen_post.file_url)
    embed.add_field(name = post_commentary.title, value = post_commentary.description)

    return embed

class DiscordButtonView(discord.ui.View):
    def __init__(self, search_tag: str):
        super().__init__(timeout = 30)
        self.search_tag = search_tag

    async def on_timeout(self):
        logging.info(f'DiscordButtonView with the tag {self.search_tag} has timed out !')

    @discord.ui.button(label = 'More !', style = discord.ButtonStyle.primary, emoji = '🐱')
    async def button_callback(ctx, button: discord.ui.Button, interaction: discord.Interaction):
        tag = button.view.search_tag
        embed = await build_embed_by_tag(tag)
        
        await interaction.response.send_message(f'More for *{tag}* ! <:521089271:1320383029876883557>', embed = embed, view = button.view)

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

        # Send to discord
        embed = await build_embed_by_tag(tag)

        if not embed:
            await ctx.respond('Could not find the tag !')
        else:
            await ctx.respond(f'Here we go ! *{tag}* <:521089271:1320383029876883557>', embed = embed, view = DiscordButtonView(tag))

def setup(bot):
    bot.add_cog(DanboRandomCommand(bot))