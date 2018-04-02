import aiohttp
from wiki import wiki_request
import asyncio

class WikiFetch(object):
    """
    An asynchronous queue of workers listening for tasks from the WikiGraph.
    Producers put work on the queue, while workers retrieve tasks and await
    wiki_requests. Callbacks are fired upon response.
    """

    def __init__(self):
        self.to_fetch = asyncio.Queue()

    async def worker(self):
        async with aiohttp.ClientSession() as session:
            while True:
                title_to_fetch, cb, depth, is_source = await self.to_fetch.get()
                resp = await wiki_request(session, title_to_fetch, is_source)
                await cb(title_to_fetch, resp, depth, is_source)

    async def producer(self, topic, cb, depth, is_source):
        await self.to_fetch.put((topic, cb, depth, is_source))

