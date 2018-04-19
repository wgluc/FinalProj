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


#Function to scrape billboard charts
def get_billboard():
    url = 'https://www.billboard.com/charts/hot-100'
    html = get_chart_using_cache(url)
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find(class_ = 'chart-data js-chart-data')
    main_dis = container.find_all(class_ = 'chart-row__main-display')
    billboard_dict = {}
    counter = 1
    for cell in main_dis:
        number_cont = cell.find(class_='chart-row__rank')
        number = number_cont.find(class_='chart-row__current-week')
        title_cont = cell.find(class_= 'chart-row__container')
        info = title_cont.find(class_= 'chart-row__title')
        title = info.find(class_ ='chart-row__song')
        artist = info.find(class_ ='chart-row__artist')
        billboard_dict[counter] = [title.string,artist.string]
        # print(str(counter) + '. ' + ''.join(billboard_dict[counter]))
        counter += 1
    return(billboard_dict)



# Gets top ten tracks for given artist
def get_top_tracks(artist):
        data = get_data_using_cache(artistName = artist)
        artist_id = data['tracks']['items'][0]['artists'][0]['id']
        uri = 'spotify:artist:' + str(artist_id)
        top_tracks_us = spotify.artist_top_tracks(uri)
        top_tracks_list = []
        for track in top_tracks_us['tracks'][:10]:
            top_tracks_list.append(track['name'])
        # counter = 1
        # for x in top_tracks_list:
        #     print(str(counter) + '. ' + str(x))
        #     counter +=1
        return top_tracks_list



def chart_compare(artist):
    billboard = get_billboard()
    billboard_songs = []
    billboard_artists = []
    feature = ''
    for x in billboard.keys():
        billboard_songs.append(billboard[x][0])
    songs_string = '\n'.join(billboard_songs)
    for x in billboard.keys():
        billboard_artists.append(billboard[x][1])
    artists_string = '\n'.join(billboard_artists)
    compare_tracks = get_top_tracks(artist)
    counter = 1
    for x in compare_tracks:
        artist_split = x.split(' (')
        if len(artist_split) > 1:
            feature_split = artist_split[-1].split()
            if len(feature_split) > 1:
                feature = ''.join(feature_split[-1:])[:-1]
        if x in songs_string:
            print(artist + ' - ' + str(counter) + '. ' + x +
            ': charting at number '+ str(billboard_songs.index(x) + 1) +
            ' on The Billboard Hot 100')
        elif x.split(' (')[0] in songs_string and feature in artists_string:
            print(artist + ' - ' + str(counter) + '. ' + x +
            ' charting at number '+ str(billboard_songs.index(x.split(' (')[0])
            + 1) + ' on The Billboard Hot 100')
        else:
            print(artist + ' - ' + str(counter) + '. ' + x + ', not charting')
        counter +=1




chart_compare(artist = 'Drake')

        # elif x.strip('(feat. ' + artist + ')') in billboard_songs and artist in billboard_artists[billboard_songs.index(x)]:
        #         print(artist + ' - ' + str(counter) + '. ' + x +
        #         ' charting at number ' + str(billboard_songs.index(x)+ 1) +
        #         ' on The Billboard Hot 100')

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
