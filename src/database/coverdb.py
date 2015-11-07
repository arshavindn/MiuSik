import shelve

class CoverDB():
    def __init__(self, loc):
        self._loc = loc
        self.__covers = {}
        self._added = False
        self._removed = False
        self._unsaved_updated_covers = []
        self.load_db()

    def get_covers_keys(self):
        return self.__covers.iterkeys()

    def add_cover(self, album, albumartist, cover):
        if (album, albumartist) not in self.get_covers_keys():
            self.__covers[(album, albumartist)] = cover
            self._added = True

    def add_cover_from_track(self, trackobj):
        al_ar = trackobj.get_album_n_albumartist()
        cover = trackobj.get_tag_disk('cover')
        if cover:
            self.add_cover(al_ar[0], al_ar[1], cover)

    def remove_cover(self, album, albumartist):
        try:
            del self.__covers((album, albumartist))
            self._removed = True
        except KeyError:
            pass

    def remove_cover_from_track(self, trackobj):
        al_ar = trackobj.get_album_n_albumartist()
        self.remove_cover(al_ar[0], al_ar[1])

    def load_db(self, loc=None):
        if not loc:
            loc = self.loc

        coverdata = shelve.open(loc, protocol=2)
        # convert key in coverdata from string to tuple
        data_keys = [literal_eval(key.decode('utf-8')) for key in coverdata.iterkeys()]
        diff = set(data_keys) - set(self.__covers)
        for key in diff:
            self.__covers[key] = coverdata[str(key).encode('utf-8')]

        coverdata.close()

    def save_db(self, loc=None):
        if not loc:
            loc = self._loc
        coverdata = shelve.open(loc, protocol=2)  # highest protocol
        data_keys = [literal_eval(key.decode('utf-8')) for key in coverdata.iterkeys()]

        if self._added or len(self.__covers) > len(data_keys):
            diff_added = set(self.__covers) - set(data_keys)
            diff_added.update(self._unsaved_updated_covers)
            for key in diff_added:
                coverdata[str(key).encode('utf-8')] = self.__covers[key]
            self._unsaved_updated_albums = []
            self._added = False

        if self._removed:
            diff_removed = set(data_keys) - set(self.__covers)
            for key in diff_removed:
                del coverdata[str(key).encode('utf-8')]
            self._removed = False

        coverdata.sync()
        coverdata.close()
