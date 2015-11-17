from test import (test_playlist, test_albumdb, test_track,
                  test_metadata, test_trackdb, test_playlistview,
                  test_mainwindow)


def testMetadata():
    test_metadata.test1()


def testTrack():
    test_track.test1()


def testTrackDB():
    test_trackdb.test1()


def testAlbumDB():
    test_albumdb.test1()


def testPlaylist():
    test_playlist.test1()


def testPlaylistview():
    test_playlistview.main_appdemo()

if __name__ == '__main__':
    # testTrack()
    # testMetadata()
    test_mainwindow.test()
