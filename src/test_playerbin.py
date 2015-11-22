import playerbin
import os
from PyQt4 import QtGui, QtCore
from time import sleep

folder = u'D:/Drive E/Vietnam'
songs = [folder + '/' + song for song in os.listdir(folder)]


class VolumeButton(QtGui.QToolButton):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)

    def enterEvent(self, event):
        # QtCore.QTimer.singleShot(500, self.parent().slider.show)
        self.show_slider = QtCore.QTimer()
        self.show_slider.setSingleShot(True)
        self.show_slider.timeout.connect(self.parent().slider.show)
        self.show_slider.start(500)

        self.hide_slider = QtCore.QTimer()
        self.hide_slider.setSingleShot(True)
        self.hide_slider.timeout.connect(self.parent().slider.hide)
        print self.geometry()
        print self.parent().slider.geometry(), self.parent().slider.sizeHint(), "\n"

    def leaveEvent(self, event):
        self.hide_slider.start(1500)

    def break_hiding_slider(self):
        self.hide_slider.stop()
        self.hide_slider.deleteLater()

    def show_slider(self):
        pass


class VolumeSilder(QtGui.QFrame):
    """docstring for VolumeSilder"""
    mouse_over = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(VolumeSilder, self).__init__(parent)
        # self.setWindowFlags(QtCore.Qt.ToolTip)
        self.slider = QtGui.QSlider()
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.setFixedWidth(120)
        hbox = QtGui.QHBoxLayout(self)
        hbox.setMargin(3)
        hbox.addWidget(self.slider)
        self.setLayout(hbox)

    def enterEvent(self, event):
        self.mouse_over.emit()

    def leaveEvent(self, event):
        QtCore.QTimer.singleShot(200, self.hide)

# class PlayControler(QtCore.QThread):
#     def __init__(self, sender, songs):
#         super(self.__class__, self).__init__(sender)
#         self.sender = sender
#         self.songs = songs
#         self.play_state = False
#         self.current_song_index = 0
#         self.player = playerbin.Player()
#         # self.player.set_file(self.songs[self.current_song_index])
#         self.sender.next_signal.connect(self.next)
#         self.sender.pre_signal.connect(self.previous)

#     def __del__(self):
#         self.wait()

#     def previous(self):
#         if self.current_song_index == 0:
#             self.current_song_index = len(self.songs) - 1
#         else:
#             self.current_song_index -= 1
#         self.player.play_given_song(self.songs[self.current_song_index])

#     def next(self):
#         if self.current_song_index == len(self.songs) - 1:
#             self.current_song_index = 0
#         else:
#             self.current_song_index += 1
#         self.player.play_given_song(self.songs[self.current_song_index])

#     def run(self):
#         while True:
#             if self.play_state:
#                 status = self.player.get_status()
#                 if status == playerbin.NOT_PLAYING:
#                     self.player.play_given_song(self.songs[self.current_song_index])
#                 elif status == playerbin.PAUSED:
#                     self.player.play()
#                 elif status == playerbin.IS_DONE:
#                     self.current_song_index += 1
#                     if self.current_song_index == len(songs):
#                         self.player.stop()
#                     else:
#                         self.player.play_given_song(self.songs[self.current_song_index])
#                 else:
#                     pass
#             else:
#                 self.player.pause()
#             sleep(0.2)


class ExUI(QtGui.QWidget):
    next_signal = QtCore.pyqtSignal()
    pre_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(self.__class__, self).__init__()
        print "ExUI", type(self)
        self.play_btn = QtGui.QPushButton("Play", self)
        self.play_btn.move(100, 20)
        self.next_btn = QtGui.QPushButton("Next", self)
        self.next_btn.move(180, 20)
        self.pre_btn = QtGui.QPushButton("Previous", self)
        self.pre_btn.move(20, 20)
        self.volume_btn = VolumeButton(self)
        self.volume_btn.setText('Volume')
        self.volume_btn.move(80, 50)
        self.slider = VolumeSilder(self)
        self.slider.slider.setRange(0, 100)

        # self.play_btn.clicked.connect(self.play_press)
        # self.next_btn.clicked.connect(self.emit_next_signal)
        # self.pre_btn.clicked.connect(self.emit_pre_signal)
        self.slider.mouse_over.connect(self.volume_btn.break_hiding_slider)
        self.volume_btn.clicked.connect(self.volume_btn_clicked)

        # self.play_controler = PlayControler(self, songs)
        # self.play_controler.start()

    def volume_btn_clicked(self):
        self.volume_btn.show_slider.stop()
        self.volume_btn.show_slider.deleteLater()
        self.volume_btn.setText("Mute")
        self.slider.slider.setValue(0)

    # def play_press(self):
    #     if self.play_controler.play_state:
    #         self.play_controler.play_state = False
    #         self.play_btn.setText("Play")
    #     else:
    #         self.play_controler.play_state = True
    #         self.play_btn.setText("Pause")
    #     print "play_state", self.play_controler.play_state

    # def emit_next_signal(self):
    #     self.next_signal.emit()

    # def emit_pre_signal(self):
    #     self.pre_signal.emit()


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    ex = ExUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
