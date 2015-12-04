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
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    if hours == 0:
        return "%d:%02d" %(mins, secs)
    else:
        return "%02d:%02d:%02d" %(hours, mins, secs)

def reverse_time_str(time_str):
    lst = time_str.split(':')
    lst[:] = [int(x) for x in lst]
    if len(lst) == 2:
        return lst[0] * 60 + lst[1]
    elif len(lst) == 3:
        return lst[0] * 3600 + lst[1] * 60 + lst[2]


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
