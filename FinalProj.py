import spotipy
import secrets
import spotipy.util as util
import json
from bs4 import BeautifulSoup
import sys

token = util.oauth2.SpotifyClientCredentials(client_id=secrets.client_id,
client_secret=secrets.client_secret)
cache_token = token.get_access_token()
spotify = spotipy.Spotify(cache_token)


CACHE_FNAME = 'cached_music.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    SPOTIFY_CACHED_DICT = json.loads(cache_contents)
    cache_file.close()
except:
    SPOTIFY_CACHED_DICT = {}

def get_data_using_cache(field='artist:',artistName = 'Radiohead',
return_type='track'):
    spotify_dict = (spotify.search(q=field + str(artistName),
    type=return_type))
    key = ['tracks']['href']
    #check what Key is here ^
    if key in SPOTIFY_CACHED_DICT:
        return SPOTIFY_CACHED_DICT[unique_indent]
    else:
        response = spotify.search(q=field + str(artistName),
        type=return_type)
        SPOTIFY_CACHED_DICT[unique_indent] = response
        fref = open('cached_music.json','w')
        dumped_data = json.dumps(SPOTIFY_CACHED_DICT)
        fref.write(dumped_data)
        fref.close()
        return SPOTIFY_CACHED_DICT[unique_indent]

x = ''
while x != 'quit':
    x = str(input('What artist would you like to search?'))
    get_data_using_cache(artistName = x)
    spot_list = spotify.search(q='artist'+ str(x))
    print(refined_list)

tracks = []

spot_list['external urls']['name']



results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])




# Part1 Oauth page server requests
# baseurl = 'https://api.spotify.com'
# util.prompt_for_user_token('hockeybean',scope = '' ,client_id= secrets.client_id,
# client_secret= secrets.client_secret,redirect_uri= secrets.redirect_uri)
# token = util.oauth2.SpotifyClientCredentials(client_id= secrets.client_id, client_secret= secrets.client_secret)
# cache_token = token.get_access_token()
# spotify = spotipy.Spotify(cache_token)
#
#
# try:
#     cache_file = open(CACHE_FNAME, 'r')
#     cache_contents = cache_file.read()
#     SPOTIFY_CACHED_DICT = json.loads(cache_contents)
#     cache_file.close()
# except:
#     SPOTIFY_CACHED_DICT = {}
#
# def process_json_dict(self, json_dict):
#
#
# def get_spotify_cache(baseurl, params):
#     unique_ident = oauth.get(baseurl, params=params).url
#     spotify.artist_albums(birdy_uri, album_type='album')
#     if unique_ident in SPOTIFY_CACHED_DICT:
#         return TWITTER_CACHE_DICT[unique_ident]
#     else:
#         resp = oauth.get(baseurl, params=params)
#         SPOTIFY_CACHED_DICT[unique_ident] = json.loads(resp.text)
#         f = open('twitter_cache.json', 'w')
#         dumped_json = json.dumps(SPOTIFY_CACHED_DICT)
#         f.write(dumped_json)
#         f.close()
#         return SPOTIFY_CACHED_DICT[unique_ident]
