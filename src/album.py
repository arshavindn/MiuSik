class Album(object):
    def __init__(self, album, artist, date=None):
        self.__info = {}  # album, artist, date, cover
        self.__info['album'] = album
        self.__info['artist'] = artist
        if date:
            self.__info['date'] = date
        self.__songs = {}

    def get_info(self, info):
        return self.__info.get(info)

    def set_date(self, date):
        self.__info['date'] = date
