from src.widgets.mainwindow import Ui_main_window
from PyQt4 import QtGui, QtCore
import time

class PlayerControl(QtCore.QThread):
    def __init__(self):
        super(self.__class__, self).__init__()
        pass


class TestThread(QtCore.QThread):
    def __init__(self):
        super(self.__class__, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        # for i in range(1000):
        print "Tada"
        time.sleep(2)


class Miusik(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(Miusik, self).__init__(parent)
        self.main_window = Ui_main_window()
        self.main_window.setupUi(self)
        # self.connect(self.main_window.add_file_button, QtCore.SIGNAL('clicked()'), self.open_files_callback)
        self.main_window.add_file_button.clicked.connect(self.open_files_callback)
        self.main_window.playlists_tabs.plusButton.clicked.connect(self.add_tab_callback)
        self.main_window.app_info_button.clicked.connect(self.test_thread)

    def add_tab_callback(self):
        index = self.main_window.playlists_tabs.addTab("Playlist")
        self.main_window.playlists_tabs.tab.start_rename(index)
        # TODO: create new playlist and add it to playlist manager

    def open_files_callback(self):
        files = QtGui.QFileDialog.getOpenFileNames(caption="Open Files",
                                                   directory="D:/Drive E")
        print files

    def test_thread(self):
        self.threads = []
        for i in range(1000):
            my_test = TestThread()
            self.threads.append(my_test)
            my_test.start()


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    miusik = Miusik()
    miusik.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
