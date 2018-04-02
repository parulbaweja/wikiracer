# WikiRacer

## Summary
Wikiracer is a Python command line tool to solve the WikiRace game. Specifically, the tool allows users to enter a source and destination topic; the tool returns a list of topics that form a path between the source and destination, based on network requests made to the WikiMedia API.

## Prerequisites
1. Python 3.6.5

## Installation
1. `virtualenv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`

To make a query, run the program with your 'Source' and 'Destination':

4. `python main.py 'Source' 'Destination'`

## Implementation
### MVP 1: A Synchronous BFS
The initial MVP included an API for a WikiTopic and a WikiGraph. A WikiGraph is instantiated with a start and end topic. An API call is made to MediaWiki for each topic's children, which are then added to the queue. A dictionary is used to keep track of each topic's parent. The queue continues until a current topic matches the destination. At this point, a path is traced backwards from the current topic to the source topic via the dictionary.

While this method ultimately found the shortest path, it was not optimized for speed. Each check in the BFS is sequential, rather than concurrent: the program must wait for a response from each API call before continuing to search.

### MVP 2: An Asynchronous BFS
To improve the speed, a few options became apparent: use multiple processes, use multiple threads or use coroutines with a single-threaded approach. Processes do not share memory, so running two BFS's without reference to the other seems impractical. Threading may potentially result in collisions.

Python3's asyncio library offers an API to concurrently handle asynchronous network I/O. With event loops, a program can continue without waiting for responses from network calls. Callbacks are fired when the response of a network call is known in the next iteration of the event loop. For WikiRacer, the majority of work is taking place in making network requests, so this option seemed viable.

With this model, we need two asynchronous queues - one for the BFS to check for a match (WikiGraph) and one for a group of workers to fetch from the MediaWiki API (WikiFetcher). The former provides work to the latter, which upon response, issues a callback to insert the new information the WikiGraph.

This approach significantly improved the runtime, as the program is no longer waiting for one network request to complete at a time. Unfortunately, some duplicate work occurs. For example, two Wikipedia pages may have idential sub-links, both sub-links are queued up for network requests and completed. Once they return, the first response is recorded and the second simply replaces the original. While this does not impact accuracy of results, it is an unnecessary step.

### MVP 3: An Asynchronous Double-Ended BFS
In the previous two approaches, the BFS occurred from a single start point. This last approach carries out a BFS from both the start and end topics. Two BFS's run asynchronously, with the start BFS and end BFS assigning workers to make requests for 'links' (links leading out from the page) and 'links here' (links leading to this page) respectively, so the graph meets in the middle.

The speed of the program is now at least 1000x faster. The resulting path is not always the shortest however.

| MVP                                 | Time    |
| ------------------------------------|:-------:|
| 1. A Synchronous BFS                | 30+ min |
| 2. An Asynchronous BFS              | 4 min   |
| 3. An Asynchronous Double-Ended BFS | 1.2 s   |

## Next Steps
1. Create a web server to listen for requests to WikiRacer. Currently, the event loop stops once a path is found and sys.exit(0) is called on the system. With a web server, the systen should not exit altogether, but rather listen for any additional requests. So, Python asyncio library's methods on stopping and ending a loop may be required here.
2. Produce a visual graph for each request, depicting how many topics were searched. This may be done with D3 or another graphing library, using the WikiGraph's came_from dictionary keys as a list of all topics searched and their corresponding parents.
3. Eliminate duplicate work by queuing up only unique network requests or dropping additional request tasks that already exist.
4. If a topic is typed incorrectly, the request will be unsuccessful, so a status code will display and the system will exit. For a web server, display that the input is incorrect/invalid and/or provide corrections.
