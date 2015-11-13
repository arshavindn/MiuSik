from playlist import Playlist
from track import Track


class PlaylistManager(object):
    def __init__(self):
    	self.playlists = []

    def save_playlist(self, pl, loc, overwrite=False):
        """
            Saves a playlist

            @param pl: the playlist
            @param overwrite: Set to [True] if you wish to overwrite a
                playlist should it happen to already exist
        """
        name = pl._name
        if overwrite or name not in self.playlists:
			pl.save_self(loc)
			if not name in self.playlists:
				self.playlists.append(name)
		else:
			raise PlaylistExists

    def remove_playlist(self, playlist):
        """
            Removes a playlist from the manager, also
            physically deletes its
        """
        name = playlist._name
        if name in self.playlists:
            try:
                os.remove(playlist._loc)
            except OSError:
                pass
            self.playlists.remove(name)

    def rename_playlist(self, playlist, new_name):
        """
            Renames the playlist to new_name
        """
        old_name = playlist._name
        if old_name in self.playlists:
            self.remove_playlist(old_name)
            playlist.name = new_name
            self.save_playlist(playlist)


class PlaylistExists(Exception):
	pass