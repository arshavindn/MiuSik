from mp3 import MP3Format

song1 = MP3Format('D:/Drive E/Music/Bruno Mars - It Will Rain.mp3')
tags = [k for k in song1.tag_mapping.iterkeys()]
# lst = song1._get_tag(song1._get_raw(), 'TIT2')
# print lst
# print tags
tag_pairs = song1.read_all()
print tag_pairs
