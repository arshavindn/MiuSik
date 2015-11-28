from playlist import Playlist
from common import *
try:
    import cPickle as pickle
except ImportError:
    import pickle


class PlaylistManager(object):

    def __init__(self, loc=None):
        self.playlists = []
        self.removed_playlists = []
        # current_playlist is a playlist that has a track is playing,
        # if no track is playling, current playlist
        # will be current tab (that contains a playlist).
        # TODO: so, how to set current_playlist satifying this condition.
        self.current_playlist = -1
        self.played_song = []
        self.current_song = None
        if loc:
            self._loc = loc
            self.load_playlist_list()

    def __len__(self):
        return len()

    def set_cur_pl(self, index):
        self.current_playlist = index

    def get_playlist(self, index):
        try:
            return self.playlists[index]
        except IndexError:
            pass

    def get_playlist_names(self):
        """
            Return a list of names of playlists.
        """
        result = []
        for playlist in self.playlists:
            result.append(playlist.get_name())
        return result

    def choose_next_song(self, track_list, shuffle):
        """
            Chosse next song for playing.
        """
        # We have para track list because when shuffle, repeat change,
        # the playing list is being play will change or when user sorts the playlist table.
        pass

    def load_playlist_list(self):
        if os.path.isfile(self.playlist_list_loc):
            # load playlists's name & loc from file
            with open(self.playlist_list_loc, 'rb') as input:
                self.playlist_list = pickle.load(input)
            # load playlist objects to memory
            for loc in self.playlist_list.itervalues():
                with open(loc, 'rb') as input:
                    playlist_object = pickle.load(input)
                    self.playlists.append(playlist_object)

    def save_playlist_list(self):
        # save playlists's name & loc to file
        playlist_list = {}
        for p in self.playlists:
            p.save_self()
            playlist_list.update({p._name: p._loc})
        with open(self.playlist_list_loc, 'wb') as output:
            pickle.dump(playlist_list, output, pickle.HIGHEST_PROTOCOL)

    def add_new_playlist(self, loc=None):
        """
            Add a new playlist with default name and default location.
        """
        name = "Playlist " + str(len(self.get_playlist_names())+1)
        playlist = Playlist(name)
        if loc:
            playlist.set(loc)
            playlist.load_self()
        self.playlists.append(playlist)
        return playlist

    def remove_playlist(self, index):
        self.removed_playlists.append(self.playlists.pop(index))

    def reindex_list(self, des, tar):
        tar_obj = self.playlists.pop(tar)
        self.playlists.insert(des, tar_obj)


class PlaylistExists(Exception):
    pass
