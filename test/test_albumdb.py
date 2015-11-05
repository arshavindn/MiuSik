from src.database.trackdb import TrackDB
from src.database.albumdb import AlbumDB


def test1():
    songs = [u"D:/Drive E/Music/Marry You - Bruno Mars.mp3",
             u"D:/Drive E/Music/The Lazy Song - Bruno Mars.mp3",
             u"D:/Drive E/Music/Bruno Mars - It Will Rain.mp3",
             u"D:/Drive E/Music/Air Supply - All Out Of Love.mp3",
             u"D:/Drive E/Music/David Archuleta - Crush.mp3",
             u"D:/Drive E/Music/Taylor Swift - 22.mp3"]

    albdb = AlbumDB("D:/Cloud/Dropbox/Programming/Code/py/Miusik/test/test_albumdb.db")
    my_trackdb = TrackDB("D:/Cloud/Dropbox/Programming/Code/py/Miusik/test/test_trackdb.db")
    for song in songs:
        my_trackdb.add_song_from_loc(song)
    print my_trackdb.get_songs()
    my_trackdb.save_db()

    for key in my_trackdb.get_keys():
        albdb.add_track_to_album(my_trackdb.get_song_by_loc(key))

    albdb.save_db()

    for key in albdb.get_keys():
        print albdb.get_album(key[0], key[1])
