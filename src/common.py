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


def format_time(seconds):
    seconds = int(round(seconds))
    hours = int(seconds) / 3600
    mins = int(seconds) / 60 - hours * 60
    secs = int(seconds) - hours * 3600 - mins * 60
    if hours == 0:
        return "%d:%d" %(mins, secs)
    else:
        return "%d:%d:%d" %(hours, mins, secs)


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
