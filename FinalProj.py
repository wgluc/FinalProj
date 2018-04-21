import spotipy
import secrets
import spotipy.util as util
import json
from bs4 import BeautifulSoup
import requests
import sqlite3 as sqlite
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='wgluc', api_key='XBTn9XbLJRW5K365kcbq')


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


#Class for creating Artist objects according to Billboard
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
            artist_id = data['artists']['items'][0]['id']
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
            if x in billboard_songs:
                print(artist + ' - ' + str(counter) + '. ' + x +
                ': charting at number '+ str(billboard_songs.index(x) + 1) +
                ' on The Billboard Hot 100')
            elif x.split(' (')[0] in billboard_songs and feature in artists_string:
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


# print(get_billboard())

#CREATING DB

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
#             'Artist' TEXT,
#             'Best Song' TEXT,
#             'Followers' TEXT,
#             'Genres' TEXT,
#             'Popularity' INTEGER,
#             'Type' TEXT,
#             'uri' TEXT
#         );
#     '''
#
#     cur.execute(statement)
#     conn.commit()
#
#     statement = '''
#         CREATE TABLE 'Chart_Data' (
#             'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
#             'Position' TEXT,
#             'Peak Position' TEXT,
#             'Previous Position' TEXT,
#             'Weeks Charting' TEXT,
#             'Artist' TEXT,
#             'Song' TEXT
#         );
#     '''
#
#     cur.execute(statement)
#     conn.commit()
#     conn.close()
#
# def populate_db():
#     conn = sqlite.connect('spotifybillboard.db')
#     cur = conn.cursor()
#
#     populate_dict = get_billboard()
#
#     for c in populate_dict.keys():
#         Position = c
#         Peak_Position = populate_dict[c][2]
#         Previous_Position = populate_dict[c][4]
#         Weeks_Charting = populate_dict[c][3]
#         Artist = populate_dict[c][1]
#         Song = populate_dict[c][0]
#
#         insertion = (None, Position, Peak_Position, Previous_Position, Weeks_Charting,
#         Artist, Song)
#         statement = 'INSERT INTO "CHART_DATA" '
#         statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
#         cur.execute(statement, insertion)
#     conn.commit()
#
#     f = open(MUSICJSON, 'r')
#     fcontents = f.read()
#     music_data = json.loads(fcontents)
#
#     for x in music_data.keys():
#         Artist = x
#         Best_Song = get_top_tracks(x)[0]
#         Followers = music_data[x]['artists']['items'][0]['followers']['total']
#         genre_list = music_data[x]['artists']['items'][0]['genres']
#         genre_string = ''
#         for y in genre_list:
#             genre_string += y + ', '
#         Genres = genre_string
#         Popularity = music_data[x]['artists']['items'][0]['popularity']
#         Type = music_data[x]['artists']['items'][0]['type']
#         uri = music_data[x]['artists']['items'][0]['uri']
#
#         insertion = (None, Artist, Best_Song, Followers, Genres, Popularity,
#         Type, uri)
#         statement = 'INSERT INTO "Artist_Data" '
#         statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
#         cur.execute(statement, insertion)
#     conn.commit()
#
#     conn.close()
#
# init_db()
# populate_db()


# plotly
def create_plot_one():
    pos_lst = []
    prev_lst = []
    billboard = get_billboard()
    for spot in billboard.keys():
        try:
            prev_lst.append(int(billboard[spot][4]))
        except:
            prev_lst.append(0)
        pos_lst.append(int(spot))
    trace0 = go.Scatter(x = pos_lst, y = prev_lst, mode = 'markers')
    data = go.Data([trace0])
    layout = dict(title = 'Billboard Previous Position on Current Position',
                  yaxis = dict(zeroline = False),
                  xaxis = dict(zeroline = False)
                 )
    fig = dict(data=data, layout=layout)
    plot_url = py.plot(fig, filename='Plot1')

