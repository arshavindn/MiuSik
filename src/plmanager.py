from playlist import Playlist
from track import Track
from common import *
try:
    import cPickle as pickle
except ImportError:
    import pickle


class PlaylistManager(object):
    def __init__(self):
    	self.playlists = []
        self.playlist_list = {}
        self.playlist_list_loc = get_appdata_dir() + '/' + 'playlist_list.miu'
        self.load_playlist_list()

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

    def add_playlist(self, name, loc):
        if not os.path.isfile(loc) and name not in [p._name for p in self.playlists]:
            playlist = Playlist(name)
            playlist.set_loc(loc)
            self.playlists.append(playlist)
        else:
            raise PlaylistExists

    def add_playlist_from_location(self, loc):
        if os.path.isfile(loc):
            playlist = pickle.load(open(loc, 'rb'))
            self.playlists.append(playlist)

    def save_playlist(self, pl, loc=None, overwrite=False):
        """
            Saves a playlist

            @param pl: the playlist
            @param overwrite: Set to [True] if you wish to overwrite a
                playlist should it happen to already exist
        """
        if overwrite or pl._name not in [p._name for p in self.playlists]:
			pl.save_self(loc)
			if not pl in [p._name for p in self.playlists]:
				self.playlists.append(pl)

        else:
        	raise PlaylistExists

    def remove_playlist(self, playlist):
        """
            Removes a playlist from the manager
        """
        if playlist in self.playlists:
            self.playlists.remove(playlist)

    def remove_playlist_with_file(self, playlist):
        """
            Removes a playlist from the manager, also
            physically deletes its
        """
        if playlist in self.playlists:
            try:
                os.remove(playlist._loc)
            except OSError:
                pass
            self.playlists.remove(playlist)

    def rename_playlist(self, playlist, new_name):
        """
            Renames the playlist to new_name
        """
        old_name = playlist._name
        if old_name in [p._name for p in self.playlists]:
            self.remove_playlist_with_file(playlist)
            playlist.rename(new_name)
            self.save_playlist(playlist, playlist._loc)


class PlaylistExists(Exception):
	pass