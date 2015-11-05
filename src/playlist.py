from track import Track, datetime_format
from album import Album
from datetime import datetime
import os


class Playlist():
    def __init__(self, name, saved_plst=None):
        self.name = name
        if saved_plst:
            pass
        self.__songs = {}  # pairs of song location and Track object
        self.__albums = {}  # pairs of (album, artist) tuple and Album object
        self.__total_duration = 0
        self.__create_plst_dir()

    def rename(self, name):
        home_dir = os.path.expanduser('~')
        app_dir = home_dir + '/Miusik'
        os.rename(app_dir + '/' + self.name, app_dir + '/' + name)
        self.name = name

    def get_plst_dir(self):
        pass

    def add_song(self, song):
        """
            song: file path of song.
        """
        if self.__songs.get(song) is None:
            track = Track(song)
            if track._scan_valid:
                date_added = unicode(datetime.now().strftime(datetime_format))
                track.set_tag_raw('__date_added', date_added)
                self.__songs[song] = track
                self.__total_duration += track.get_tag_raw('__length')
                track_album = track.get_tag_raw('album')
                track_artist = track.get_tag_raw('artist')
                # add song to album
                if self.__albums.get((track_album, track_artist)) is None:  # if album does not exist in self.__albums
                    album = Album(track_album, track_artist)
                    album.add_song(track)
                    self.__albums[(track_album, track_artist)] = album
                else:
                    self.__albums[(track_album, track_artist).add_song(track)]
                return track
            else:
                return False
        else:
            return False

    def remove_song(self, loc):
        """
            Remove song from playlist with given location.
        """
        track = self.__songs.get(loc)
        if track:
            self.__total_duration -= track.get_tag_raw('__length')
            track_album = track.get_tag_raw('album')
            track_artist = track.get_tag_raw('artist')
            del self.__songs[loc]
            self.__albums[(track_album, track_artist)].remove_song(loc)
            if len(self.__albums[(track_album, track_artist)]) == 0:
                del self.__albums[(track_album, track_artist)]

    def get_track(self, loc):
        """
            Return track object of given location.
            If not found, return None.
        """
        return self.__songs.get(loc)

    def __len__(self):
        """
            Return number of songs in playlist.
        """
        return len(self.__songs)

    def get_total_duration(self):
        return self.__total_duration

    def __create_plst_dir(self):
        home_dir = os.path.expanduser('~')
        app_dir = home_dir + '/Miusik'
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)
        if not os.path.exists(app_dir + '/' + self.name):
            os.makedirs(app_dir + '/' + self.name)

    def save_playlist(self, loc):
        pass

    def load_playlist(self, loc):
        pass
