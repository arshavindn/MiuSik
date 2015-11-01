class Album(object):
    def __init__(self, album, artist, date=None):
        self.__info = {}  # album, artist, date, cover
        self.__info['album'] = album
        self.__info['artist'] = artist
        if date:
            self.__info['date'] = date
        self.__songs = {}  # pairs of song location and Track object

    def __len__(self):
        return len(self.__songs)

    def get_info(self, info):
        return self.__info.get(info)

    def set_date(self, date):
        self.__info['date'] = date

    def add_song(self, trackobj):
        if trackobj:
            self.__songs[trackobj.get_loc()] = trackobj

    def remove_song(self, loc):
        try:
            del self.__songs[loc]
        except KeyError:
            pass
