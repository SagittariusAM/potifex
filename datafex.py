from __future__ import unicode_literals
import json
from requests import get
import yt_dlp
from yt_dlp import YoutubeDL
from yt_dlp.postprocessor.ffmpeg import FFmpegMetadataPP
from bs4 import *
from metadfex import *

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}

class Song:
    def __init__(self, sData, datafex):
        self.id = sData["track"]["id"]
        self.name = sData["track"]["name"]
        self.album = sData["track"]["album"]["name"]
        self.artist = getArtist(sData)
        self.albumartist = datafex["name"]
        self.track = sData["track"]["track_number"]
        self.imageURL = sData["track"]["album"]["images"][0]["url"]

with open("data\DownloadedList.json", "r") as b:
    DownloadedList = json.load(b)

def getFromSpotify(headers, playlistID):
    pageURL = f"https://api.spotify.com/v1/playlists/{playlistID}"
    while pageURL:
        pageRes = requests.get(url=pageURL, headers=headers).json()
        try:
            for item in pageRes.json()["items"]:
                (pageRes["tracks"]["items"]).append(item)
            pageURL = pageRes.json()["next"]
        except:
            pageURL = pageRes.json()["tracks"]["next"]
    # upData = json.dumps(mainData, indent=2)
    return pageRes

# Main function: Gets each song and assigns its attributes.
def getFromYouTube(thestuff, datafex):
    for dictn in datafex["tracks"]["items"]:
        song = Song(dictn, datafex)
        fullTitle = f"{song.name} - {song.artist}"
        if all(fullTitle != track for track in DownloadedList): # Checks for if already exists.
            print(f"Name: {song.name}\nAlbum: {song.album}\nArtist: {song.artist}")
            executeS(song)
            listingS(fullTitle)
        else:
            pass

# Organizing function.
def executeS(song):
    outS = (song.name).replace("\"", "").replace("?", "").replace("|", "").replace("/", "")
    idSong = search(f"{song.name} {song.artist}")
    downloadS(idSong, outS)
    metadata(song, outS)
    moveSong(outS)

# Search function from YoutubeDL.
def search(arg):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            get(arg) 
        except:
            video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        else:
            video = ydl.extract_info(arg, download=False)
    idSong = video["id"]
    tiSong = video["title"]
    print(f"Downloading: {tiSong}")
    return idSong

# Download from YouTube.
def downloadS(id, outS):
    boop = outS + '.%(ext)s'
    ydl_opts = {
        'format': 'bestaudio/best',
        'quality': '0',
        'outtmpl': boop,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={id}"])
        print(ydl)

# Add to a downloaded songs list.
def listingS(fullTitle):
    DownloadedList.append(fullTitle)
    upData = json.dumps(DownloadedList, indent=2)
    with open("DownloadedList.json", "w") as b:
        b.write(upData)

def countPages(headers, pageURL):
    tracks = 0
    while pageURL:
        pageRes = requests.get(url=pageURL, headers=headers).json()
        try:
            for item in pageRes.json()["items"]: tracks += 1
            pageURL = pageRes.json()["next"]
        except:
            for item in pageRes.json()["tracks"]["items"]: tracks += 1
            pageURL = pageRes.json()["tracks"]["next"]
    return tracks

def addToHistory(playlistid, playlist_name, history_doc):
    try: del history_doc[playlistid]
    except KeyError: pass
    finally: 
        history_doc[playlistid] = playlist_name
        history = json.dumps(history_doc, indent=2)
        with open("data\history.json", "w") as h:
            h.write(history)
