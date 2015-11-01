from PyQt4 import QtGui
import sys
from src.playerbin import Player


class MyApp(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Gstreamer init
        self.player = Player()
        self.player.set_file('D:/Drive E/Music/Bruno Mars - It Will Rain.mp3')
        # Play button
        self.play_button = QtGui.QPushButton('Play', self)
        self.play_button.clicked.connect(self.player.play)
        self.repeat()
        self.show()

    def repeat(self):
        if self.player.is_done():
            self.player.set_file('D:/Drive E/Music/Bruno Mars - It Will Rain.mp3')
            self.player.play()


def main():
    app = QtGui.QApplication(sys.argv)

    w = MyApp()
    w.setWindowTitle('MyApp')

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
