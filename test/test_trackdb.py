from src.database.trackdb import TrackDB


def test1():
    songs = [u"D:/Drive E/Music/Bruno Mars - It Will Rain.mp3",
             u"D:/Drive E/Music/Air Supply - All Out Of Love.mp3",
             u"D:/Drive E/Music/David Archuleta - Crush.mp3",
             u"D:/Drive E/Music/Taylor Swift - 22.mp3"]

    my_trackdb = TrackDB("D:/Cloud/Dropbox/Programming/Code/py/Miusik/test/test_trackdb.db")
    for song in songs:
        my_trackdb.add_song_from_loc(song)
    print my_trackdb.get_songs()
    my_trackdb.save_db()
