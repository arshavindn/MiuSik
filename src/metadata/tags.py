class _TD(object):
    __slots__ = [
        'name',  # descriptive name
        'tag_name',  # raw tag name
        'type',
        'editable',
        'min',
        'max',
        'use_disk',  # set true if should retrieve tag from disk
    ]

    def __init__(self, name, type, **kwargs):
        self.name = name
        self.type = type

        # these are overridable by keyword arg
        self.editable = True
        self.use_disk = False

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def __str__(self):
        return self.name + " is " + self.tag_name + " tag, " + self.type + " type."

tag_data = {
    'album':            _TD('Album',        'text'),
    'arranger':         _TD('Arranger',     'text'),
    'artist':           _TD('Artist',       'text'),
    'author':           _TD('Author',       'text'),
    'bpm':              _TD('BPM',          'int', min=0, max=500),
    'copyright':        _TD('Copyright',    'text'),
    'comment':          _TD('Comment',      'multiline', use_disk=True),
    'composer':         _TD('Composer',     'text'),
    'conductor':        _TD('Conductor',    'text'),
    'cover':            _TD('Cover',        'image', use_disk=True),
    'date':             _TD('Date',         'datetime'),
    'discnumber':       _TD('Disc',         'dblnum', min=0, max=50),
    'encodedby':        _TD('Encoded by',   'text'),
    'genre':            _TD('Genre',        'text'),
    'grouping':         _TD('Grouping',     'text'),
    'isrc':             _TD('ISRC',         'text'),
    'lyrics':           _TD('Lyrics',       'multiline', use_disk=True),
    'lyricist':         _TD('Lyricist',     'text'),
    'organization':     _TD('Organization', 'text'),
    'originalalbum':    _TD('Original album', 'text'),
    'originalartist':   _TD('Original artist', 'text'),
    'originaldate':     _TD('Original date', 'text'),
    'part':             None,
    'performer':        _TD('Performer',    'text'),
    'title':            _TD('Title',        'text'),
    'tracknumber':      _TD('Track',        'dblnum', min=0, max=500),
    'version':          _TD('Version',      'text'),
    'website':          _TD('Website',      'text'),

    # various internal tags
    '__bitrate':        _TD('Bitrate',      'bitrate', editable=False),
    '__basedir':        None,
    '__date_added':     _TD('Date added',   'timestamp', editable=False),
    '__last_played':    _TD('Last played',  'timestamp', editable=False),
    '__length':         _TD('Length',       'time', editable=False),
    '__loc':            _TD('Location',     'location', editable=False),
    '__modified':       _TD('Modified',     'timestamp', editable=False),
    '__playtime':       _TD('Play time',    'time', editable=False),
    '__playcount':      _TD('Times played', 'int', editable=False),
    '__rating':         None,  # currently special.
    '__startoffset':    _TD('Start offset', 'time', min=0, max=3600),  # TODO: calculate these parameters
    '__stopoffset':     _TD('Stop offset',  'time', min=0, max=3600),
}

for k, v in tag_data.iteritems():
    if v:
        v.tag_name = k


def get_default_tagdata(tag):
    '''If the tagname is not in tag_data, you can use this function
       to get a _TD object for it'''

    return _TD(tag, 'text', editable=(not tag.startswith('__')), tag_name=tag)
