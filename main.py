from queue import Queue
from wiki import wiki_request
import coros
# import asyncio
# import aiohttp

class WikiGraph(object):
    def __init__(self):
        self.graph = {}
        self.to_visit = Queue()

    def shortest_path(self, start, end):
        if start == end:
            print('The start and end are the same')
            return

        came_from = {
            start: None,
        }

        self.to_visit.put((start, 0))

        while self.to_visit:
            cur, depth = self.to_visit.get()
            if depth == 10:
                break

            if cur not in self.graph:
                # enqueue for worker
                self.graph[cur] = wiki_request(cur)
            sublinks = self.graph[cur]

            for sublink in sublinks:
                if sublink in came_from:
                    continue
                came_from[sublink] = cur
                if sublink == end:
                    return self.find_path(came_from, sublink)
                self.to_visit.put((sublink, depth + 1))

        print('No path found')

    def find_path(self, parents, dest):

        path = [dest]
        while parents[dest] is not None:
            path.append(parents[dest])
            dest = parents[dest]

        path.reverse()
        return path


# p = WikiGraph('Python', 'Total Film')
# s = p.shortest_path()
# print(s)
