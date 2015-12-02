# -*- coding: utf-8 -*-

from src.widgets.mainwindow import Ui_main_window
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

# end class PlayerControler


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

        self.seek_slider_timer  =QtCore.QTimer()
        self.seek_slider_timer.timeout.connect(self.seek_slider_move)

        self.play_controler = PlayerControler()
        self.play_controler.start()
        self.play_pause_button.clicked.connect(self.play_toggle)
        self.next_button.clicked.connect(self.next_btn_click)
        self.connect(self.volume_slider.slider, QtCore.SIGNAL("valueChanged(int)"),
                     self.volume_handle)
        self.connect(self.seek_slider, QtCore.SIGNAL("valueChanged(int)"),
                     self.play_controler.player.seek)

        self.set_menu_action(self.shuffle_button, self.shuffle_triggered, self.shuffle)
        self.set_menu_action(self.repeat_button, self.repeat_triggered, self.repeat)
        # add files handler
        self.add_file_button.clicked.connect(self.open_files_callback)
        # add tab handler
        self.playlists_tabs.plusButton.clicked.connect(self.add_tab_callback)
        self.app_info_button.clicked.connect(self.test_playlist_tab)  # for test

        settings = QtCore.QSettings()
        # self.recentFiles = settings.value("RecentFiles").toStringList()
        self.restoreGeometry(
                settings.value("MainWindow/Geometry").toByteArray())
        self.restoreState(settings.value("MainWindow/State").toByteArray())

    def volume_handle(self, rate):
        self.play_controler.player.set_volume(rate)
        icon = QtGui.QIcon()
        if rate == 0:
            icon.addPixmap(QtGui.QPixmap(":/icons/volume-0.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        elif rate > 0 and rate <= 33:
            icon.addPixmap(QtGui.QPixmap(":/icons/volume-1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        elif rate > 33 and rate <= 66:
            icon.addPixmap(QtGui.QPixmap(":/icons/volume-2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        else:
            icon.addPixmap(QtGui.QPixmap(":/icons/volume-full.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.volume_button.setIcon(icon)

    def play_song_handle(self, song):
        self.play_controler.player.play_given_song(song)
        current_song_len = \
            self.trackdb.get_track_by_loc(song).get_tag_raw('__length')
        self.playing_song.setText(self.trackdb.get_track_by_loc(song).get_tag_raw('title', True))
        self.artist.setText(self.trackdb.get_track_by_loc(song).get_tag_raw('artist', True))
        self.choose_next_timer.start(current_song_len*1000)
        self.seek_slider.setValue(0)
        self.seek_slider.setRange(0, int(round(current_song_len)))
        self.seek_slider_timer.start(1000)

    def seek_slider_move(self):
        self.seek_slider.setValue(self.seek_slider.value() + self.seek_slider.singleStep())

    def row_double_click(self, row):
        loc_inx = self.playlists_tabs.currentWidget().get_headertag_index("__loc")
        loc = unicode(self.playlists_tabs.currentWidget().item(row, loc_inx).text())
        self.play_song_handle(loc)
        self.playlists_tabs.current_song = loc
        curr_index = self.playlists_tabs.currentIndex()
        if self.playlists_tabs.current_playlist_index != curr_index:
            self.playlists_tabs.current_playlist_index = curr_index
            self.playlists_tabs.current_album = self.playlists_tabs.currentWidget().get_album_from_loc(loc)
        self.playlists_tabs.get_list_for_play(self.repeat)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_pause_button.setIcon(icon)

    def play_toggle(self):
        state = self.play_controler.player.get_status()
        icon = QtGui.QIcon()
        if state == playerbin.IS_PLAYING:
            self.play_controler.player.pause()
            icon.addPixmap(QtGui.QPixmap(":/icons/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.play_controler.is_playing = False
        elif state == playerbin.NOT_PLAYING:
            self.play_song_handle(self.playlists_tabs.current_song)
            icon.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        elif state == playerbin.PAUSED:
            self.play_controler.player.play()
            icon.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        else:  # IS_DONE
            self.play_controler.player.stop()
            self.play_controler.player.play()
            icon.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_pause_button.setIcon(icon)
        self.play_controler.is_playing = True

    def next_btn_click(self):
        self.playlists_tabs.current_song = \
                    self.playlists_tabs.choose_next_song(self.shuffle)
        if self.play_controler.is_playing:
            self.play_song_handle(self.playlists_tabs.current_song)
        else:
            self.play_controler.player.stop()
            self.play_controler.player.set_file(self.playlists_tabs.current_song)

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
        settings = QtCore.QSettings()
        settings.setValue("MainWindow/Geometry", QtCore.QVariant(
                          self.saveGeometry()))
        settings.setValue("MainWindow/State", QtCore.QVariant(
                          self.saveState()))
        # self.play_controler.quit()
        save_trackdb = MThread(self.trackdb.save_db)
        save_trackdb.start()
        #self.connect(test_th, QtCore.SIGNAL("finished()"), test_th.quit)
        save_coverdb = MThread(self.coverdb.save_db)
        save_coverdb.start()
        #self.connect(test_th1, QtCore.SIGNAL("finished()"), test_th.quit)


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("BK Team")
    app.setOrganizationDomain("github.com/arshavindn/Miusik")
    miusik = Miusik()
    qss_file = open('miusik.qss').read()
    miusik.setStyleSheet(qss_file)
    miusik.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
