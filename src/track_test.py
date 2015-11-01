from track import Track

def test_track():
	song = Track('I:/Coming_Home.mp3')
	file_size = song.get_file_size()
	print song.list_tags()
	print song.read_tags()


if __name__ == '__main__':
	test_track()