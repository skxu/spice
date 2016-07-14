from sys import exit
from sys import stderr
from time import sleep
import spice
import constants
import requests

def get_query_url(medium, query):
    query = query.strip()
    terms = query.replace(' ', '+')
    if medium == spice.Medium.ANIME:
        return constants.ANIME_QUERY_BASE + terms
    elif medium == spice.Medium.MANGA:
        return constants.MANGA_QUERY_BASE + terms
    else:
        return None

def get_scrape_url(id, medium):
    id_str = str(id).strip()
    if medium == spice.Medium.ANIME:
        return constants.ANIME_SCRAPE_BASE + id_str
    elif medium == spice.Medium.MANGA:
        return constants.MANGA_SCRAPE_BASE + id_str
    else:
        return None

def get_post_url(id, medium, op):
    if op == spice.Operations.ADD:
        if medium == spice.Medium.ANIME:
            return constants.ANIME_ADD_BASE.format(id) +  constants.OP_SUFFIX
        elif medium == spice.Medium.MANGA:
            return constants.MANGA_ADD_BASE.format(id) +  constants.OP_SUFFIX
    elif op == spice.Operations.UPDATE:
        if medium == spice.Medium.ANIME:
            return constants.ANIME_UPDATE_BASE.format(id) +  constants.OP_SUFFIX
        elif medium == spice.Medium.MANGA:
            return constants.MANGA_UPDATE_BASE.format(id) +  constants.OP_SUFFIX
    else:
        if medium == spice.Medium.ANIME:
            return constants.ANIME_DELETE_BASE.format(id) +  constants.OP_SUFFIX
        elif medium == spice.Medium.MANGA:
            return constants.MANGA_DELETE_BASE.format(id) +  constants.OP_SUFFIX

    return None

def verif_auth():
    verif_resp = requests.get(constants.CREDENTIALS_VERIFY,
                              auth=spice.credentials)
    if verif_resp.status_code == 200:
        return True
    else:
        return False


def get_list_url(medium, user):
    if medium == spice.Medium.ANIME:
        return constants.ANIMELIST_BASE.format(user)
    elif medium == spice.Medium.MANGA:
        return constants.MANGALIST_BASE.format(user)
    else:
        return None

def reschedule(func, wait, *args):
    stderr.write("Too many requests. Waiting 5 seconds.\n")
    sleep(wait)
    return func(*args)

def find_key(status_num, medium):
    if status_num == str(spice.Status.READING):
        if medium == spice.Medium.MANGA:
            return spice.Keys.READING
        elif medium == spice.Medium.ANIME:
            return spice.Keys.WATCHING
        else:
            return None
    elif status_num == str(spice.Status.COMPLETED):
        return spice.Keys.COMPLETED
    elif status_num == str(spice.Status.ONHOLD):
        return spice.Keys.ONHOLD
    elif status_num == str(spice.Status.DROPPED):
        return spice.Keys.DROPPED
    elif status_num == str(spice.Status.PLANTOREAD):
        if medium == spice.Medium.MANGA:
            return spice.Keys.PLANTOREAD
        elif medium == spice.Medium.ANIME:
            return spice.Keys.PLANTOWATCH
        else:
            return None
    else:
        return None

if __name__ == '__main__':
    exit(0)
