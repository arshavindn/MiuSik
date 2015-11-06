from track import Track


class Album(object):
    __slots__ = ["__info", "__songs"]

    def __init__(self, album, artist, date=None):
        self.__info = {}  # album, artist, date
        self.__info['album'] = album
        self.__info['artist'] = artist
        if date:
            self.__info['date'] = date
        self.__songs = []

    def __len__(self):
        return len(self.__songs)

    def __str__(self):
        return str(self.__songs)

    def get_info(self, info):
        return self.__info.get(info)

    def set_date(self, date):
        self.__info['date'] = date

    def add_song(self, trackobj):
        if isinstance(trackobj, Track):
            if trackobj.get_tag_raw('album') == self.__info['album'] and \
                    trackobj.get_tag_raw('album') == self.__info['artist']:
                self.unchecked_add_song(trackobj)
                return True
            else:
                return False
        else:
            return False

    def unchecked_add_song(self, trackobj):
        if trackobj.get_loc() not in self.__songs:
            self.__songs.append(trackobj.get_loc())

            if not self.__info.get('cover'):
                cover = trackobj.get_tag_disk('cover')
                if not cover:
                    cover = trackobj.get_tag_disk('coverart')

                if cover:
                    self.__info['cover'] = cover

    def remove_song(self, loc):
        try:
            self.__songs.remove(loc)
            return True
        except ValueError:
            return False
