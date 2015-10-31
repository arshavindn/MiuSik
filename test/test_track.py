from src import track

loc = u"D:/Drive E/Music/Bruno Mars - It Will Rain.mp3"


def test1():
    song1 = track.Track(loc)
    rating = song1.get_tag_raw('__rating')
    print rating
