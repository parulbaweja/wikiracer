from graph import WikiGraph
import asyncio
import sys

# main execution of program

# instantiate a left and right graph for source and dest topics
left = WikiGraph()
right = WikiGraph(is_source=False)

# instantiate coroutines or workers for both graphs
coros = [left.fetcher.worker() for i in range(10)]
coros.extend([right.fetcher.worker() for i in range(10)])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(
        left.shortest_path(sys.argv[1], sys.argv[2], right.came_from),
        right.shortest_path(sys.argv[2], sys.argv[1], left.came_from),
        *coros
    ))

