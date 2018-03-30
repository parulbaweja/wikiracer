import requests
import json
from queue import Queue

class WikiTopic(object):
    def __init__(self, topic):
        self.topic = topic
        self.links = self.get_titles()

    def wiki_request(self):
        payload = {
            'action': 'query',
            'titles': self.topic,
            'prop': 'links',
            'format': 'json',
            'pllimit': '500'
        }

        r = requests.get('https://en.wikipedia.org/w/api.php?', params=payload)
        return json.loads(r.text)

    def get_titles(self):

        r = self.wiki_request()
        pages = r['query']['pages']
        links = []
        for page in pages:
            if 'links' in pages[page]:
                links.append(pages[page]['links'])

        titles = []
        for link in links:
            for sub in link:
                titles.append(sub['title'])
        return titles


class WikiGraph(object):
    def __init__(self, start, end):
        self.start = WikiTopic(start)
        self.end = WikiTopic(end)
        self.graph = {}

    def shortest_path(self):
        if self.start.topic == self.end.topic:
            print('The start and end are the same')
            return

        came_from = {
            self.start.topic: None,
        }

        to_visit = Queue()
        to_visit.put(self.start.topic)

        while to_visit:
            cur = to_visit.get()
            self.graph[cur] = WikiTopic(cur).get_titles()
            sublinks = self.graph[cur]

            for sublink in sublinks:
                if sublink in came_from:
                    continue
                came_from[sublink] = cur
                if sublink == self.end.topic:
                    return self.find_path(came_from, sublink)
                to_visit.put(sublink)

        print('No path found')

    def find_path(self, parents, dest):

        path = [dest]
        while parents[dest] is not None:
            path.append(parents[dest])
            dest = parents[dest]

        path.reverse()
        return path


p = WikiGraph('Python', 'Total Film')
s = p.shortest_path()
print(s)
