from main import WikiGraph
import asyncio
import coros
import sys

left = WikiGraph()
right = WikiGraph(isSource=False)

coros = [left.fetcher.worker() for i in range(10)]
coros.extend([right.fetcher.worker() for i in range(10)])
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    left.shortest_path(sys.argv[1], sys.argv[2], right.came_from),
    right.shortest_path(sys.argv[2], sys.argv[1], left.came_from),
    *coros
))

