import requests
import json
import aiohttp

BASE_URL = 'https://en.wikipedia.org/w/api.php?'


async def wiki_request(session, topic):
    cont = None
    titles = []

    while cont != 'DONE':
        body = await _wiki_request(session, topic, cont)
        _get_titles(body, titles)
        try:
            cont = body['continue']['plcontinue']
        except KeyError:
            cont = 'DONE'

    return titles


async def _wiki_request(session, topic, cont):
    payload = {
        'action': 'query',
        'titles': topic,
        'prop': 'links',
        'format': 'json',
        'pllimit': '500',
    }
    if cont:
        payload['plcontinue'] = cont

    # using 'with' closes the session
    async with session.get(BASE_URL, params=payload) as resp:
        return await resp.json()


def _get_titles(body, titles):
    pages = body['query']['pages']
    links = []

    for page in pages:
        if 'links' in pages[page]:
            links.append(pages[page]['links'])

    for link in links:
        for sub in link:
            titles.append(sub['title'])
