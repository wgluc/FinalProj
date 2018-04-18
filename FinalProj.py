import spotipy
import secrets
import spotipy.util as util
import json
from bs4 import BeautifulSoup
import sys
import requests

#Oauth2 Set Up
token = util.oauth2.SpotifyClientCredentials(client_id=secrets.client_id,
client_secret=secrets.client_secret)
cache_token = token.get_access_token()
spotify = spotipy.Spotify(cache_token)

#SPOTIFY CACHE
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
    search_dict = spotify.search(q=field + str(artistName),
    type=return_type)
    keys = []
    for i in search_dict.keys():
        keys.append(i)
    if artistName in keys:
        return SPOTIFY_CACHED_DICT[key]
    else:
        response = spotify.search(q=field + str(artistName),
        type=return_type)
        SPOTIFY_CACHED_DICT[artistName] = response
        fref = open('cached_music.json','w')
        dumped_data = json.dumps(SPOTIFY_CACHED_DICT)
        fref.write(dumped_data)
        fref.close()
        return SPOTIFY_CACHED_DICT[artistName]

#Billboard Cache
CACHE_FNAME2 = 'cached_chart.json'
try:
    cache_file1 = open(CACHE_FNAME2, 'r')
    cache_contents1 = cache_file.read()
    CHART_CACHE_DICT = json.loads(cache_contents)
    cache_file1.close()
except:
    CHART_CACHE_DICT = {}
#artist_top_tracks(artist_id, country='US')

def get_chart_using_cache(baseurl):
    unique_indent = baseurl
    if baseurl in CHART_CACHE_DICT:
        return CHART_CACHE_DICT[baseurl]
    else:
        response = requests.get(baseurl)
        CHART_CACHE_DICT[unique_indent] = response.text
        fref = open('cached_chart.json', 'w')
        dumped_data = json.dumps(CHART_CACHE_DICT)
        fref.write(dumped_data)
        fref.close()
        return CHART_CACHE_DICT[unique_indent]

def get_billboard():
    url = 'https://www.billboard.com/charts/hot-100'
    html = get_chart_using_cache(url)
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find(class_ = 'chart-data js-chart-data')
    main_dis = container.find_all(class_ = 'chart-row__main-display')
    billboard_dict = {}
    for cell in main_dis:
        counter = 1
        number_cont = cell.find(class_='chart-row__rank')
        number = number_cont.find(class_='chart-row__current-week')
        title_cont = cell.find(class_= 'chart-row__container')
        info = title_cont.find(class_= 'chart-row__title')
        title = info.find(class_ ='chart-row__song')
        artist = info.find(class_ ='chart-row__artist')
        counter = 1
        billboard_dict[counter] = [title.string,artist.string]
        print('--------------------')
        print(str(counter) + '. ' + ''.join(billboard_dict[counter]))
        counter += 1


        # for x in billboard_dict.keys:
            # print(billboard_dict[x].split('\n'))

def get_top_tracks(artist):
        data = get_data_using_cache(artistName = artist)
        artist_id = data['tracks']['items'][0]['artists'][0]['id']
        uri = 'spotify:artist:' + str(artist_id)
        top_tracks_us = spotify.artist_top_tracks(uri)
        for track in top_tracks_us['tracks'][:10]:
            counter = 0
            counter += 1
            print(str(counter) + '. ' + track['name'])

get_billboard()
get_top_tracks(artist = 'Taylor Swift')



# Example Cache Population
# x = ''
# while x != 'quit':
#     x = str(input('What artist would you like to search?'))
#     results = get_data_using_cache(artistName = x)
#     print(results)






# spot_list['external urls']['name']
# Part1 Oauth page server requests
# baseurl = 'https://api.spotify.com'
# util.prompt_for_user_token('hockeybean',scope = '' ,client_id= secrets.client_id,
# client_secret= secrets.client_secret,redirect_uri= secrets.redirect_uri)
# token = util.oauth2.SpotifyClientCredentials(client_id= secrets.client_id, client_secret= secrets.client_secret)
# cache_token = token.get_access_token()
# spotify = spotipy.Spotify(cache_token)
