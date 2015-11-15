from playlist import Playlist
from track import Track
import common


class PlaylistManager(object):
    def __init__(self):
    	self.playlists = []
        self.playlist_list = {}
        self.playlist_list_loc = get_appdata_dir() + '/' + 'playlist_list.miu'
        self.load_playlist_list()

    def load_playlist_list(self):
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
            playlist_list.update({p._name: p._loc})
        with open(self.playlist_list_loc, 'wb') as output:
            pickle.dump(playlist_list, output pickle.HIGHEST_PROTOCOL)

    def add_playlist(self, name):
    	playlist = Playlist(name)
        self.playlists.append(playlist)

    def save_playlist(self, pl, loc, overwrite=False):
        """
            Saves a playlist

            @param pl: the playlist
            @param overwrite: Set to [True] if you wish to overwrite a
                playlist should it happen to already exist
        """
        if overwrite or p1 not in self.playlists:
			pl.save_self(loc)
			if not p1 in self.playlists:
				self.playlists.append(p1)
		else:
			raise PlaylistExists

    def remove_playlist(self, playlist):
        """
            Removes a playlist from the manager
        """
        if playlist in self.playlists:
            self.playlists.remove(playlist)

    def remove_playlist_file(self, playlist):
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
        if old_name in self.playlists:
            self.remove_playlist(old_name)
            playlist.rename(new_name)
            self.save_playlist(playlist, playlist._loc)


class PlaylistExists(Exception):
	pass