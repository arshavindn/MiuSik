import os

APP_NAME = 'Miusik'


def get_user_dir():
    return os.path.expanduser('~')


def get_appdata_dir():
    return get_user_dir() + '/' + APP_NAME
