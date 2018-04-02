from graph import WikiGraph
import asyncio
import sys
from collections import deque

# main execution of program

# async def main():
    # instantiate a left and right graph for source and dest topics
left = WikiGraph()
    # right = WikiGraph(is_source=False)

    # instantiate coroutines or workers for both graphs
    # coros = [right.shortest_path(sys.argv[2], sys.argv[1], left.came_from),
    #          left.shortest_path(sys.argv[1], sys.argv[2], right.came_from)]
coros = [left.fetcher.worker() for i in range(10)]

    # q = deque(coros)
    # while q:
    #     try:
    #         g = q.popleft()
    #         ret = await g.__anext__()
    #         print(ret)
    #         q.append(g)
    #     except StopAsyncIteration:
    #         pass

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    loop.run_until_complete(asyncio.gather(
        left.shortest_path(sys.argv[1], sys.argv[2]),
        # right.shortest_path(sys.argv[2], sys.argv[1], left.came_from),
        *coros
    ))

