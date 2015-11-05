from src.album import Album
import shelve
from ast import literal_eval


class AlbumDB():
    def __init__(self, loc):
        self._loc = loc
        self.__albums = {}
        self._added = False
        self._removed = False
        self._unsaved_updated_albums = []
        self.load_db()

    def __len__(self):
        return len(self.__albums)

    def get_keys(self):
        return self.__albums.iterkeys()

    def get_album(self, album, artist):
        return self.__albums.get((album, artist))

    def add_album(self, albumobj):
        album = albumobj.get_info('album')
        if not album:
            album = u'Unknown'
        artist = albumobj.get_info('artist')
        if not artist:
            artist = u'Unknown'
        if not self.get_album(album, artist):
            self.__albums[(album, artist)] = albumobj
            self._added = True

    def remove_album(self, album, artist):
        try:
            if self.get_album(album, artist):
                del self.__albums[(album, artist)]
                self._removed = True
                return True
            else:
                return False
        except KeyError:
            return False

    def add_track_to_album(self, trackobj):
        """
            Add track to album in data,
            if album does not exist, creat new album.
        """
        tr_album = trackobj.get_tag_raw('album', True)
        if not tr_album:
            tr_album = u'Unknown'
        tr_artist = trackobj.get_tag_raw('artist', True)
        if not tr_artist:
            tr_artist = u'Unknown'
        if self.get_album(tr_album, tr_artist):
            self.get_album(tr_album, tr_artist).unchecked_add_song(trackobj)
            if (tr_album, tr_artist) not in self._unsaved_updated_albums:
                self._unsaved_updated_albums.append((tr_album, tr_artist))
        else:
            new_album = Album(tr_album, tr_artist)
            new_album.unchecked_add_song(trackobj)
            self.__albums[(tr_album, tr_artist)] = new_album
            self._added = True

    def remove_track_from_album(self, trackobj):
        tr_album = trackobj.get_tag_raw('album', True)
        if not tr_album:
            tr_album = u'Unknown'
        tr_artist = trackobj.get_tag_raw('artist', True)
        if not tr_artist:
            tr_artist = u'Unknown'
        if self.get_album(tr_album, tr_artist):
            check = self.get_album(tr_album, tr_artist).remove_song(trackobj.get_loc())
            if check and \
                    (tr_album, tr_artist) not in self._unsaved_updated_albums:
                self._unsaved_updated_albums.append((tr_album, tr_artist))
            return check
        else:
            return False

    def load_db(self, loc=None):
        if not loc:
            loc = self._loc

        albumdata = shelve.open(loc, protocol=2)
        # convert key in albumdata from string to tuple
        data_keys = [literal_eval(key.decode('utf-8')) for key in albumdata.iterkeys()]
        diff = set(data_keys) - set(self.__albums)
        for key in diff:
            self.__albums[key] = albumdata[str(key).encode('utf-8')]

        albumdata.close()

    def save_db(self, loc=None):
        if not loc:
            loc = self._loc
        albumdata = shelve.open(loc, protocol=2)  # highest protocol
        data_keys = [literal_eval(key.decode('utf-8')) for key in albumdata.iterkeys()]

        if self._added or len(self.__albums) > len(data_keys):
            diff_added = set(self.__albums) - set(data_keys)
            diff_added.update(self._unsaved_updated_albums)
            for key in diff_added:
                albumdata[str(key).encode('utf-8')] = self.__albums[key]
            self._unsaved_updated_albums = []
            self._added = False

        if self._removed:
            diff_removed = set(data_keys) - set(self.__albums)
            for key in diff_removed:
                del albumdata[str(key).encode('utf-8')]
            self._removed = False

        albumdata.sync()
        albumdata.close()

# end AlbumDB class
