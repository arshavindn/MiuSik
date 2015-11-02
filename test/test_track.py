from src import track

loc1 = u"D:/Drive E/Music/Bruno Mars - It Will Rain.mp3"


def test1():
    song1 = track.Track(loc1)
    # rating = song1.get_tag_raw('__rating')
    # print rating
    song1.set_tags()
    print song1.get_tag_raw('__length')
    print song1
