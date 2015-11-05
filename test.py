from test import test_track, test_metadata, test_trackdb, test_albumdb


def testMetadata():
    test_metadata.test1()


def testTrack():
    test_track.test1()


def testTrackDB():
    test_trackdb.test1()


def testAlbumDB():
    test_albumdb.test1()

if __name__ == '__main__':
    testAlbumDB()
    #testMetadata()
