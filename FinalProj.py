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
    return_type='artist'):
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
        counter += 1
    return(billboard_dict)


# Gets top ten tracks for given artist
def get_top_tracks(artist):
        data = get_data_using_cache(artistName = artist)
        artist_id = data['artists']['items'][0]['uri']
        uri = 'spotify:artist:' + str(artist_id)
        top_tracks_us = spotify.artist_top_tracks(uri)
        top_tracks_list = []
        for track in top_tracks_us['tracks'][:10]:
            top_tracks_list.append(track['name'])
        return(top_tracks_list)


# Gets top ten tracks and billboard data
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


# Interface
def load_help_text():
    with open('help.txt') as f:
        return f.read()

def interactive_prompt():
    help_text = load_help_text()
    print('Type "help" to see more detailed instructions.')
    response = ''
    while response != 'quit' or 'help':
        response = input('Enter any artist to retrieve their top 10 songs from Spotify.\nIf a song is currently charting on the Billboard Hot 100,\nits position on the chart will also be displayed.\nEnter here: ')
        if response == 'help':
            print('----------------------------')
            print(help_text)
            print('----------------------------')
        elif response == 'quit':
            break
        else:
            chart_compare(response)

        # else:
        #     print('Command not recognized:', response)
        #     print('Type "help" to see a list of commands and instructions.')




interactive_prompt()

#Create database
# DBNAME = 'spotifybillboard.db'
# CHARTJSON = 'cached_chart.json'
# MUSICJSON = 'cached_music.json'
#
# def init_db():
#     conn = sqlite.connect(DBNAME)
#     cur = conn.cursor()
#
#     statement = '''
#         DROP TABLE IF EXISTS 'Artist_Data';
#     '''
#
#     cur.execute(statement)
#     conn.commit()
#
#     statement = '''
#         DROP TABLE IF EXISTS 'Chart_Data';
#     '''
#
#     cur.execute(statement)
#     conn.commit()
#
#     statement = '''
#         CREATE TABLE 'Artist_Data' (
#             'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
#             'Company' TEXT,
#             'SpecificBeanBarName' TEXT,
#             'REF' TEXT,
#             'ReviewDate' TEXT,
#             'CocoaPercent' REAL,
#             'CompanyLocation' TEXT,
#             'CompanyLocationId' INTEGER,
#             'Rating' REAL,
#             'BeanType' TEXT,
#             'BroadBeanOrigin' TEXT,
#             'BroadBeanOriginId' INTEGER
#         );
#     '''
#
#     cur.execute(statement)
#     conn.commit()
#
#     statement = '''
#         CREATE TABLE 'Chart_Data' (
#             'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
#             'Alpha2' TEXT,
#             'Alpha3' TEXT,
#             'EnglishName' INTEGER,
#             'Region' TEXT,
#             'Subregion' REAL,
#             'Population' INTEGER,
#             'Area' REAL
#         );
#     '''
#
#     cur.execute(statement)
#     conn.commit()
#     conn.close()






# chart_compare(artist = 'Drake')



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
