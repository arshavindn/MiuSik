import os
from src import metadata


class Track(object):
    __slots__ = ["__tags"]

    def __init__(self, loc):
        """
            parameters:
                loc: must be unicode string
        """
        self.__tags = {}
        self.__tags['__loc'] = loc

    def get_file_size(self):
        """Return file size in Mb"""
        size = os.path.getsize(self.get_loc())  # it is bytes
        return round(size / 1024.0 / 1024.0, 2)

    def get_loc(self):
        return self.__tags['__loc']
