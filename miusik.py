from src.widgets.mainwindow import Ui_main_window
from src import common
from PyQt4 import QtGui, QtCore
import time
import ConfigParser


class PlayerControl(QtCore.QThread):
    def __init__(self):
        super(self.__class__, self).__init__()
        pass


class Miusik(QtGui.QMainWindow, Ui_main_window):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.shuffle = "Off"
        self.repeat = "Off"
        self.load_sss()

        self.set_menu_action(self.shuffle_button, self.shuffle_triggered, self.shuffle)
        self.set_menu_action(self.repeat_button, self.repeat_triggered, self.repeat)

        self.add_file_button.clicked.connect(self.open_files_callback)
        self.playlists_tabs.plusButton.clicked.connect(self.add_tab_callback)

    def set_menu_action(self, button, func, val):
        for act in button.menu().actions():
            act.triggered[()].connect(lambda xact=act: func(xact))
            if act.text().__str__() == val:
                act.setChecked(True)

    def add_tab_callback(self):
        index = self.playlists_tabs.addTab("Playlist")
        self.playlists_tabs.tab_bar.start_rename(index)
        # test: print length of given idex table in playlist tabs
        # TODO: create new playlist and add it to playlist manager

    def open_files_callback(self):
        files = QtGui.QFileDialog.getOpenFileNames(caption="Open Files",
                                                   directory="D:/Drive E")
        print files
        # TODO: add theses files to current playlist

    def shuffle_triggered(self, act):
        self.shuffle = act.text().__str__()
        print self.shuffle, self.repeat

    def repeat_triggered(self, act):
        self.repeat = act.text().__str__()
        print self.shuffle, self.repeat

    def load_sss(self, loc=None):
        """
            Load session settings.
        """
        if not loc:
            loc = common.get_appdata_dir() + "/settings.ini"
        sss = ConfigParser.ConfigParser()
        sss.read(loc)
        if sss.sections():
            self.shuffle = sss.get('session', 'shuffle')
            self.repeat = sss.get('session', 'repeat')
        else:
            sss.add_section('session')
            sss.set('session', 'shuffle', self.shuffle)
            sss.set('session', 'repeat', self.repeat)
            with open(loc, 'w') as configfile:
                sss.write(configfile)

    def save_sss(self, loc=None):
        if not loc:
            loc = common.get_appdata_dir() + '/settings.ini'
        sss = ConfigParser.ConfigParser()
        sss.set('session', 'shuffle', self.shuffle)
        sss.set('session', 'repeat', self.repeat)
        with open(loc, 'w') as configfile:
                sss.write(configfile)


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    miusik = Miusik()
    miusik.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
