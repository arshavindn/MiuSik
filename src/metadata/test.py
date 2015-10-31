from mp3 import MP3Format
from tags import tag_data


def test_tags_pair():
    song1 = MP3Format('D:/Drive E/Music/Bruno Mars - It Will Rain.mp3')
    tags = [k for k in tag_data.iterkeys()]
    # lst = song1._get_tag(song1._get_raw(), 'TIT2')
    # print lst
    print tags
    tag_pairs = song1.read_tags(tags)
    for k, v in tag_pairs.iteritems():
        if k != 'cover':
            print k, v
    # print tag_pairs['__rating']


def test_tags_module():
    print tag_data['album']

if __name__ == '__main__':
    test_tags_pair()
