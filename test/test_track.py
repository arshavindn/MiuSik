from src import track

loc = u"D:/Drive E/Music/Bruno Mars - It Will Rain.mp3"


def test1():
    song1 = track.Track(loc)
    song1.set_tags()
    print song1
