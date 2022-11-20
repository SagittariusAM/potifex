from __future__ import unicode_literals
import os
import json
from requests import get
import yt_dlp
from yt_dlp import YoutubeDL
from yt_dlp.postprocessor.ffmpeg import FFmpegMetadataPP
from bs4 import *
from metadfex import *

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}

def search(arg):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            get(arg) 
        except:
            video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        else:
            video = ydl.extract_info(arg, download=False)

    return video

def downloadS(id, song):
    outS = song.name + '.%(ext)s'
    ydl_opts = {
        'format': 'bestaudio/best',
        'quality': '0',
        'outtmpl': outS,
        # C:/Users/lenovo/Music/iTunes/iTunes Media/Automatically Add to iTunes/
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={id}"])
        

def getS(thestuff):
    with open(f'{thestuff}.json', 'r') as f:
        datafex = json.load(f)
    for dictn in datafex["tracks"]["items"]:
        try:
            a2 = dictn["track"]["artists"][1]["name"]
            a1 = dictn["track"]["artists"][0]["name"]
            artists = f"{a1} & {a2}"
        except: 
            artists = dictn["track"]["artists"][0]["name"]
        song = Song(dictn, artists, datafex)
        print(f"Name: {song.name}\nAlbum: {song.album}\nArtist: {song.artist}")
        # name = (song.name).replace(" ", "+").replace("&", "%26").replace(":", "%3A")
        # print(f"https://www.youtube.com/results?search_query={name}")
        m = search(song.name)
        idSong = m["id"]
        title = m["title"]
        # input(f"Proceed to download ? {title}")
        downloadS(idSong, song)
        metadata(song)
        moveSong(song)

class Song:
    def __init__(self, sData, sArtists, datafex):
        self.id = sData["track"]["id"]
        self.name = sData["track"]["name"]
        self.album = sData["track"]["album"]["name"]
        self.artist = sArtists
        self.albumartist = datafex["name"]
        self.track = sData["track"]["track_number"]
        self.imageURL = sData["track"]["album"]["images"][0]["url"]


getS("thestuff")
