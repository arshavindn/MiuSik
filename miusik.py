# -*- coding: utf-8 -*-

from src.widgets.mainwindow import Ui_main_window
from src import common, track, plmanager
from src.database import trackdb, coverdb
from PyQt4 import QtGui, QtCore
import time
import ConfigParser


class PlayerControl(QtCore.QThread):
    def __init__(self):
        super(self.__class__, self).__init__()
        pass


class AddTracksThread(QtCore.QThread):
    def __init__(self, locs, playlist, trackdb, coverdb, table):
        super(self.__class__, self).__init__()
        self.locs = locs
        self.playlist = playlist
        self.trackdb = trackdb
        self.coverdb = coverdb
        self.table = table

    def __del__(self):
        self.wait()

    def run(self):
        for loc in self.locs:
            tr = self.playlist.add_track(loc, self.trackdb, self.coverdb)
            if not tr:
                print "nah"
                continue
            else:
                self.table.add_track(tr)
                time.sleep(0.05)
            print "tada"


class Miusik(QtGui.QMainWindow, Ui_main_window):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.shuffle = "Off"
        self.repeat = "Off"
        self.load_sss()
        self.trackdb_loc = common.get_appdata_dir() + "/tracks.db"
        self.coverdb_loc = common.get_appdata_dir() + "/covers.db"
        self.trackdb = trackdb.TrackDB(self.trackdb_loc)
        self.coverdb = coverdb.CoverDB(self.coverdb_loc)

        self.playlist_manager = plmanager.PlaylistManager()

        self.set_menu_action(self.shuffle_button, self.shuffle_triggered, self.shuffle)
        self.set_menu_action(self.repeat_button, self.repeat_triggered, self.repeat)
        # add files handler
        self.add_file_button.clicked.connect(self.open_files_callback)
        # add tab handler
        self.playlists_tabs.plusButton.clicked.connect(self.add_tab_callback)
        self.connect(self.playlists_tabs.tab_bar, QtCore.SIGNAL("finishedRename(int, QString)"),
                     self.playlist_rename)
        self.connect(self.playlists_tabs.tab_bar, QtCore.SIGNAL("tabCloseRequested(int)"),
                     self.playlist_manager.remove_playlist)
        self.connect(self.playlists_tabs.tab_bar, QtCore.SIGNAL("tabMoved(int, int)"),
                     self.playlist_manager.reindex_list)
        # current playlist change handler
        self.connect(self.playlists_tabs.tab_bar, QtCore.SIGNAL("currentChanged(int)"),
                     self.change_cur_pl)
        self.app_info_button.clicked.connect(self.test_playlist_tab)  # for test

    def print_sorted_col(self, col):
        print col

    def change_cur_pl(self, index):
        self.playlist_manager.set_cur_pl(index)

    def set_menu_action(self, button, func, val):
        for act in button.menu().actions():
            act.triggered[()].connect(lambda xact=act: func(xact))
            if act.text().__str__() == val:
                act.setChecked(True)

    def add_tab_callback(self):
        playlist = self.playlist_manager.add_new_playlist()
        index = self.playlists_tabs.addTab(playlist.get_name())
        self.playlists_tabs.tab_bar.start_rename(index)

    def playlist_rename(self, index, qname):
        playlist = self.playlist_manager.get_playlist(index)
        playlist.rename(unicode(qname))

    def test_playlist_tab(self):
        """
            Test playlist tab when click on About button.
        """
        table = self.playlists_tabs.widget(0)
        track1 = track.Track(u"D:\\Drive E\\Vietnam\\B\u1ea3n T\xecnh Ca \u0110\u1ea7u Ti\xean - Duy Khoa.mp3")
        table.add_track(track1)
        print self.playlist_manager.get_playlist_names()
        # horiz_header = table.horizontalHeader()
        # for i in range(len(table.all_header)):
        #     print i+1, table.all_header[i]
        # print horiz_header.visualIndex(0)
        # print table.horizontalHeaderItem(0).text(), type(table.horizontalHeaderItem(0).text())
        # for col in range(table.columnCount()):
        #     if not table.isColumnHidden(col):
        #         print table.horizontalHeaderItem(col).text()

    def open_files_callback(self):
        locs = QtGui.QFileDialog.getOpenFileNames(caption="Open Files",
                                                   directory=common.get_user_dir())
        locs = [unicode(f) for f in locs]
        print locs
        if self.playlist_manager.current_playlist != -1:
            self.add_track_thread = AddTracksThread(locs,
                                                    self.playlist_manager.get_playlist(
                                                        self.playlist_manager.current_playlist),
                                                    self.trackdb, self.coverdb,
                                                    self.playlists_tabs.currentWidget())
            self.add_track_thread.start()
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
            # self.trackdb_loc = sss.get('database', 'trackdb_loc')
            # self.trackdb_loc = sss.get('database', 'coverdb_loc')
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
