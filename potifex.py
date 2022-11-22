import requests
from bs4 import *
import base64
import json
from datafex import *

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

playlistID = "01PstILJGu2ygcj0y2bkGE" #input("Input Playlist ID:-")
playlistURL = f"https://api.spotify.com/v1/playlists/{playlistID}"

headers = {
    "Authorization": "Bearer " + token
}

mainData = requests.get(url=playlistURL, headers=headers).json()
pageURL = mainData["tracks"]["next"]

while pageURL:
    print("Paged well")
    pageRes = requests.get(url=pageURL, headers=headers)
    for item in pageRes.json()["items"]: (mainData["tracks"]["items"]).append(item)
    upData = json.dumps(mainData, indent=2)
    with open(f"{playlistID}.json", "w") as b:
        b.write(upData)
    pageURL = pageRes.json()["next"]

getS(playlistID)
