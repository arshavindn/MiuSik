import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
Gst.init(None)

mypath = "D:/Drive E/Music/Bruno Mars - It Will Rain.mp3"

player = Gst.Pipeline.new("player")
source = Gst.ElementFactory.make("filesrc", "file-source")
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
player.get_by_name("file-source").set_property("location", mypath)
player.set_state(Gst.State.PLAYING)
