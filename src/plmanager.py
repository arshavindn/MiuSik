from playlist import Playlist
from track import Track
import common


class PlaylistManager(object):
    def __init__(self):
    	self.playlists = []
        self.previous_session_playlist = {}
        self.session_data_loc = get_appdata_dir() + '/' + 'session.miu'
        self.load_session()

    def load_session(self):
        # load playlists's name & loc of previous session from file
        with open(self.session_data_loc, 'rb') as input:
            self.previous_session_playlist = pickle.load(input)
        # load playlist objects to memory
        for loc in self.previous_session_playlist.itervalues():
            with open(loc, 'rb') as input:
                playlist_object = pickle.load(input)
                self.playlists.append(playlist_object)

    def save_session(self):
        # save playlists's name & loc of current session to file
        current_session_playlist = {}
        for p in self.playlists:
            current_session_playlist.update({p._name: p._loc})
        with open(self.session_data_loc, 'wb') as output:
            pickle.dump(current_session_playlist, output pickle.HIGHEST_PROTOCOL)

    def add_playlist(self, name):
    	pass

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
            Removes a playlist from the manager, also
            physically deletes its
        """
        if playlist in self.playlists:
            # try:
            #     os.remove(playlist._loc)
            # except OSError:
            #     pass
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