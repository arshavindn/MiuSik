from track import Track
from album import Album
try:
    import cPickle as pickle
except ImportError:
    import pickle


class Playlist():
    def __init__(self, name=None):
        if name:
            self._name = name
        self.__albums = {}  # pairs of (album, albumartist) tuple and Album object
        self.__total_duration = 0
        self.played_songs = []

    def __len__(self):
        """
            Return number of songs in playlist.
        """
        songs_num = 0
        for album in self.get_albums():
            songs_num += len(album)
        return songs_num

    def get_playlist_duration(self):
        return self.__total_duration

    def set_loc(self, loc):
        self._loc = loc
        # self.load_self()

    def get_albums_dict(self):
        return self.__albums

    def get_albums_keys(self):
        return self.__albums.iterkeys()

    def get_album_from_loc(self, loc):
        for album in self.get_albums():
            if album.has_track(loc):
                return album
        return None

    def get_albums(self):
        return self.__albums.itervalues()

    def get_total_duration(self):
        return self.__total_duration

    def rename(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def get_album_from_info(self, album, albumartist):
        return self.__albums.get((album, albumartist))

    def get_loc_list(self):
        """
            Return a list of tracks' location
        """
        loc_list = []
        for album in self.get_albums():
            loc_list.extend(album.get_songs())
        return loc_list

    def add_track(self, loc, trackdb):
        track = trackdb.get_track_by_loc(loc)
        if not track:
            track = Track(loc)
            respone = trackdb.add_track_from_trackobj(track)
            if not respone:
                return False
        tr_album = track.get_tag_raw('album', True)
        tr_albumartist = track.get_tag_raw('albumartist', True)
        if tr_albumartist == u'':
            tr_albumartist = track.get_tag_raw('artist', True)
        album = self.get_album_from_info(tr_album, tr_albumartist)
        if not album:
            # create new album
            album = Album(tr_album, tr_albumartist)
            self.__albums[(tr_album, tr_albumartist)] = album
        album.unchecked_add_song(track)
        self.__total_duration += track.get_tag_raw('__length')

        # cover = coverdb.get_cover(tr_album, tr_albumartist)
        # if not cover:
        #     tr_cover = track.get_tag_disk('cover')
        #     if tr_cover:
        #         coverdb.add_cover(tr_album, tr_albumartist, tr_cover)
        return track

    def remove_track(self, loc, trackdb):
        """
            Remove song from playlist with given location.
        """
        track = trackdb.get_track_by_loc(loc)
        if not track:
            track = Track(loc)
            if not track._scan_valid:
                return False
        tr_album = track.get_tag_raw('album', True)
        tr_albumartist = track.get_tag_raw('albumartist', True)
        if tr_albumartist == u'':
            tr_albumartist = track.get_tag_raw('artist', True)
        album = self.get_album_from_info(tr_album, tr_albumartist)
        if not album:
            return False
        return album.remove_track(loc)

    def save_self(self, loc=None):
        if not loc:
            loc = self._loc
        with open(loc, 'w+b') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def load_data(self, data):
        self._name = data[0]
        self.__albums = data[1]
        self.__total_duration = data[2]
