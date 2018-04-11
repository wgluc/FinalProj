import spotipy
import secrets
import spotipy.util as util

# CACHE_FNAME = 'cached_music.json'
# baseurl = 'https://api.spotify.com'
# util.prompt_for_user_token('hockeybean',scope = '' ,client_id= secrets.client_id,
# client_secret= secrets.client_secret,redirect_uri= secrets.redirect_uri)

token = util.oauth2.SpotifyClientCredentials(client_id= secrets.client_id, client_secret= secrets.client_secret)

cache_token = token.get_access_token()
spotify = spotipy.Spotify(cache_token)

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])



# def get_data_using_cache(baseurl):
#     unique_indent = baseurl
#     if baseurl in CACHE_DICT:
#         return CACHE_DICT[baseurl]
#     else:
#         response = requests.get(baseurl)
#         CACHE_DICT[unique_indent] = response.text
#         fref = open('cached_music.json', 'w')
#         dumped_data = json.dumps(CACHE_DICT)
#         fref.write(dumped_data)
#         fref.close()
#         return CACHE_DICT[unique_indent]
