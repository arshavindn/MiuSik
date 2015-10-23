import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GstAudio

# STATE
NOT_PLAYING = -1
IS_PLAYING = -2
PAUSED = -3
IS_DONE = -4


class Player():
    def __init__(self):
        Gst.init(None)
        self.player = Gst.ElementFactory.make("playbin", "player")
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

    def __str__(self):
        state = self.get_status()
        if state == NOT_PLAYING:
            return "Not playing"
        elif state == IS_PLAYING:
            return "Playing " + self.player.get_property('current-uri')
        elif state == PAUSED:
            return "Pause " + self.player.get_property('current-uri')
        else:  # IS_DONE
            return "Done playing " + self.player.get_property('current-uri')

    def set_file(self, filepath):
        self.player.set_property('uri', 'file:///' + filepath)

    def get_status(self):
        '''
        Return one of four states (NOT_PLAYING, IS_PLAYING, PAUSED, IS_DONE)
        '''
        dura_temp = self.get_duration()
        ok, state, pending = self.player.get_state(0)
        if dura_temp is None or ok == Gst.StateChangeReturn.FAILURE:
            return -1
        else:
            if int(dura_temp) == int(self.get_position()):
                return -4
            elif ok == Gst.StateChangeReturn.ASYNC:
                if pending == Gst.State.PLAYING:
                    return -2
                elif pending == Gst.State.PAUSED:
                    return -3
            elif ok == Gst.StateChangeReturn.SUCCESS:
                if state == Gst.State.PLAYING:
                    return -2
                elif state == Gst.State.PAUSED:
                    return -3

    def play(self):
        if self.get_status() == IS_DONE:
            self.stop()
        self.player.set_state(Gst.State.PLAYING)

    def pause(self):
        self.player.set_state(Gst.State.PAUSED)

    def stop(self):
        self.player.set_state(Gst.State.NULL)

    def get_position(self):
        '''
        Return current position (second).
        '''
        return float(self.player.query_position(Gst.Format.TIME)[1])/Gst.SECOND

    def get_duration(self):
        ok = self.player.query_duration(Gst.Format.TIME)[0]
        if ok:
            return float(self.player.query_duration(Gst.Format.TIME)[1])/Gst.SECOND
        else:
            return None

    def seek(self, position):
        '''
        Seek to position (second).
        '''
        self.player.seek_simple(Gst.Format.TIME,
                                Gst.SeekFlags.FLUSH |
                                Gst.SeekFlags.KEY_UNIT,
                                position * Gst.SECOND)
        # self.player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, position * Gst.SECOND)

    def get_volume(self):
        '''
        Return volume rate (0.0 -> 1.0).
        '''
        return self.player.get_volume(GstAudio.StreamVolumeFormat.LINEAR)

    def set_volume(self, rate):
        self.player.set_volume(GstAudio.StreamVolumeFormat.LINEAR, rate)

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
        elif t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
