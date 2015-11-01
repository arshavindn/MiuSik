from track import Track
from album import Album


class Playlist():
    def __init__(self, name=None):
        if name:
            self.name = name
        self.__songs = {}  # pairs of song location and Track object
        self.__albums = {}  # pairs of album, artist tuple and Album object
        self.__total_duration = 0

    def set_name(self, name):
        self.name = name

    def add_songs(self, songs):
        """
            songs: list of file path of songs.
        """
        for song in songs:
            if self.__songs.get(song) is None:
                self.__songs[song] = Track(song)

                self.__total_duration += self.__songs[song]['__length']

    def remove_song(self, song):
        """
            Remove song from playlist with given file path of song.
        """
        try:
            self.__total_duration -= self.__songs[song]['__length']
            del self.__songs[song]
        except KeyError:
            pass

    def __len__(self):
        """
            Return number of songs in playlist.
        """
        return len(self.__songs)

    def get_total_duration(self):
        return self.__total_duration
