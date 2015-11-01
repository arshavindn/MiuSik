from mp3 import MP3Format
from flac import FlacFormat
from tags import tag_data


def test_tags_pair():
    song1 = FlacFormat('D:/Movies/Christina_Perri-Lovestrong-Deluxe_Edition/02-christina_perri-arms.flac')
    tags = [k for k in tag_data.iterkeys()]
    # lst = song1._get_tag(song1._get_raw(), 'TIT2')
    # print lst
    print tags
    tag_pairs = song1.read_all()
    print tag_pairs


def test_tags_module():
    print tag_data['album']

if __name__ == '__main__':
    test_tags_pair()
