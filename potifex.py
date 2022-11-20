import os
import requests
from bs4 import *
import base64
import json
# from datafex import *

url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}

clientID = '571af78e9c2444f89ce35ddb3527a970'
clientSecret = '288133efbc3741e39834fa46844d0de4'
aaaokay = f"{clientID}:{clientSecret}"
msgBytes = aaaokay.encode('ascii')
msgBytes64 = base64.b64encode(msgBytes)
msg64 = msgBytes64.decode('ascii')

headers['Authorization'] = f"Basic {msg64}"
data['grant_type'] = "client_credentials"

r = requests.post(url, headers=headers, data=data)

token = r.json()['access_token']

playlistID = input("Input Playlist ID:-")
playlistURL = f"https://api.spotify.com/v1/playlists/{playlistID}"

headers = {
    "Authorization": "Bearer " + token
}

r = requests.get(url=playlistURL, headers=headers)

thestuff = json.dumps(r.json(), indent=2)
f = open(f"thestuff.json", "w")
f.write(thestuff)

# getS(thestuff)