def create_plot_two():
    pos_lst = []
    weeks_lst = []
    billboard = get_billboard()
    for spot in billboard.keys():
        pos_lst.append(int(spot))
        weeks_lst.append(int(billboard[spot][3]))
    trace0 = go.Scatter(x = pos_lst, y = weeks_lst, mode = 'markers')
    data = go.Data([trace0])
    layout = dict(title = 'Billboard Weeks on Current Position',
                  yaxis = dict(zeroline = False),
                  xaxis = dict(zeroline = False)
                 )
    fig = dict(data=data, layout=layout)
    plot_url = py.plot(fig, filename='Plot2')

def create_plot_three():
    peak_lst = []
    weeks_lst = []
    billboard = get_billboard()
    for spot in billboard.keys():
        peak_lst.append(int(billboard[spot][2]))
        weeks_lst.append(int(billboard[spot][3]))
    trace0 = go.Scatter(x = peak_lst, y = weeks_lst, mode = 'markers')
    data = go.Data([trace0])
    layout = dict(title = 'Billboard Weeks Charting on Peak Position',
                  yaxis = dict(zeroline = False),
                  xaxis = dict(zeroline = False)
                 )
    fig = dict(data=data, layout=layout)
    plot_url = py.plot(fig, filename='Plot3')

def create_plot_four():
    f = open('cached_music.json', 'r')
    fcontents = f.read()
    music_data = json.loads(fcontents)
    followers_list = []
    pop_list = []
    for spot in music_data.keys():
        pop_list.append(music_data[spot]['artists']['items'][0]['popularity'])
        followers_list.append(music_data[spot]['artists']['items'][0]['followers']['total'])
    p_four = 'Spotify Artist Popularity on Artist Followers (from Cached Results)'
    trace0 = go.Scatter(x = followers_list, y = pop_list, mode = 'markers')
    data = go.Data([trace0])
    layout = dict(title = p_four,
                  yaxis = dict(zeroline = False),
                  xaxis = dict(zeroline = False)
                 )
    fig = dict(data=data, layout=layout)
    plot_url = py.plot(fig, filename='Plot4')


# Interface
def load_help_text():
    with open('help.txt') as f:
        return f.read()

def interactive_prompt():
    txt = 'Enter any artist to retrieve their top 10 songs from Spotify.\nIf a song is currently charting on the Billboard Hot 100,\nits position on the chart will also be displayed.\nEnter here: '
    help_text = load_help_text()
    print('Type "help" to see more detailed instructions.')
    choice = ''
    while choice != 'quit' or 'help':
        choice = input('Enter "1" to make artist searches into the Spotify Library\nEnter "2" to view sample graphs from plotly:\n')
        if choice == 'quit':
            break
        elif int(choice) == 1:
            response = input('You have selected to make searches.' + txt)
            while response != 'quit' or 'help':
                chart_compare(response)
                response = input(txt)
                if response == 'help':
                    print('----------------------------')
                    print(help_text)
                    print('----------------------------')
                elif response == 'quit':
                    break
                else:
                    chart_compare(response)
        elif int(choice) == 2:
            print('Enter 1 for "Billboard Previous Position on Current Position" Scatterplot')
            print('Enter 2 for "Billboard Weeks on Current Position" Scatterplot')
            print('Enter 3 for "Billboard Weeks Charting on Peak Position" Scatterplot')
            print('Enter 4 for "Spotify Artist Popularity on Artist Followers"(from Cached Results)" Scatterplot')
            plot_response = input('Enter a number : ')
            while(plot_response != 'quit'):
                if plot_response == 'quit':
                    break
                elif int(plot_response) == 1:
                    create_plot_one()
                elif int(plot_response) == 2:
                    create_plot_two()
                elif int(plot_response) == 3:
                    create_plot_three()
                elif int(plot_response) == 4:
                    create_plot_four()
                elif plot_response == 'help':
                    print(help_text)
                else:
                    print('INVALID INPUT ******** Please type "help" or try again.')
                plot_response = input('Enter a number: ')
        elif choice == 'quit':
            break
        elif choice == 'help':
            print(help_text)
        else:
            print('Please be more prudent in your inputs and searches.' + help_text)




