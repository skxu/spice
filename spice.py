from bs4 import BeautifulSoup
import requests
from objects import Anime
from objects import Manga
import helpers
import sys

this = sys.modules[__name__]
this.credentials = None

ANIME = 'anime'
MANGA = 'manga'

def init_auth(username, password):
    this.credentials = (username, password)
    return (username, password)

def search(query, medium):
    api_query = helpers.get_query_url(id, medium, query)
    search_resp = requests.get(api_query, auth=credentials)
    results = BeautifulSoup(search_resp.text, 'lxml')
    if medium == ANIME:
        return [Anime(entry) for entry in results.anime.findAll('entry')]
    elif medium == MANGA:
        return [Manga(entry) for entry in results.manga.findAll('entry')]
    else:
        return None

def search_id(id, medium):
    scrape_query = helpers.get_scrape_url(id, medium)
    search_resp = requests.get(scrape_query)
    results = BeautifulSoup(search_resp.text, 'html.parser')
    #inspect element on an anime page, you'll see where this scrape is
    #coming from.
    query = results.find('span', {'itemprop':'name'})
    matches = search(query.text, medium)
    for match in matches:
        if match.id == str(id):
            return match

    return None

def add(data, id, medium):
    _op(data, id, medium, 'add')

def update(data, id, medium):
    _op(data, id, medium, 'update')

def delete(data, id, medium):
    _op(data, id, medium, 'delete')

def _op(data, id, medium, op):
    post = helpers.get_post_url(id, medium, op)
    post = post + ".xml?data=" + data.to_xml()
    headers = {'Content-type': 'application/xml', 'Accept': 'text/plain'}
    #MAL API is broken to hell -- you have to actually use GET
    #and chuck the data into the URL as seen above and below...
    r = requests.get(post, headers=headers, auth=credentials)

if __name__ == '__main__':
    print("Spice is meant to be imported into a project.")
