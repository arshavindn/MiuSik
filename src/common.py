import os

APP_NAME = 'Miusik'

TRACKDB_VER = "trackdb ver 1.0"
COVERDB_VER = "coverdb ver 1.0"


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


def get_user_dir():
    return os.path.expanduser('~')


def get_appdata_dir():
    return get_user_dir() + '/' + APP_NAME
