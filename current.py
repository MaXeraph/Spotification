# coding: utf-8

import spotipy
import spotipy.util as util
import json
import pync
import os
import requests

CLIENT_ID = '0653e348f6134e17afe2533c3307bb48'
CLIENT_SECRET = '147ceb6e7e3b4139aac65bfdebbf9557'
USER = '12180777012'
DISPLAY = 'Max Pham'
scope = 'user-read-playback-state' #https://developer.spotify.com/web-api/using-scopes/

def notify(device: str, title: str, artist: str):
    pync.notify("Playing: %s by %s | %s" % (title, artist, device),
                 title='Spotify',
                 activate='com.spotify.client',
                 group=os.getpid(),
                 appIcon='https://i.imgur.com/zmKJPEk.png')

def current_user_playing_track(spot):
        ''' Get information about the current users currently playing track.
        '''
        return spot._get('me/player/currently-playing')

def current_user_playing(spot):
        ''' Get information about the current users currently playing.
        '''
        return spot._get('me/player')


###### AUTH
# token = util.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
# cache_token = token.get_access_token()
# spotify = spotipy.Spotify(cache_token) # use for not-so-private data

token = util.prompt_for_user_token(USER,
                                    scope,
                                    client_id=CLIENT_ID,
                                    client_secret=CLIENT_SECRET,
                                    redirect_uri='http://localhost/')

refresh = requests.post('https://accounts.spotify.com/api/token',
                        data={'grant_type': 'authorization_code',
                                'code': token,
                                'redirect_uri': 'http://localhost/'})
spotify = spotipy.Spotify(auth=token)

###### COLLECTION

### Currently playing title
data, current_player  = current_user_playing_track(spotify), current_user_playing(spotify)
parsed = json.dumps(data, indent=2) # read the whole thing
# print(parsed)

current_title, current_artist, current_device = '', '', ''

try:
    while True:
        data, current_player  = current_user_playing_track(spotify), current_user_playing(spotify)

        if current_title != data["item"]['name'] or current_device != current_player['device']['name']:
            current_device = current_player['device']['name']
            current_title = data["item"]['name']
            current_artist = data["item"]["artists"][0]["name"]

            notify(current_device, current_title, current_artist)
except KeyboardInterrupt:
    pass
