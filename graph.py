from queue import Queue
from wiki import wiki_request
import fetcher
import asyncio
import sys

class WikiGraph(object):
    """
    A Wikipedia page and its outlinks stored as a graph.
    """
    def __init__(self, is_source=True):
        self.graph = {}                         # stores links for all topics
        self.to_visit = asyncio.Queue()         # queue for bfs
        self.fetcher = fetcher.WikiFetch()      # queue up wiki_requests
        self.came_from = {}                     # tracks parent topic & visited
        self.is_source = is_source              # bool for tracking src

    async def shortest_path(self, start, end, dest_cf):
        """
        A breadth-first search for a path between a start and end topic.
        """
        # if start and end are the same, finish fast
        if start == end:
            print([start])
            sys.exit(0)

        # initialize came_from with start node to trace back
        self.came_from[start] = None

        # push start, depth=0 onto queue
        await self.to_visit.put((start, 0))

        while True:
            cur, depth = await self.to_visit.get()

            # if current topic is found in the opposing topic's visited,
            # then path exists and must be traced back on both sides to return
            if cur in dest_cf:
                path1 = self.find_path(self.came_from, cur)
                path2 = self.find_path(dest_cf, cur)

                if self.is_source:
                    _format_path(path1)
                else:
                    _format_path(path2)

                path1.extend(path2)
                print(path1)
                sys.exit(0)

            # condition set to not exceed 20 depths of search
            if depth == 20:
                break

            if cur not in self.graph:
                # add current topic to worker's to_fetch queue
                await self.fetcher.producer(cur, self.queue_links, depth)
                continue
            else:
                # otherwise, add cur's children to to_visit queue
                await self.queue_links(cur, self.graph[cur])

        print('No path found')
        sys.exit(0)

    def find_path(self, parents, dest):
        """
        Traces path from current node to parent.
        """
        path = [dest]
        while parents[dest] is not None:
            path.append(parents[dest])
            dest = parents[dest]

        return path

    async def queue_links(self, cur, resp, depth):
        """
        Adds node's children to to_visit queue for bfs.
        Callback that is fired after worker retrieves wiki_request.
        """
        self.graph[cur] = resp
        for link in resp:
            if link in self.came_from:
                continue
            self.came_from[link] = cur
            await self.to_visit.put((link, depth + 1))

    def _format_path(path):
        """
        Formats path for correct display.
        """
        path1.reverse()
        path1.pop()