interactive_prompt()
# create_plot_two()
# def create_plot2():
#     billboard = get_billboard()
#     data = []

#         data.append(trace0)
#
#     py.plot(data, filename='Billboard Current Position on Weeks Charting')
#
# def create_plot3():
#     f = open('cached_music.json', 'r')
#     fcontents = f.read()
#     music_data = json.loads(fcontents)
#     billboard = get_billboard()
#     num = 0
#     pop = 0
#     data = []
#     for x in billboard.keys():
#         num = int(x)
#         for y in music.data.keys():
#             pop = int(music_data[y]['artists']['items'][0]['popularity'])
#         trace = go.Scatter(x = num, y = pop)
#         data.append(trace)
#     f = 'Billboard Current Position on Spotify Popularity Score'
#     py.plot(data, filename= f)

# create_plot_one()





















# cache_list = ['Young Thug', 'Migos', 'Kanye West', 'Demi Lovato',
# 'A Tribe Called Quest', 'Lil Uzi Vert', 'Post Malone', 'Tom Misch',
# 'The Beatles', 'Chief Keef', 'Glass Animals', 'Fugees', 'Michael Jackson',
# 'Dave East', 'Drake', 'Future', 'Chance The Rapper', 'Goldlink', 'Kaytranada',
# 'Steve Lacy', 'The Internet', 'Kendrick Lamar', 'Flying Lotus', 'Lil Pump',
# 'Bas', 'Kali Uchis', 'Khalid', 'Famous Dex', 'Flatbush Zombies', 'A$AP Rocky',
# 'Kygo', 'Diplo', 'Rich The Kid', 'Saba', 'Nas', 'Travis Scott', 'The Weeknd',
# 'Denzel Curry', 'Frank Ocean', 'Cardi B', 'Bruno Mars', 'Ed Sheeran', 'Offset',
# 'Quavo', 'Dua Lipa', 'Tupac', 'Nicki Minaj', 'SZA', 'Jay Rock', 'J. Cole',
# '2 Chainz', 'YG', 'Calvin Harris', 'Logic', 'Florida Georgia Line',
# 'Taylor Swift', 'Big Sean', 'Halsey', 'James Blake', 'Rae Sremmurd',
# 'XXXTENTACION', 'Meghan Trainor', 'Rihanna', 'Jason Aldean', 'Chris Brown',
# 'Shawn Mendes', 'Tame Impala', 'Swae Lee', '21 Savage', 'Justin Timberlake',
# 'Dillon Francis', 'Galantis', 'Miller Guth', 'Sam Feldt', 'JPEGMAFIA', 'Trouble',
# 'Swedish House Mafia', 'Tyler, The Creator', 'Syd', 'Frank Sinatra',
# 'Jessie Reyez', 'Billie Eilish', 'Fall Out Boy', 'Sheck Wes', 'Luke Bryan',
# 'Beyonce', 'Chris Stapleton', 'Sampha', 'De La Soul', 'Akon', 'Vic Mensa',
# 'Arctic Monkeys','Tay-K', 'Tchami', 'Thundercat', 'Lil Yachty', 'Lil Wayne',
# 'Solange', 'Louis The Child', 'Lauv', 'Skepta']
#
#
# for x in cache_list:
#     chart_compare(x)




# spot_list['external urls']['name']
# Part1 Oauth page server requests
# baseurl = 'https://api.spotify.com'
# util.prompt_for_user_token('hockeybean',scope = '' ,client_id= secrets.client_id,
# client_secret= secrets.client_secret,redirect_uri= secrets.redirect_uri)
# token = util.oauth2.SpotifyClientCredentials(client_id= secrets.client_id, client_secret= secrets.client_secret)
# cache_token = token.get_access_token()
# spotify = spotipy.Spotify(cache_token)
