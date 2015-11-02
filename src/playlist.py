from track import Track
from album import Album


class Playlist():
    def __init__(self, name, saved_plst=None):
        self.name = name
        if saved_plst:
            pass
        self.__songs = {}  # pairs of song location and Track object
        self.__albums = {}  # pairs of (album, artist) tuple and Album object
        self.__total_duration = 0

    def rename(self, name):
        self.name = name

    def add_songs(self, songs):
        """
            songs: list of file path of songs.
        """
        for song in songs:
            if self.__songs.get(song) is None:
                track = Track(song)
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

    def __len__(self):
        """
            Return number of songs in playlist.
        """
        return len(self.__songs)

    def get_total_duration(self):
        return self.__total_duration

    def save_playlist(self, loc):
        pass

    def load_playlist(self, loc):
        pass
