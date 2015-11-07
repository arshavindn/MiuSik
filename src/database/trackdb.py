from src.track import Track, datetime_format
from datetime import datetime
import shelve


class TrackDB():
    def __init__(self, loc):
        self._loc = loc
        self.__songs = {}
        self.load_db()
        self._added = False  # True if any song added
        self._removed = False  # True if any song removed
        self._unsaved_updated_songs = []  # List of locs of undated songs were not saved to database on disk

    def __len__(self):
        return len(self.__songs)

    def get_songs(self):
        return self.__songs

    def get_keys(self):
        return self.__songs.iterkeys()

    def add_track_from_loc(self, loc):
        if loc not in self.get_keys():
            track = Track(loc)
            self.add_track_from_trackobj(track)
        else:
            return False

    def add_track_from_trackobj(self, trackobj):
        if not trackobj._scan_valid:
            return False
        if trackobj.get_loc() not in self.get_keys():
            if not trackobj.get_tag_raw('__date_added'):
                date_added = unicode(datetime.now().strftime(datetime_format))
                trackobj.set_tag_raw('__date_added', date_added)
            self.__songs[trackobj.get_loc()] = trackobj
            self._added = True
            return trackobj
        else:
            return False

    def add_updated_songs(self, locs):
        for loc in locs:
            if loc not in self._unsaved_updated_songs:
                self._unsaved_updated_songs.append(loc)

    def remove_song(self, loc):
        try:
            del self.__songs[loc]
            self._removed = True
            return True
        except KeyError:
            return False

    def get_track_by_loc(self, loc):
        return self.__songs.get(loc)

    def load_db(self, loc=None, merge=True):
        """
            Load track data from disk.
        """
        if not loc:
            loc = self._loc

        trackdata = shelve.open(loc, protocol=2)  # highest protocol
        trackdata_keys = [key.decode('utf-8') for key in trackdata.iterkeys()]
        if merge:
            diff = set(trackdata_keys) - set(self.__songs)
        else:
            self.__songs = {}
            diff = set(trackdata_keys)
        for key in diff:
            if isinstance(trackdata[key.encode('utf-8')], Track):
                self.__songs[key] = trackdata[key.encode('utf-8')]

        trackdata.close()

    def save_db(self, loc=None):
        """
            Save tracks to database on disk.
        """
        if not loc:
            loc = self._loc

        trackdata = shelve.open(loc, protocol=2)  # highest protocol
        trackdata_keys = [key.decode('utf-8') for key in trackdata.iterkeys()]

        if self._added or len(self.__songs) > len(trackdata_keys):
            diff_added = set(self.__songs) - set(trackdata_keys)
            diff_added.update(self._unsaved_updated_songs)
            for key in diff_added:
                trackdata[key.encode('utf-8')] = self.__songs[key]  # save track object to database
            self._unsaved_updated_songs = []
            self._added = False

        if self._removed:
            diff_removed = set(trackdata_keys) - set(self.__songs)
            for key in diff_removed:
                del trackdata[key.encode('utf-8')]
            self._removed = False

        trackdata.sync()
        trackdata.close()

# end class TrackDB
