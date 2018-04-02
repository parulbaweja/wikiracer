import requests
import json
import aiohttp
import sys

BASE_URL = 'https://en.wikipedia.org/w/api.php?'


async def wiki_request(session, topic, is_source):
    """
    Sends wiki request to obtain links for a topic.
    Due to a 500 link limit, additional requests must be sent based on the
    'continue' response.
    """

    cont = None
    titles = []

    while cont != 'DONE':
        if is_source:
            body = await _get_links(session, topic, cont)
            cont_type = 'plcontinue'
        else:
            body = await _get_linkshere(session, topic, cont)
            cont_type = 'lhcontinue'

        _get_titles(body, titles, cont_type)
        try:
            cont = body['continue'][cont_type]
        except KeyError:
            cont = 'DONE'

    return titles


async def _get_links(session, topic, cont):
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


async def _get_linkshere(session, topic, cont):
    """
    Helper function for single wiki request.
    """
    payload = {
        'action': 'query',
        'titles': topic,
        'prop': 'linkshere',
        'format': 'json',
        'lhlimit': '500',
    }

    if cont:
        payload['lhcontinue'] = cont

    # using 'with' closes the session
    async with session.get(BASE_URL, params=payload) as resp:
        # check to see if response is OK
        if resp.status // 100 == 2:
            return await resp.json()
        else:
            print(resp.status)
            sys.exit(1)

def _get_titles(body, titles, cont_type):
    """
    Adds titles from response to list.
    Responses typically have one page of links, but accounted for several in
    case.
    """

    pages = body['query']['pages']
    links = []
    if cont_type == 'plcontinue':
        link_type = 'links'
    else:
        link_type = 'linkshere'

    for page in pages:
        if link_type in pages[page]:
            links.append(pages[page][link_type])

    for link in links:
        for sub in link:
            titles.append(sub['title'])
