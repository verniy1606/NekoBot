import logging
import httpx
import asyncio

from dataclasses import dataclass

@dataclass
class DanboPost:
    id: int
    rating: str
    file_url: str
    tag_string_artist: str
    danbo_url: str
    # created_at: str
    # uploaded_at: str

@dataclass
class DanboArtist:
    id: int
    name: str
    danbo_url: str

@dataclass
class DanboCommentary:
    id: int
    post_id: int
    title: str
    description: str

class DanbooruClient:
    def __init__(self, base_url = 'https://danbooru.donmai.us'):
        self.base_url = base_url
        self.http = httpx.AsyncClient(follow_redirects = True)
    
    def __del__(self):
        # self.http.aclose()
        return

    async def get_http(self, api_url: str, params: list = None) -> list:
        try:
            response = await self.http.get(api_url, params = params)
            response.raise_for_status()

            data = response.json()

            if not data:
                logging.warning('The api returned nothing !')
                return None
            
            return data
        
        except httpx.HTTPStatusError as e:
            logging.error(f'An HTTPStatusError occured during the request !: {e}')
            return None

    async def get_artists(self, artist_url: str) -> list[DanboArtist]:
        api_url = f'{self.base_url}/artists.json'

        params = {
            'search[any_name_or_url_matches]': artist_url
        }

        result = await self.get_http(api_url, params)

        if not result: 
            return []
        
        artists: list[DanboArtist] = []

        for artist in result:
            id = artist.get('id')
            name = artist.get('name', '?')
            danbo_url = f'{self.base_url}/artists/{id}'

            instance = DanboArtist(id = id, name = name, danbo_url = danbo_url)
            artists.append(instance)
        
        return artists
    
    async def get_commentary(self, post_id: str) -> DanboCommentary:
        api_url = f'{self.base_url}/posts/{post_id}/artist_commentary.json'

        result = await self.get_http(api_url)
        
        if not result:
            logging.info(f'The post {post_id} does not have commentaries')
            return DanboCommentary(id = 0, post_id = post_id, title = 'No title provided.', description = 'No description provided.')
        
        id = result.get('id')
        post_id = result.get('post_id')
        original_title = result.get('original_title', '?')
        original_description = result.get('original_description', '?')

        return DanboCommentary(id = id, post_id = post_id, title = original_title, description = original_description)
        
    async def get_posts_by_tag(self, tags: str, limit: int = 5, random: bool = False) -> list[DanboPost]:
        api_url = f'{self.base_url}/posts.json'

        params = {
            'tags': tags, 
            'limit': limit,
            'random': random
        }

        result = await self.get_http(api_url, params)

        if not result:
            return None

        posts: list[DanboPost] = []
        
        for post in result:
            id = post.get('id')
            rating = post.get('rating', '?')
            file_url = post.get('file_url', 'Requires a gold account to see this post, so we could not fetch the file...')
            tag_string_artist = post.get('tag_string_artist', '?')
            danbo_url = f'{self.base_url}/posts/{id}'

            instance = DanboPost(id = id, rating = rating, file_url = file_url, tag_string_artist = tag_string_artist, danbo_url = danbo_url)
            posts.append(instance)

        return posts
    
danbo_global = DanbooruClient()

if __name__ == '__main__':
    async def test():
        client = DanbooruClient()

        artists = await client.get_artists('')
        posts = await client.get_posts_by_tag(tags='nekomimi', random = True)

        if not posts:
            print('Posts is null !')
        
        if not artists:
            print('Artists is null !')
        
        print(f'artists: {artists}')
        print(f'posts: {posts}')

    asyncio.run(test())
