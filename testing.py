# coding: utf-8

import json
import requests
import webbrowser
import base64
import six

CLIENT_ID = '0653e348f6134e17afe2533c3307bb48'
CLIENT_SECRET = '147ceb6e7e3b4139aac65bfdebbf9557'
USER = '12180777012'
DISPLAY = 'Max Pham'
scopes = 'user-read-playback-state' #https://developer.spotify.com/web-api/using-scopes/

###### AUTH
def _make_authorization_headers(client_id, client_secret):
    auth_header = base64.b64encode(six.text_type(client_id + ':' + client_secret).encode('ascii'))
    return auth_header.decode('ascii')

def request_auth(client, scope):
    r = requests.get('https://accounts.spotify.com/authorize', params={'client_id': CLIENT_ID,
                                                                    'response_type': 'code',
                                                                    'redirect_uri': 'http://localhost/',
                                                                    'scope': scopes})
    webbrowser.open(r.url)
    authCode = input('Put in the returned URL: ')
    if authCode.find('code=') != -1:
        print('ACCESS GRANTED !!!!!')
        return authCode[authCode.find('code=') + 5:]
    else:
        print('ACCESS DENIED')

def request_refresh_for_tokens(authy):
    
    payload = {'Authorization': 'Basic %s' % (_make_authorization_headers(CLIENT_ID,CLIENT_SECRET)),
                'grant_type': 'authorization_code',
                'code': authy,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'redirect_uri': 'http://localhost/'}

    r = requests.post('https://accounts.spotify.com/api/token', data=payload)
    print(headers)

if __name__ == '__main__':
    auth = request_auth(CLIENT_ID, scopes)
    request_refresh_for_tokens(auth)
