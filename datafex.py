from __future__ import unicode_literals
import os
import json
from requests import get
import youtube_dl
from youtube_dl import YoutubeDL
from bs4 import *

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

def downloadS(id):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={id}"])

def getS(thestuff):
    with open(f'{thestuff}.json', 'r') as f:
        datafex = json.load(f)

    for dictn in datafex["tracks"]["items"]:
        song = Song(dictn)
        # name = (song.name).replace(" ", "+").replace("&", "%26").replace(":", "%3A")
        # print(f"https://www.youtube.com/results?search_query={name}")
        m = search(song.name)
        idSong = m["id"]
        title = m["title"]
        input(f"Proceed to download ? {title}")
        downloadS(idSong)

class Song:
    def __init__(self, name):
        self.__dict__ = name["track"]
