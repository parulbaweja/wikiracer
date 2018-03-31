import requests
import json

BASE_URL = 'https://en.wikipedia.org/w/api.php?'


def wiki_request(topic):
    cont = None
    titles = []

    while cont != 'DONE':
        body = _wiki_request(topic, cont)
        _get_titles(body, titles)
        try:
            cont = body['continue']['plcontinue']
        except KeyError:
            cont = 'DONE'

    return titles


def _wiki_request(topic, cont):
    payload = {
        'action': 'query',
        'titles': topic,
        'prop': 'links',
        'format': 'json',
        'pllimit': '500',
        'plcontinue': cont,
    }

    body = requests.get(BASE_URL, params=payload)
    return json.loads(body.text)


def _get_titles(body, titles):
    pages = body['query']['pages']
    links = []

    for page in pages:
        if 'links' in pages[page]:
            links.append(pages[page]['links'])

    for link in links:
        for sub in link:
            titles.append(sub['title'])
