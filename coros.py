import aiohttp
from wiki import wiki_request
import asyncio

class WikiFetch(object):

    def __init__(self):
        self.to_fetch = asyncio.Queue()

    async def worker(self):
        async with aiohttp.ClientSession() as session:
            while True:
                title_to_fetch, cb, depth = await self.to_fetch.get()
                resp = await wiki_request(session, title_to_fetch)
                await cb(title_to_fetch, resp, depth)

    async def producer(self, topic, cb, depth):
        await self.to_fetch.put((topic, cb, depth))

