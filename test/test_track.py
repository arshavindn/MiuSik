# -*- coding: utf-8 -*-

from src import track
import os

loc0 = u"D:/Drive E/Music/Escape (The Piña Colada Song) - Rupert Holmes.mp3"
loc1 = u"D:/Drive E/Music/Bruno Mars - It Will Rain.mp3"
loc2 = u'D:/Drive E/Music/TV In Black White - Lana Del Rey.mp3'
folder = u"D:/Drive E/Vietnam"
songs = [folder + '/' + song for song in os.listdir(folder)]
loc3 = songs[7]

print len(loc3)


def test1():
    song = track.Track(loc0)
    # rating = song1.get_tag_raw('__rating')
    # print rating
    print song._scan_valid
    a = song.get_tag_disk('albumartist')
    print a
    # print song.get_tag_disk('cover')
    # print type(a)
    # print song1.get_cover()
    # print song1
