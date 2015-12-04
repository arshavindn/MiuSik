# -*- coding: utf-8 -*-

import time, gc, os, codecs
import ConfigParser
from PyQt4 import QtGui, QtCore
from src.widgets.mainwindow import Ui_main_window
from src import common, playerbin
from src.database import trackdb


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


class PlayerControler(QtCore.QThread):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.player = playerbin.Player()
        self.is_playing = False

# end class PlayerControler


class AddTracksThread(QtCore.QThread):
    def __init__(self, locs, trackdb, table):
        super(self.__class__, self).__init__()
        self.locs = locs
        self.trackdb = trackdb
        # self.coverdb = coverdb
        self.table = table

    def run(self):
        # self.trackdb = trackdb.TrackDB(self.trackdb_loc)
        # self.coverdb = coverdb.CoverDB(self.coverdb_loc)
        for loc in self.locs:
            self.table.add_track(loc, self.trackdb)
            time.sleep(0.03)
        # self.trackdb.save_db()
        # self.coverdb.save_db()
        # del track_data
        # del cover_data
        print "from add track threads", gc.collect()


class Miusik(QtGui.QMainWindow, Ui_main_window):
    play_order = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.shuffle = "Off"
        self.repeat = "Off"
        self.trackdb_loc = common.get_appdata_dir() + "/tracks.db"
        # self.coverdb_loc = common.get_appdata_dir() + "/covers.db"
        self.trackdb = trackdb.TrackDB(self.trackdb_loc)
        # self.coverdb = coverdb.CoverDB(self.coverdb_loc)

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
        self.connect(self.seek_slider, QtCore.SIGNAL("sliderMoved(int)"),
                     self.seeker_dragging)

        self.set_menu_action(self.shuffle_button, self.shuffle_triggered, self.shuffle)
        self.set_menu_action(self.repeat_button, self.repeat_triggered, self.repeat)
        # add files handler
        self.add_file_button.clicked.connect(self.open_files_callback)
        # add tab handler
        self.playlists_tabs.plusButton.clicked.connect(self.add_tab_callback)
        self.connect(self.playlists_tabs, QtCore.SIGNAL("tab_added(int)"), self.tab_added_handler)
        # previous sesion
        self.load_sss()
        self.playlists_tabs.load_previous_session(common.get_appdata_dir() + "/playlists.mpk", self.trackdb)
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
        self.choose_next_timer.start(current_song_len*1000)
        self.seek_slider_timer.start(1000)
        self.playing_song.setText(self.trackdb.get_track_by_loc(song).get_tag_raw('title', True))
        self.artist.setText(self.trackdb.get_track_by_loc(song).get_tag_raw('artist', True))
        self.position.setText("0:00")
        self.seek_slider.setValue(0)
        self.seek_slider.setRange(0, int(round(current_song_len)))
        self.duration.setText(common.format_time(int(round(current_song_len))))
        self.playlists_tabs.current_album = \
            self.playlists_tabs.currentWidget().get_album_from_loc(song)

    def seek_slider_move(self):
        self.seek_slider.setValue(self.seek_slider.value() + self.seek_slider.singleStep())
        self.position.setText(common.format_time(self.seek_slider.value()))

    def seeker_dragging(self, pos):
        self.play_controler.player.seek(pos)
        self.choose_next_timer.start((self.seek_slider.maximum() - self.seek_slider.value())*1000)

    def row_double_click(self, row):
        loc_inx = self.playlists_tabs.currentWidget().get_headertag_index("__loc")
        loc = unicode(self.playlists_tabs.currentWidget().item(row, loc_inx).text())
        self.play_song_handle(loc)
        self.playlists_tabs.current_song = loc
        curr_index = self.playlists_tabs.currentIndex()
        if self.playlists_tabs.current_playlist_index != curr_index:
            self.playlists_tabs.current_playlist_index = curr_index
            self.playlists_tabs.get_list_for_play(self.repeat)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_pause_button.setIcon(icon)
        self.play_controler.is_playing = True

    def play_toggle(self):
        state = self.play_controler.player.get_status()
        icon = QtGui.QIcon()
        self.play_controler.is_playing = True
        if state == playerbin.IS_PLAYING:
            self.play_controler.player.pause()
            icon.addPixmap(QtGui.QPixmap(":/icons/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.seek_slider_timer.stop()
            self.play_controler.is_playing = False
        elif state == playerbin.NOT_PLAYING:
            self.play_song_handle(self.playlists_tabs.current_song)
            icon.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        elif state == playerbin.PAUSED:
            self.play_controler.player.play()
            icon.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.seek_slider_timer.start()
        else:  # IS_DONE
            self.play_controler.player.stop()
            self.play_controler.player.play()
            icon.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_pause_button.setIcon(icon)

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
        # self.playlists_tabs.tab_bar.start_rename(index)

    def tab_added_handler(self):
        self.connect(self.playlists_tabs.currentWidget(), QtCore.SIGNAL("cellDoubleClicked(int,int)"),
                     self.row_double_click)
        self.connect(self.playlists_tabs.currentWidget().horizontalHeader(),
                     QtCore.SIGNAL("sortIndicatorChanged(int, Qt::SortOrder)"),
                     lambda repeat=self.repeat: self.playlists_tabs.get_list_for_play(repeat))
        self.playlists_tabs.get_list_for_play(self.repeat)
        print "tab_added", gc.collect()

    def open_files_callback(self):
        open_dlg = QtGui.QFileDialog()
        locs = open_dlg.getOpenFileNames(parent=self, caption="Open Files",
                                                  directory='')
        locs = [unicode(f) for f in locs]
        open_dlg.deleteLater()
        current_index = self.playlists_tabs.currentIndex()
        if current_index != -1 and locs:
            self.add_track_thread = AddTracksThread(locs,
                                                    self.trackdb,
                                                    self.playlists_tabs.currentWidget())
            self.add_track_thread.start()
            self.connect(self.add_track_thread, QtCore.SIGNAL("finished()"),
                         lambda index=current_index: self.add_track_done(index))
        open_dlg = None
        print "open file dialog", gc.collect()

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
            loc = os.getcwd() + "/settings.ini"
        sss = ConfigParser.ConfigParser()
        sss.read(loc)
        if sss.sections():
            self.shuffle = sss.get('session', 'shuffle')
            self.repeat = sss.get('session', 'repeat')
            self.volume_handle(int(sss.get('session', 'volume')))
            self.volume_slider.slider.setValue(int(sss.get('session', 'volume')))
            self.playlists_tabs.current_playlist_index = int(sss.get('session', 'current playlist index'))
            self.playlists_tabs.setCurrentIndex(self.playlists_tabs.current_playlist_index)
            self.playlists_tabs.current_song = sss.get('session', 'current song')

    def save_sss(self, loc=None):
        if not loc:
            loc = os.getcwd() + '/settings.ini'
            print loc
        sss = ConfigParser.ConfigParser()
        sss.read(loc)
        sss.set('session', 'shuffle', self.shuffle)
        sss.set('session', 'repeat', self.repeat)
        sss.set('session', 'volume', self.play_controler.player.get_volume())
        sss.set('session', 'current song', self.playlists_tabs.current_song)
        sss.set('session', 'current playlist index', self.playlists_tabs.current_playlist_index)
        with codecs.open(loc, 'w', encoding='utf-8') as configfile:
                sss.write(configfile)

    def closeEvent(self, event):
        self.playlists_tabs.save_session(common.get_appdata_dir() + "/playlists.mpk")
        settings = QtCore.QSettings()
        settings.setValue("MainWindow/Geometry", QtCore.QVariant(
                          self.saveGeometry()))
        settings.setValue("MainWindow/State", QtCore.QVariant(
                          self.saveState()))
        self.save_sss()
        MThread(self.trackdb.save_db).start()
        # save_trackdb.start()
        # self.connect(test_th, QtCore.SIGNAL("finished()"), test_th.quit)
        # MThread(self.coverdb.save_db).start()
        # save_coverdb.start()
        # self.connect(test_th1, QtCore.SIGNAL("finished()"), test_th.quit)


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("BK Team")
    app.setOrganizationDomain("github.com/arshavindn/Miusik")
    app.setApplicationName("Miusik")
    miusik = Miusik()
    with open('miusik.qss') as qss_file:
        style = qss_file.read()
        miusik.setStyleSheet(style)
    miusik.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
