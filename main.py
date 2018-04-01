from queue import Queue
from wiki import wiki_request
import coros
import asyncio
import sys

class WikiGraph(object):
    def __init__(self, isSource=True):
        self.graph = {}
        self.to_visit = asyncio.Queue()
        self.fetcher = coros.WikiFetch()
        self.came_from = {}
        self.isSource = isSource

    async def shortest_path(self, start, end, dest_cf):
        if start == end:
            print([start])
            sys.exit(0)

        self.came_from[start] = None

        await self.to_visit.put((start, 0))

        while True:
            cur, depth = await self.to_visit.get()

            if cur in dest_cf:
                path1 = self.find_path(self.came_from, cur)
                path2 = self.find_path(dest_cf, cur)
                if self.isSource:
                    path1.reverse()
                    path1.pop()
                else:
                    path2.reverse()
                    path2.pop()
                path1.extend(path2)
                print(path1)
                sys.exit(0)

            if depth == 20:
                break

            if cur not in self.graph:
                await self.fetcher.producer(cur, self.queue_links, depth)
                continue
            else:
                await self.queue_links(cur, self.graph[cur])

        print('No path found')
        sys.exit(0)

    def find_path(self, parents, dest):
        path = [dest]
        while parents[dest] is not None:
            path.append(parents[dest])
            dest = parents[dest]

        return path

    async def queue_links(self, cur, resp, depth):
        self.graph[cur] = resp
        for link in resp:
            if link in self.came_from:
                continue
            self.came_from[link] = cur
            await self.to_visit.put((link, depth + 1))

