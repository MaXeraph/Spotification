# import spotipy
# spotify = spotipy.Spotify()
# name = 'Ed Sheeran'
# results = spotify.search(q='artist:' + name, type='artist')
# print(results)

# coding: utf-8
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import credentials

import json
import time

CLIENT_ID = credentials.CLIENT_ID
CLIENT_SECRET = credentials.CLIENT_SECRET
USER = credentials.USER
DISPLAY = credentials.DISPLAY
scope = 'user-modify-playback-state' #https://developer.spotify.com/web-api/using-scopes/

def start_playback(self, device_id = None, context_uri = None, uris = None, offset = None):
    ''' Start or resume user's playback.
        Provide a `context_uri` to start playback or a album,
        artist, or playlist.
        Provide a `uris` list to start playback of one or more
        tracks.
        Provide `offset` as {"position": <int>} or {"uri": "<track uri>"}
        to start playback at a particular offset.
        Parameters:
            - device_id - device target for playback
            - context_uri - spotify context uri to play
            - uris - spotify track uris
            - offset - offset into context by index or track
    '''
    if context_uri is not None and uris is not None:
        self._warn('specify either context uri or uris, not both')
        return
    if uris is not None and not isinstance(uris, list):
        self._warn('uris must be a list')
        return
    data = {}
    if context_uri is not None:
        data['context_uri'] = context_uri
    if uris is not None:
        data['uris'] = uris
    if offset is not None:
        data['offset'] = offset
    return self._put("me/player/play?device_id=ddb1605ef0045a2bde85bb4892a464ffa28e0cb7", payload=data)

def pause_playback(spot, device_id = None):
    ''' Pause user's playback.
        Parameters:
            - device_id - device target for playback
    '''
    return spot._put("me/player/pause?device_id=ddb1605ef0045a2bde85bb4892a464ffa28e0cb7")

###### AUTH
# token = util.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
# cache_token = token.get_access_token()
# spotify = spotipy.Spotify(cache_token) # use for not-so-private data

token = util.prompt_for_user_token(USER,scope,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri='http://localhost/')
spotify = spotipy.Spotify(auth=token)

# Pause playback for 3 seconds then restart
try:
    pause_playback(spotify)
except:
    pass
time.sleep(3)
start_playback(spotify)

###### COLLECTION
