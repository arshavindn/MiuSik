# -*- coding: utf-8 -*-

from src.widgets.mainwindow import Ui_main_window
from src.widgets.playlistview import PlaylistTable
from src import common, track, playerbin
from src.database import trackdb, coverdb
from PyQt4 import QtGui, QtCore
import time
import ConfigParser


class MThread(QtCore.QThread):
    def __init__(self, func, *args, **kwargs):
        super(MThread, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        self.wait()

    def run(self):
        self.func(*self.args, **self.kwargs)
# end class MThead

def test():
    for i in range(10):
        print "tada"

def test2(name):
    for i in range(5):
        print name


class PlayerControler(QtCore.QThread):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.player = playerbin.Player()
        self.is_playing = False

    def __del__(self):
        self.wait()


class AddTracksThread(QtCore.QThread):
    def __init__(self, locs, trackdb, coverdb, table):
        super(self.__class__, self).__init__()
        self.locs = locs
        self.trackdb = trackdb
        self.coverdb = coverdb
        self.table = table

    def run(self):
        for loc in self.locs:
            self.table.add_track(loc, self.trackdb, self.coverdb)
            time.sleep(0.03)


class Miusik(QtGui.QMainWindow, Ui_main_window):
    play_order = QtCore.pyqtSignal()
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

        self.choose_next_timer = QtCore.QTimer()
        self.choose_next_timer.timeout.connect(self.next_btn_click)

        self.play_controler = PlayerControler()
        self.play_controler.start()
        self.play_pause_button.clicked.connect(self.play_toggle)
        self.next_button.clicked.connect(self.next_btn_click)

        self.set_menu_action(self.shuffle_button, self.shuffle_triggered, self.shuffle)
        self.set_menu_action(self.repeat_button, self.repeat_triggered, self.repeat)
        # add files handler
        self.add_file_button.clicked.connect(self.open_files_callback)
        # add tab handler
        self.playlists_tabs.plusButton.clicked.connect(self.add_tab_callback)
        self.app_info_button.clicked.connect(self.test_playlist_tab)  # for test

    def print_sorted_col(self, col):
        print col

    def row_double_click(self, row):
        print row
        loc_inx = self.playlists_tabs.currentWidget().get_headertag_index("__loc")
        loc = unicode(self.playlists_tabs.currentWidget().item(row, loc_inx).text())
        self.play_controler.player.play_given_song(loc)
        self.playlists_tabs.current_playlist = self.playlists_tabs.currentIndex()
        self.playlists_tabs.current_album = self.playlists_tabs.currentWidget().get_album_from_loc(loc)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_pause_button.setIcon(icon)

    def play_toggle(self):
        # TODO: fix icon show wrongly in some situation
        print self.playlists_tabs.list_for_play
        if self.play_controler.player.get_status() == playerbin.IS_PLAYING:
            self.play_controler.player.pause()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        elif self.play_controler.player.get_status() == playerbin.NOT_PLAYING:
            self.play_controler.player.play_given_song(self.playlists_tabs.current_song)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        elif self.play_controler.player.get_status() == playerbin.PAUSED:
            self.play_controler.player.play()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_pause_button.setIcon(icon)

    def next_btn_click(self):
        self.playlists_tabs.current_song = \
                self.playlists_tabs.choose_next_song(self.shuffle)
        self.play_controler.player.play_given_song(self.playlists_tabs.current_song)
        current_song_len = \
            self.trackdb.get_track_by_loc(self.playlists_tabs.current_song).get_tag_raw('__length')
        self.choose_next_timer.start(current_song_len*1000)

    def set_menu_action(self, button, func, val):
        for act in button.menu().actions():
            act.triggered[()].connect(lambda xact=act: func(xact))
            if str(act.text()) == val:
                act.setChecked(True)

    def add_tab_callback(self):
        self.playlists_tabs.addTab()
        self.connect(self.playlists_tabs.currentWidget(), QtCore.SIGNAL("cellDoubleClicked(int,int)"),
                     self.row_double_click)
        # self.playlists_tabs.tab_bar.start_rename(index)

    def test_playlist_tab(self):
        """
            Test playlist tab when click on About button.
        """
        table = self.playlists_tabs.widget(0)
        track1 = track.Track(u"D:\\Drive E\\Vietnam\\B\u1ea3n T\xecnh Ca \u0110\u1ea7u Ti\xean - Duy Khoa.mp3")
        table.add_track(track1)
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
        current_index = self.playlists_tabs.currentIndex()
        if current_index != -1:
            self.add_track_thread = AddTracksThread(locs,
                                                    self.trackdb, self.coverdb,
                                                    self.playlists_tabs.currentWidget())
            self.add_track_thread.start()
            self.connect(self.add_track_thread, QtCore.SIGNAL("finished()"),
                         lambda index=current_index: self.add_track_done(index))

    def add_track_done(self, index):
        if not self.playlists_tabs.current_song:
            self.playlists_tabs.current_playlist_index = index
            self.playlists_tabs.get_list_for_play(self.repeat)
            self.playlists_tabs.current_song = \
                self.playlists_tabs.get_current_playlist().get_loc_list_gui()[0]
            self.playlists_tabs.current_album = \
                self.playlists_tabs.get_current_playlist().get_album_from_loc(
                    self.playlists_tabs.current_song)
            self.add_track_thread.deleteLater()

    def shuffle_triggered(self, act):
        self.shuffle = str(act.text())
        print self.shuffle, self.repeat
        # for key, value in self.trackdb.get_songs():
        #     print key, value
        # print len(self.trackdb)
        # self.trackdb.save_db()
        # self.coverdb.save_db()

    def repeat_triggered(self, act):
        self.repeat = str(act.text())
        print self.shuffle, self.repeat
        self.playlists_tabs.get_list_for_play(self.repeat)

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

    def closeEvent(self, event):
        self.play_controler.quit()
        save_trackdb = MThread(self.trackdb.save_db)
        save_trackdb.start()
        #self.connect(test_th, QtCore.SIGNAL("finished()"), test_th.quit)
        save_coverdb = MThread(self.coverdb.save_db)
        save_coverdb.start()
        #self.connect(test_th1, QtCore.SIGNAL("finished()"), test_th.quit)



def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    miusik = Miusik()
    qss_file = open('miusik.qss').read()
    miusik.setStyleSheet(qss_file)
    miusik.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
