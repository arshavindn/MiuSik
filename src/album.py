from track import Track


class Album(object):
    __slots__ = ["__info", "__songs"]

    def __init__(self, album, albumartist, date=None):
        self.__info = {}  # album, artist, date
        self.__info['album'] = album
        self.__info['albumartist'] = albumartist
        if date:
            self.__info['date'] = date
        self.__songs = []

    def __len__(self):
        return len(self.__songs)

    def __str__(self):
        return str(self.__songs)

    def get_info(self, info):
        return self.__info.get(info)

    def get_songs(self):
        return self.__songs

    def set_date(self, date):
        self.__info['date'] = date

    def add_song(self, trackobj):
        if isinstance(trackobj, Track):
            album = trackobj.get_tag_raw('album', True)
            albumartist = trackobj.get_tag_raw('albumartist', True)
            if albumartist == u'':
                albumartist = trackobj.get_tag_raw('artist', True)
            if album == self.get_info('album') and \
                    albumartist == self.get_info('albumartist'):
                self.unchecked_add_song(trackobj)

    def unchecked_add_song(self, trackobj):
        if trackobj.get_loc() not in self.__songs:
            self.__songs.append(trackobj.get_loc())
            date = trackobj.get_tag_raw('date', True)
            if not self.get_info('date') and date != u'':
                self.set_date(date)

    def remove_track(self, loc):
        try:
            self.__songs.remove(loc)
            return True
        except ValueError:
            return False
