import os

APP_NAME = 'Miusik'

TRACKDB_VER = "trackdb ver 1.0"
COVERDB_VER = "coverdb ver 1.0"

def get_user_dir():
    return os.path.expanduser(u'~')


def get_appdata_dir():
    return get_user_dir() + '/' + APP_NAME

default_session_settings = {
    'shuffle': ['Off', ('Off', 'Album', 'Playlist' )],
    'repeat': ['Off', ('Off', 'Song', 'Album', 'Playlist')],
    'open_folder_dialog_loc': get_user_dir()
}


class VersionError(Exception):
    """
       Represents version discrepancies
    """
    #: the error message
    message = None

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
        return repr(self.message)
