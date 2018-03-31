import aiohttp
from wiki import wiki_request
import asyncio

topics = ['Python', 'Albert Einstein']

class WikiFetch(object):

    def __init__(self):
        self.to_fetch = asyncio.Queue()

    async def worker(i):
        async with aiohttp.ClientSession() as session:
            while True:
                titles = await wiki_request(session, await to_fetch.get())
                print(titles)

    async def producer(topic):
        await to_fetch.put(topic)

    def main():
        coros = [worker(i) for i in range(2)]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(producer(), *coros))

main()
