import unittest
import json
import requests
import webbrowser
import spotipy
import client
import oauth2
import secrets


CACHE_FNAME = 'cached_music.json'
baseurl = https://api.spotify.com

def get_data_using_cache(baseurl):
    unique_indent = baseurl
    if baseurl in CACHE_DICT:
        return CACHE_DICT[baseurl]
    else:
        response = requests.get(baseurl)
        CACHE_DICT[unique_indent] = response.text
        fref = open('cached_music.json', 'w')
        dumped_data = json.dumps(CACHE_DICT)
        fref.write(dumped_data)
        fref.close()
        return CACHE_DICT[unique_indent]
