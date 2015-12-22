# -*- coding: utf-8 -*-

import gc, os
from time import sleep
import ConfigParser
from PyQt4 import QtGui, QtCore
from src.widgets.mainwindow import Ui_main_window
from src.widgets.playlistview import PlaylistTable, CellWidget
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
        time = self.kwargs.get('time')
        if time is not None:
            sleep(time)
            print "tada"
            del self.kwargs['time']
        self.func(*self.args, **self.kwargs)
# end class MThead

def run_in_thread(func):
    """
        Decoration for run thread.
    """
    def wrapped_f(*args, **kwargs):
        MThread(func, *args, **kwargs).start()

    return wrapped_f


# end class TrackContextMenu


class PlayerControler(QtCore.QThread):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        self.player = playerbin.Player()
        self.is_playing = False


# end class PlayerControler


class AddTracksThread(QtCore.QThread):
    def __init__(self, locs, trackdb, table):
        super(AddTracksThread, self).__init__()
        self.locs = locs
        self.trackdb = trackdb
        # self.coverdb = coverdb
        self.table = table
        self.table.setSortingEnabled(False)

    def run(self):
        for loc in self.locs:
            self.table.add_track(loc, self.trackdb)
            sleep(0.01)
        print "from add track threads", gc.collect()


class Miusik(QtGui.QMainWindow, Ui_main_window):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        settings = QtCore.QSettings()

        self.shuffle = "Off"
        self.repeat = "Off"
        self.trackdb_loc = common.get_appdata_dir() + "/tracks.db"
        # self.coverdb_loc = common.get_appdata_dir() + "/covers.db"
        self.trackdb = trackdb.TrackDB(self.trackdb_loc)
        # self.coverdb = coverdb.CoverDB(self.coverdb_loc)

        self.choose_next_timer = QtCore.QTimer()
        self.choose_next_timer.timeout.connect(self.next_btn_click)

        self.seek_slider_timer = QtCore.QTimer()
        self.seek_slider_timer.timeout.connect(self.seek_slider_move)

        self.play_controler = PlayerControler(self)
        self.play_controler.start()
        self.play_pause_button.clicked.connect(self.play_toggle)
        self.next_button.clicked.connect(self.next_btn_click)
        self.connect(self.volume_slider.slider, QtCore.SIGNAL("valueChanged(int)"),
                     self.volume_handle)
        self.connect(self.seek_slider, QtCore.SIGNAL("sliderMoved(int)"),
                     self.seeker_dragging)
        # self.app_info_button.clicked.connect(self.nah)

        # add files handler
        self.add_file_button.clicked.connect(self.open_files_callback)
        # add tab handler
        self.pl_tabs.plusButton.clicked.connect(self.add_tab_callback)
        self.connect(self.pl_tabs, QtCore.SIGNAL("tab_added(int)"), self.tab_added_handler)
        # test gc collect
        # self.app_info_button.clicked.connect(self.test_gc)
        # previous sesion
        PlaylistTable.save_header_state(state=settings.value("HeaderState").toByteArray())
        self.load_sss()
        self.set_menu_action(self.shuffle_button, self.shuffle_triggered, self.shuffle)
        self.set_menu_action(self.repeat_button, self.repeat_triggered, self.repeat)
        self.restoreGeometry(
                settings.value("MainWindow/Geometry").toByteArray())
        self.restoreState(settings.value("MainWindow/State").toByteArray())
        self.app_info_button.clicked.connect(self.show_about_dialog)
        # for tab_index in range(self.pl_tabs.count()):
        #     self.pl_tabs.widget(tab_index).horizontalHeader().restoreState(
        #         settings.value("HeaderState").toByteArray())
    # end __init__ method

    # def test_gc(self):
    #     print "test gc", gc.collect()

    # def nah(self):
    #     print self.pl_tabs.list_for_play

    def show_about_dialog(self):
        from src.widgets.about_dialog import Ui_Dialog
        Dialog = QtGui.QDialog(self)
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()

    def set_cover(self, trackobj):
        pixmap = QtGui.QPixmap()
        try:
            data = trackobj.get_tag_disk('cover')[0].data
            pixmap.loadFromData(data)
        except TypeError:
            pixmap.load(":/icons/default-cover.png")
        self.cover.setPixmap(pixmap)

    def track_menu_about_show(self):
        """
            Handle the aboutToShow signal of track context menu.
        """
        # TODO: Need more work here
        if self.pl_tabs.currentWidget().menu.loc == self.pl_tabs.current_song:
            self.pl_tabs.currentWidget().menu.actions()[0].setEnabled(False)  # play
        else:
            self.pl_tabs.currentWidget().menu.actions()[1].setEnabled(False)  # pause

    def track_right_click(self, action):
        """
            Handle the actions of track context menu when it triggered.
        """
        action_name = str(action.text())
        if action_name == "Play":
            self.play_song_handle(self.pl_tabs.currentWidget().menu.loc, self.pl_tabs.currentWidget().menu.row)
        elif action_name == "Pause":
            self.pause_handler()
        elif action_name == "Cut":
            pass
        elif action_name == "Copy":
            pass
        elif action_name == "Paste":
            pass
        elif action_name == "Remove from playlist":
            pass
        elif action_name == "Delete from disk":
            pass
        elif action_name == "Properties":
            pass

    def table_header_moved(self, logicalIndex, oldVisualIndex, newVisualIndex):
        if self.sender() == self.pl_tabs.currentWidget().horizontalHeader():
            # self.pl_tabs.currentWidget().save_header_state()
            PlaylistTable.save_header_state(self.pl_tabs.currentWidget())
            indexs = range(self.pl_tabs.currentIndex()) + \
                     range(self.pl_tabs.currentIndex()+1, self.pl_tabs.count())
            for index in indexs:
                self.pl_tabs.widget(index).horizontalHeader().moveSection(oldVisualIndex, newVisualIndex)

    def table_header_resized(self, logicalIndex, oldSize, newSize):
        if self.sender() == self.pl_tabs.currentWidget().horizontalHeader():
            # self.pl_tabs.currentWidget().save_header_state()
            PlaylistTable.save_header_state(self.pl_tabs.currentWidget())
            for index in range(self.pl_tabs.currentIndex()) + \
                         range(self.pl_tabs.currentIndex()+1, self.pl_tabs.count()):
                self.pl_tabs.widget(index).horizontalHeader().resizeSection(logicalIndex, newSize)

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

    def set_playing_state(self, trackobj, song_len=None):
        self.playing_song.setText(trackobj.get_tag_raw('title', True))
        self.artist.setText(trackobj.get_tag_raw('artist', True))
        self.set_cover(trackobj)
        self.position.setText("0:00")
        if not song_len:
            song_len = trackobj.get_tag_raw('__length')
        self.duration.setText(common.format_time(int(round(song_len))))
        self.seek_slider.setValue(0)

    def play_song_handle(self, song, row=None):
        self.play_controler.player.play_given_song(song)
        trackobj = self.trackdb.get_track_by_loc(song)
        current_song_len = trackobj.get_tag_raw('__length')
        self.choose_next_timer.start(current_song_len*1000 + 500)
        self.seek_slider.setRange(0, int(round(current_song_len)))
        self.seek_slider_timer.start(1000)
        self.set_playing_state(trackobj)
        self.pl_tabs.current_song = song
        self.pl_tabs.current_album = \
            self.pl_tabs.currentWidget().get_album_from_loc(song)
        try:
            table = self.pl_tabs.widget(self.pl_tabs.played_songs[-1][-1])
            old_row = table.locs_gui[self.pl_tabs.played_songs[-1][0]]
            table.removeCellWidget(old_row, 0)
        except (IndexError, KeyError):
            pass
        if not row:
            row = self.pl_tabs.get_current_playlist().locs_gui[song]
        self.pl_tabs.get_current_playlist().setCellWidget(row, 0, CellWidget(":/icons/play.png"))
        self.pl_tabs.get_current_playlist().scrollToItem(self.pl_tabs.get_current_playlist().item(row, 1), 0)
        self.pl_tabs.get_current_playlist().played_songs.append(song)
        self.pl_tabs.played_songs.append((song, self.pl_tabs.currentIndex()))

    def seek_slider_move(self):
        self.seek_slider.setValue(self.seek_slider.value() + self.seek_slider.singleStep())
        self.position.setText(common.format_time(self.seek_slider.value()))

    def seeker_dragging(self, pos):
        self.play_controler.player.seek(pos)
        self.choose_next_timer.start((self.seek_slider.maximum() - self.seek_slider.value())*1000)

    def row_double_click(self, row):
        loc_inx = self.pl_tabs.currentWidget().get_headertag_index("__loc")
        loc = unicode(self.pl_tabs.currentWidget().item(row, loc_inx).text())
        self.play_song_handle(loc, row)
        curr_index = self.pl_tabs.currentIndex()
        if self.pl_tabs.current_playlist_index != curr_index:
            self.pl_tabs.current_playlist_index = curr_index
        self.pl_tabs.get_list_for_play(self.repeat)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_pause_button.setIcon(icon)
        self.play_controler.is_playing = True

    def pause_handler(self):
        self.play_controler.player.pause()
        # icon.addPixmap(QtGui.QPixmap(":/icons/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.seek_slider_timer.stop()
        self.choose_next_timer.stop()
        self.play_controler.is_playing = False
        self.play_pause_button.setIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/play.png")))

    def play_toggle(self):
        state = self.play_controler.player.get_status()
        icon = QtGui.QIcon()
        self.play_controler.is_playing = True
        if state == playerbin.IS_PLAYING:
            self.pause_handler()
            return
        elif state == playerbin.NOT_PLAYING:
            self.play_song_handle(self.pl_tabs.current_song)
            icon.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        elif state == playerbin.PAUSED:
            self.play_controler.player.play()
            icon.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.seek_slider_timer.start()
            self.choose_next_timer.start()
        else:  # IS_DONE
            self.play_controler.player.stop()
            self.play_controler.player.play()
            icon.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_pause_button.setIcon(icon)

    def next_btn_click(self):
        self.pl_tabs.current_song = \
                    self.pl_tabs.choose_next_song(self.shuffle)
        if self.play_controler.is_playing:
            self.play_song_handle(self.pl_tabs.current_song)
        else:
            self.play_controler.player.stop()
            trackobj = self.trackdb.get_track_by_loc(self.pl_tabs.current_song)
            self.set_playing_state(trackobj)
            self.play_controler.player.set_file(self.pl_tabs.current_song)

    def set_menu_action(self, button, func, val):
        for act in button.menu().actions():
            act.triggered[()].connect(lambda xact=act: func(xact))
            if str(act.text()) == val:
                act.setChecked(True)

    def add_tab_callback(self):
        self.pl_tabs.addTab()
        # self.pl_tabs.tab_bar.start_rename(index)

    def tab_added_handler(self, index):
        self.connect(self.pl_tabs.currentWidget(), QtCore.SIGNAL("cellDoubleClicked(int,int)"),
                     self.row_double_click)
        self.connect(self.pl_tabs.currentWidget().horizontalHeader(),
                     QtCore.SIGNAL("sortIndicatorChanged(int, Qt::SortOrder)"),
                     lambda: QtCore.QTimer.singleShot(500, lambda: self.pl_tabs.get_list_for_play(self.repeat)))
        self.connect(self.pl_tabs.currentWidget().horizontalHeader(),
                     QtCore.SIGNAL("sectionMoved(int,int,int)"), self.table_header_moved)
        self.connect(self.pl_tabs.currentWidget().horizontalHeader(),
                     QtCore.SIGNAL("sectionResized(int,int,int)"), self.table_header_resized)
        self.connect(self.pl_tabs.currentWidget().menu, QtCore.SIGNAL("triggered(QAction*)"), self.track_right_click)
        self.connect(self.pl_tabs.currentWidget().menu, QtCore.SIGNAL("aboutToShow()"), self.track_menu_about_show)
        if index == self.pl_tabs.current_playlist_index:
            self.pl_tabs.setCurrentIndex(index)
            try:
                self.pl_tabs.current_album = \
                    self.pl_tabs.get_current_playlist().get_album_from_loc(
                        self.pl_tabs.current_song)
                self.pl_tabs.get_list_for_play(self.repeat)
            except AttributeError:
                if len(self.pl_tabs.get_current_playlist()) != 0:
                    self.update_things()

    def open_files_callback(self):
        locs = QtGui.QFileDialog().getOpenFileNames(parent=self, caption="Open Files",
                                                    directory='')
        locs = [unicode(f) for f in locs]
        current_index = self.pl_tabs.currentIndex()
        if current_index != -1 and locs:
            self.add_track_thread = AddTracksThread(locs, self.trackdb,
                                                    self.pl_tabs.currentWidget())
            self.add_track_thread.start()
            self.connect(self.add_track_thread, QtCore.SIGNAL("finished()"),
                         lambda index=current_index: self.thread_add_track_done(index))
        print "open file dialog", gc.collect()

    def thread_add_track_done(self, index):
        if not self.pl_tabs.current_song:
            self.pl_tabs.current_playlist_index = index
            self.update_things()
        self.pl_tabs.currentWidget().setSortingEnabled(True)
        self.add_track_thread.deleteLater()

    def update_things(self):
        self.pl_tabs.current_song = self.pl_tabs.get_current_playlist().get_loc_list_gui()[0]
        self.pl_tabs.current_album = \
            self.pl_tabs.get_current_playlist().get_album_from_loc(
                self.pl_tabs.current_song)
        self.pl_tabs.get_list_for_play(self.repeat, True)

    def shuffle_triggered(self, act):
        self.shuffle = str(act.text())
        # print self.shuffle, self.repeat

    def repeat_triggered(self, act):
        self.repeat = str(act.text())
        # print self.shuffle, self.repeat
        self.pl_tabs.get_list_for_play(self.repeat)

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
            self.pl_tabs.current_playlist_index = int(sss.get('session', 'current playlist index'))
            if self.pl_tabs.current_playlist_index != -1:
                self.pl_tabs.current_song = sss.get('session', 'current song').decode("utf-8")
                self.pl_tabs.load_previous_session(
                    common.get_appdata_dir() + "/playlists.mpk", self.trackdb)

    def save_sss(self, loc=None):
        if not loc:
            loc = os.getcwd() + '/settings.ini'

        sss = ConfigParser.ConfigParser()
        sss.read(loc)
        sss.set('session', 'shuffle', self.shuffle)
        sss.set('session', 'repeat', self.repeat)
        sss.set('session', 'volume', self.play_controler.player.get_volume())
        loc_for_save = self.pl_tabs.current_song.encode("utf-8")
        print loc_for_save
        sss.set('session', 'current song', loc_for_save)
        sss.set('session', 'current playlist index', self.pl_tabs.current_playlist_index)
        with open(loc, 'w') as configfile:
                sss.write(configfile)

    def closeEvent(self, event):
        self.pl_tabs.save_session(common.get_appdata_dir() + "/playlists.mpk")
        settings = QtCore.QSettings()
        settings.setValue("MainWindow/Geometry", QtCore.QVariant(
                          self.saveGeometry()))
        settings.setValue("MainWindow/State", QtCore.QVariant(
                          self.saveState()))
        settings.setValue("HeaderState", QtCore.QVariant(
                          self.pl_tabs.currentWidget().horizontalHeader().saveState()))
        self.save_sss()
        MThread(self.trackdb.save_db).start()
        # save_trackdb.start()
        # self.connect(test_th, QtCore.SIGNAL("finished()"), test_th.quit)
        # MThread(self.coverdb.save_db).start()
        # save_coverdb.start()
        # self.connect(test_th1, QtCore.SIGNAL("finished()"), test_th.quit)


def main():
    import sys
    from gi.repository import GObject
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("BK Team")
    app.setOrganizationDomain("github.com/arshavindn/Miusik")
    app.setApplicationName("Miusik")
    miusik = Miusik()
    miusik.setWindowTitle("Miusik")
    # miusik.setWindowIcon(":/icons/miusik.png")
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/icons/miusik.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    miusik.setWindowIcon(icon)
    with open('miusik.qss') as qss_file:
        style = qss_file.read()
        miusik.setStyleSheet(style)
    GObject.threads_init()
    miusik.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
