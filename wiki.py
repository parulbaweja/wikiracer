import requests
import json
import aiohttp
import sys

BASE_URL = 'https://en.wikipedia.org/w/api.php?'


async def wiki_request(session, topic):
    """
    Sends wiki request to obtain links for a topic.
    Due to a 500 link limit, additional requests must be sent based on the
    'continue' response.
    """

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
    """
    Helper function for single wiki request.
    """
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
        # check to see if response is OK
        if resp.status // 100 == 2:
            return await resp.json()
        else:
            print(resp.status)
            sys.exit(1)


def _get_titles(body, titles):
    """
    Adds titles from response to list.
    Responses typically have one page of links, but accounted for several in
    case.
    """

    pages = body['query']['pages']
    links = []

    for page in pages:
        if 'links' in pages[page]:
            links.append(pages[page]['links'])

    for link in links:
        for sub in link:
            titles.append(sub['title'])
