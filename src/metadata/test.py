from mp3 import MP3Format
from tags import tag_data


def test_tags_pair():
    song1 = MP3Format('D:/Drive E/Music/Bruno Mars - It Will Rain.mp3')
    tags = [k for k in song1.tag_mapping.iterkeys()]
    # lst = song1._get_tag(song1._get_raw(), 'TIT2')
    # print lst
    # print tags
    tag_pairs = song1.read_all()
    print tag_pairs


def test_tags_module():
    print tag_data['album']

if __name__ == '__main__':
    test_tags_module()