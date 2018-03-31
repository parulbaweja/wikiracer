from queue import Queue
from wiki import wiki_request
import coros
import asyncio
# import aiohttp

class WikiGraph(object):
    def __init__(self):
        self.graph = {}
        self.to_visit = asyncio.Queue()
        self.fetcher = coros.WikiFetch()
        self.came_from = {}

    async def shortest_path(self, start, end):
        if start == end:
            print('The start and end are the same')
            return

        self.came_from[start] = None

        await self.to_visit.put((start, 0))

        while True:
            cur, depth = await self.to_visit.get()

            if cur == end:
                return self.find_path(self.came_from, cur)

            if depth == 10:
                return

            if cur not in self.graph:
                await self.fetcher.producer(cur, self.queue_links, depth)
                continue
            else:
                await self.queue_links(cur, self.graph[cur])

        print('No path found')

    def find_path(self, parents, dest):
        path = [dest]
        while parents[dest] is not None:
            path.append(parents[dest])
            dest = parents[dest]

        path.reverse()
        print(path)
        return path

    async def queue_links(self, cur, resp, depth):
        self.graph[cur] = resp
        for link in resp:
            if link in self.came_from:
                continue
            self.came_from[link] = cur
            await self.to_visit.put((link, depth + 1))


p = WikiGraph()
coros = [p.fetcher.worker() for i in range(10)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    p.shortest_path('Python', 'Total Film'),
    *coros
))
