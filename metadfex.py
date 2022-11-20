import os
import shutil
from bs4 import *
import requests
from lyricsgenius import Genius
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TS2, APIC, USLT, TALB, TRCK, TPE2, TS2


def switchToALAC(name):
    os.system("ffmpeg -i %s.m4a-c:a alac %s.alac" %(name, name))

def urlit(ut):
    return (ut).replace(" ", "+").replace("&", "%26").replace(":", "%3A")

def getLyrics(song):
    genius = Genius("Gx0pG5ohW_o_gENp8RGDtXD-k0cSxT1yDI8yPUJtscamGsNR1BRUzQN_ZnavcNdi")
    try:
        print(f"Actually searching for {song.name}")
        songL = genius.search_song(song.name, song.artist)
    except:
        songL = genius.search_song(song.name)
    return songL.lyrics

def metadata(song):
    print("metadata-ing...")
    recentSong = MP3(f"{song.name}.mp3", ID3=ID3)
    r = requests.get(song.imageURL).content
    with open('image.jpg', 'wb') as image:
        image.write(r)
    image = open('image.jpg', 'rb').read()
    recentSong.tags.add(APIC(3, 'image/jpg', 3, 'Album Cover', image))
    recentSong.tags.add(TIT2(text=song.name))
    recentSong.tags.add(TPE2(text=song.albumartist))
    recentSong.tags.add(TS2(text=song.albumartist))
    recentSong.tags.add(TPE1(text=song.artist))
    recentSong.tags.add(TALB(text=song.album))
    recentSong.tags.add(TRCK(text=str(song.track)))
    try: recentSong.tags.add(USLT(lang='eng', desc='desc', text=getLyrics(song)))
    except: print("NO LYRICS FOUND")

    recentSong.save()

def moveSong(song):
    shutil.move(f'{song.name}.mp3', f'C:/Users/lenovo/Music/iTunes/iTunes Media/Automatically Add to iTunes/{song.name}.mp3')
    print("Moved to iTunes")
