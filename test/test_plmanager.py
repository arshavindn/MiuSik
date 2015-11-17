from src import playlist
from src import plmanager
import os

def test1():
	my_playlist_manager = plmanager.PlaylistManager()
	# test add playlist
	print "* Test add playlist"
	my_playlist_manager.add_playlist('Playlist1', 'I:/Playlist1.pl')
	my_playlist_manager.add_playlist('Playlist2', 'I:/Playlist2.pl')
	for p in my_playlist_manager.playlists:
		print p._name
	# test delete playlist
	print "* Test delete playlist"
	for p in my_playlist_manager.playlists:
		if p._name == 'Playlist2':
			my_playlist_manager.remove_playlist(p)
	for p in my_playlist_manager.playlists:
		print p._name
	# test save playlist list
	print "* Test save playlist list"
	my_playlist_manager.save_playlist_list()
	print os.listdir('I:/')
	# test rename playlist
	print "* Test rename playlist"
	for p in my_playlist_manager.playlists:
		if p._name == 'Playlist1':
			my_playlist_manager.rename_playlist(p, 'Playlist1_renamed')
	for p in my_playlist_manager.playlists:
		print p._name
	# test add playlist from location
	print "* Test add playlist from location"
	my_playlist_manager.add_playlist_from_location('I:/Playlist3.pl')
	for p in my_playlist_manager.playlists:
		print p._name