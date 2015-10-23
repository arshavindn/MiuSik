from playlist import Playlist
from track import Track


class PlaylistManager(object):
    def __init__(self):
        self.playlists = []
        self.temp_playlists = []
        self.temp_songs = []
        self.current_playlist = None
        self.current_song = None
        self.repeat_modes = ['Off', 'Track', 'Album', 'Playlist']
        self.repeat = 'Off'
        self.shuffle = False

    def next_song(self):
        if self.current_song:
            self.temp_songs.append(self.current_song)
            if len(self.temp_songs) > 10:
                self.temp_songs.pop(0)
            if self.repeat == 'Track':
                return self.current_song
            elif:
