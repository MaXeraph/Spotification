# import spotipy
# spotify = spotipy.Spotify()
# name = 'Ed Sheeran'
# results = spotify.search(q='artist:' + name, type='artist')
# print(results)

# coding: utf-8
import spotipy
import spotipy.util as util
import json

CLIENT_ID = '0653e348f6134e17afe2533c3307bb48'
CLIENT_SECRET = '147ceb6e7e3b4139aac65bfdebbf9557'
USER = '12180777012'
DISPLAY = 'Max Pham'
scope = 'user-read-playback-state' #https://developer.spotify.com/web-api/using-scopes/

def current_user_playing_track(spot):
        ''' Get information about the current users currently playing track.
        '''
        return spot._get('me/player/currently-playing')

###### AUTH
# token = util.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
# cache_token = token.get_access_token()
# spotify = spotipy.Spotify(cache_token) # use for not-so-private data


token = util.prompt_for_user_token(USER,scope,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri='http://localhost/')
spotify = spotipy.Spotify(auth=token)

###### COLLECTION

### Currently playing title
data = current_user_playing_track(spotify)
parsed = json.dumps(data, indent=2) # read the whole thing
current_title, current_artist = '', ''

try:
    while True:
        data = current_user_playing_track(spotify)
        if current_title != data["item"]['name']:
            current_title = data["item"]['name']
            current_artist = data["item"]["artists"][0]["name"]
            print("Playing: %s | %s" % (current_title, current_artist))
except KeyboardInterrupt:
    pass

### Display playlist - doesnt work
# for i, playlist in enumerate(results1['items']):
#     if playlist['owner']['display_name'] == DISPLAY:
#     #     print(playlist['name'].encode('utf-8'))
#         print("%d %s" %(i, playlist['name'].encode('utf-8', 'replace')))
