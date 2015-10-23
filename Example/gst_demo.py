import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
Gst.init(None)

# pipeline = "filesrc location=C:/Photograph-Ed_Sheeran.mp3 ! decodebin ! audioconvert ! autoaudiosink"

# player = Gst.parse_launch(pipeline)
# player.set_state(Gst.State.PLAYING)
## get position
# float(player.query_position(Gst.Format.TIME)[1])/Gst.SECOND
## get duration
# player.query_duration(Gst.Format.TIME)


def play_music_1(location):
    pipeline_string = "filesrc location=" + \
                      location + \
                      " ! decodebin ! audioconvert ! autoaudiosink"
    player = Gst.parse_launch(pipeline_string)
    player.set_state(Gst.State.PLAYING)


def play_music_2(location):
    player = Gst.Pipeline.new("player")
    print player
    source = Gst.ElementFactory.make("filesrc", "file-source")
    print source
    decoder = Gst.ElementFactory.make("mad", "mp3-decoder")
    conv = Gst.ElementFactory.make("audioconvert", "converter")
    sink = Gst.ElementFactory.make("autoaudiosink", "a_a_sink")
    player.add(source)
    player.add(decoder)
    player.add(conv)
    player.add(sink)
    source.link(decoder)
    decoder.link(conv)
    conv.link(sink)
    player.get_by_name("file-source").set_property("location", location)
    player.set_state(Gst.State.PLAYING)


if __name__ == '__main__':
    mypath = "D:/Drive E/Music/Bruno Mars - It Will Rain.mp3"
    play_music_2(mypath)
