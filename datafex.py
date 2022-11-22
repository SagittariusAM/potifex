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

with open("DownloadedList.json", "r") as b:
    DownloadedList = json.load(b)

# Main function: Gets each song and assigns its attributes.
def getS(thestuff):
    with open(f'{thestuff}.json', 'r') as f:
        datafex = json.load(f)
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

getS("01PstILJGu2ygcj0y2bkGE")