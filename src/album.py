class Album(object):
    def __init__(self, name=None):
        self.name = None
        if name:
            self.name = name
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def remove_song(self, song):
        if song in self.songs:
            self.songs.pop(self.songs.index(song))

    def set_name(self, name):
        self.name = name

    def __len__(self):
        return len(self.songs)
