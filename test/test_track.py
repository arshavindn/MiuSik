# -*- coding: utf-8 -*-

from src import track
import os

loc1 = u"D:/Drive E/Music/Bruno Mars - It Will Rain.mp3"
loc2 = u'D:/Drive E/Music/TV In Black White - Lana Del Rey.mp3'
folder = u"D:/Drive E/Vietnam"
songs = [folder + '/' + song for song in os.listdir(folder)]
loc3 = songs[7]

print len(loc3)

def test1():
    song2 = track.Track(loc3)
    # rating = song1.get_tag_raw('__rating')
    # print rating
    print song2._scan_valid
    a = song2.get_tag_raw('artist')
    print a
    # print song2.get_tag_disk('cover')
    # print type(a)
    # print song1.get_cover()
    # print song1
