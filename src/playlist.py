from track import Track


class Playlist():
    def __init__(self, name=None):
        if name:
            self.name = name
        self.__songs = {}

    def set_name(self, name):
        self.name = name

    def add_songs(self, songs):
        """
            songs: list of file path of songs.
        """
        for song in songs:
            if self.__songs.get(song) is None:
                self.__songs[song] = Track(song)
                self.__songs[song].set_tags()

    def remove_song(self, song):
        """
            Remove song from playlist with given file path of song.
        """
        try:
            del self.__songs[song]
        except KeyError:
            pass

    def __len__(self):
        """
            Return number of songs in playlist.
        """
        return len(self.__songs)
