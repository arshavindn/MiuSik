import os
import time
import metadata
import os.path, time


class Track(object):
    __slots__ = ["__tags", "_scan_valid"]

    def __init__(self, loc):
        """
            parameters:
                loc: must be valid unicode text location
        """
        self.__tags = {}
        self.__tags['__loc'] = loc
        self._scan_valid = None

    def __str__(self):
        # return self.__tags.get('title') + ', ' + self.__tags.get('album') + \
        #     ', ' + self.__tags.get('artist')
        return self.__tags.__str__()

    def get_file_size(self):
        """Return file size in Mb"""
        size = os.path.getsize(self.get_loc())  # it is bytes
        return round(size / 1024.0 / 1024.0, 2)

    def get_loc(self):
        return self.__tags['__loc']

    def get_dir_path(self):
        """
            Return folder path of file path
            Ex: file_path = u"D:/Music/It Will Rain.mp3"
            dir_path = u"D:/Music"
        """
        return os.path.dirname(self.get_loc())

    def get_basename(self):
        """
            Return file name
            Ex: file_path = u"D:/Music/It Will Rain.mp3"
            dir_path = u"It Will Rain.mp3"
        """
        return os.path.basename(self.get_loc())

    def __set_tag_raw(self, tag, values):
        """
            Private function for setting tag to __tags
        """
        if not isinstance(values, list):
            if not tag.startswith("__"):  # internal tags don't have to be lists
                values = [values]
        else:
            [value for value in values if value not in (None, u'')]

        if not values:
            try:
                del self.__tags[tag]
            except KeyError:
                pass
        else:
            self.__tags[tag] = values

    def list_tags(self):
        return self.__tags.keys() + ['__basename']

    def set_tags(self):
        """
            Reads tags from the file and set for this Track.

            Returns False if unsuccessful, otherwise returns
            Format object from 'src.metadata'.
        """
        try:
            f = metadata.get_format(self.get_loc())
            if f is None:
                return False  # not a supported type
            ntags = f.read_all()
            for k, v in ntags.iteritems():
                self.__set_tag_raw(k, v)

            # remove tags that have been deleted in the file, while
            # taking into account that the db may have tags not
            # supported by the file's tag format.
            if f.others:
                supported_tags = [t for t in self.list_tags()
                                  if not t.startswith("__")]
            else:
                supported_tags = f.tag_mapping.keys()
            for tag in supported_tags:
                if tag not in ntags.keys():
                    self.__set_tag_raw(tag, None)

            # fill out file specific items
            mtime = time.localtime(os.stat(self.get_loc()).st_mtime)
            self.__set_tag_raw('__modified', mtime)
            # TODO: this probably breaks on non-local files
            folder_path = self.get_dir_path()
            self.__set_tag_raw('__basedir', folder_path)
            return f
        except Exception:
            return False

    def write_tags(self):
        """
            Writes tags to the file for this Track.

            Returns False if unsuccessful, and a Format object from
            `xl.metadata` otherwise.
        """
        try:
            f = metadata.get_format(self.get_loc())
            if f is None:
                return False  # not a supported type
            f.write_tags(self.__tags)
            return f
        except IOError:
            return False
        except Exception:
            return False

    def read_tags(self):
        """
            Reads tags from the file for this Track.

            Returns False if unsuccessful, and a Format object from
            `xl.metadata` otherwise.
        """
        try:
            f = metadata.get_format(self.get_loc())
            if f is None:
                self._scan_valid = False
                return False # not a supported type
            ntags = f.read_all()
            for k, v in ntags.iteritems():
                self.__tags[k] = v

            # remove tags that have been deleted in the file, while
            # taking into account that the db may have tags not
            # supported by the file's tag format.
            if f.others:
                supported_tags = [ t for t in self.list_tags() \
                        if not t.startswith("__") ]
            else:
                supported_tags = f.tag_mapping.keys()
            for tag in supported_tags:
                if tag not in ntags.keys():
                    self.__tags[tag] = None

            # fill out file specific items
            mtime = time.ctime(os.path.getmtime(self.get_loc()))
            self.__tags['__modified'] = mtime
            # TODO: this probably breaks on non-local files
            path = os.path.dirname(self.get_loc())
            self.__tags['__basedir'] = path
            self._scan_valid = True
            return f
        except Exception:
            self._scan_valid = False
            return False