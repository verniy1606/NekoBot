import logging
import httpx
import urllib
import asyncio

class DanbooruClient:
    def __init__(self, base_url='https://danbooru.donmai.us'):
        self.base_url = base_url
        self.http = httpx.AsyncClient(follow_redirects=True)
    
    def __del__(self):
        # self.http.aclose()
        return

    async def get_http(self, api_url: str, params: list) -> list:
        try:
            response = await self.http.get(api_url, params=params)
            response.raise_for_status()

            data = response.json()

            if not data:
                logging.warning('The api returned nothing !')
                return None
            
            return data
        
        except httpx.RequestException as e:
            logging.error(f'An error occured during the request !: {e}')
            return None

    async def get_artist_by_url(self, artist_url: str) -> list:
        api_url = f'{self.base_url}/artists.json'

        params = {
            'search[url_matches]': artist_url
        }

        result = await self.get_http(api_url, params)
        return result[0] # first artist
        
    async def get_posts_by_tag(self, tags: str, limit: int = 5, random: bool = False) -> list:
        api_url = f'{self.base_url}/posts.json'

        params = {
            'tags': tags, 
            'limit': limit,
            'random': random
        }

        result = await self.get_http(api_url, params)
        return result

if __name__ == '__main__':
    async def test():
        client = DanbooruClient()

        artist = await client.get_artist_by_url('https://twitter.com/ramunezake')
        posts = await client.get_posts_by_tag(tags='nekomimi', random=True)

        if not artist:
            print('OI')
            return
        
        if not posts:
            print('OII')
            return

        print(f'name: {artist['name']} \nid: {artist['id']}')
        print(f'{posts[0]['file_url']}')

    asyncio.run(test())