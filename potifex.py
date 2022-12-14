from bs4 import *
import base64
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

headers = {
    "Authorization": "Bearer " + token
}

print("You can type PATH to change download folder.")
while True:
    with open("data\History.json", "r") as h:
        history = json.load(h)
    print("Recently Played:")
    no = 0
    recent_searches = [0]
    reversed_history = dict(reversed(list(history.items())))
    for pid in reversed_history:
        no += 1
        name = reversed_history[pid]
        pageURL = f"https://api.spotify.com/v1/playlists/{pid}"
        no_of_songs = countPages(headers, pageURL)
        songs_added = no_of_songs - len(DownloadedList[pid])
        print(f"  {no}- {pid}: {name}, {no_of_songs} Songs (+{songs_added} Added)")
        recent_searches.append(pid)
        if len(recent_searches) >= 6: break

    playlistID = input("Input Playlist ID or choose from Recents:-")

    if playlistID.upper() == "PATH": PATH = input("Set a new download directory:-")
    else: pass

    try: playlistID = int(playlistID)

    except: pass

    else: playlistID = recent_searches[playlistID]

    finally: 
        playlist_data = getFromSpotify(headers, playlistID)
        addToHistory(playlistID, playlist_data["name"], history)
        getFromYouTube(playlistID, playlist_data)
    # except Exception as err: print("\u001b[")
