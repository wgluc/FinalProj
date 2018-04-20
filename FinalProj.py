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
        return SPOTIFY_CACHED_DICT[artistName]
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
    cache_contents1 = cache_file1.read()
    CHART_CACHE_DICT = json.loads(cache_contents1)
    cache_file1.close()
except:
    CHART_CACHE_DICT = {}

def get_chart_using_cache(baseurl):
    unique_indent = baseurl
    if unique_indent in CHART_CACHE_DICT.keys():
        return CHART_CACHE_DICT[unique_indent]
    else:
        response = requests.get(unique_indent)
        CHART_CACHE_DICT[unique_indent] = response.text
        fref = open('cached_chart.json', 'w')
        dumped_data = json.dumps(CHART_CACHE_DICT)
        fref.write(dumped_data)
        fref.close()
        return CHART_CACHE_DICT[unique_indent]


#Function to scrape billboard charts
def get_billboard():
    url = 'https://www.billboard.com/charts/hot-100'
    html = get_chart_using_cache(baseurl = url)
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find(class_ = 'chart-data js-chart-data')
    main_dis = container.find_all(class_ = 'chart-row__main-display')
    more_info = container.find(class_ = 'container')
    more_stats = more_info.find_all(class_ = 'chart-row__secondary')
    #.find_all(class_ = '')[1]
    billboard_dict = {}
    counter = 1
    for cell in main_dis:
        number_cont = cell.find(class_='chart-row__rank')
        position = number_cont.find(class_='chart-row__current-week')
        title_cont = cell.find(class_= 'chart-row__container')
        info = title_cont.find(class_= 'chart-row__title')
        title = info.find(class_ ='chart-row__song')
        artist = info.find(class_ ='chart-row__artist')
        artist = artist.string.replace('\n', '')
        billboard_dict[counter] = [title.string,artist]
        counter += 1
    counter = 1
    for cell in more_stats:
        inside_stats = cell.find(class_ = 'chart-row__stats')
        peak = inside_stats.find(class_ = 'chart-row__top-spot')
        peak_value = peak.find(class_ = 'chart-row__value')
        week = inside_stats.find(class_ = 'chart-row__weeks-on-chart')
        week_value = week.find(class_ = 'chart-row__value')
        prev_week = inside_stats.find(class_ = 'chart-row__last-week')
        prev_week_value = prev_week.find(class_ = 'chart-row__value')
        billboard_dict[counter].append(peak_value.string)
        billboard_dict[counter].append(week_value.string)
        billboard_dict[counter].append(prev_week_value.string)
        counter += 1
    return(billboard_dict)

class BillboardArtistData():
    def __init__(self, songName = 'Creep', artistName = 'Radiohead',current = 0,
    peak = 0, weeks = 0, previous = 0):
        self.songName = songName
        self.artistName = artistName
        self.current = current
        self.peak = peak
        self.weeks = weeks
        self.previous = previous


    def __str__(self):
        return '{} by {} is currently charting at number {}. Throughout its {} week(s) charting, its top position was {}, and its last position was {}'.format(
        self.songName,self.artistName, self.current, self.weeks, self.peak,
        self.previous)



# Gets top ten tracks for given artist
def get_top_tracks(artist):
        data = get_data_using_cache(artistName = artist)
        try:
            artist_id = data['artists']['items'][0]['uri']
            uri = 'spotify:artist:' + str(artist_id)
            top_tracks_us = spotify.artist_top_tracks(uri)
            top_tracks_list = []
            for track in top_tracks_us['tracks'][:10]:
                top_tracks_list.append(track['name'])
            return(top_tracks_list)
        except:
            print('Invalid search request')
            return None


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
    try:
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
    except:
        print('**********ERROR**********')
        print('There is an issue with your artist. Please avoid using special characters, make sure your search is case sensitive, and make sure it is spelled correctly.\n')
        print('**********ERROR**********')


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


print(get_billboard())





# spot_list['external urls']['name']
# Part1 Oauth page server requests
# baseurl = 'https://api.spotify.com'
# util.prompt_for_user_token('hockeybean',scope = '' ,client_id= secrets.client_id,
# client_secret= secrets.client_secret,redirect_uri= secrets.redirect_uri)
# token = util.oauth2.SpotifyClientCredentials(client_id= secrets.client_id, client_secret= secrets.client_secret)
# cache_token = token.get_access_token()
# spotify = spotipy.Spotify(cache_token)
