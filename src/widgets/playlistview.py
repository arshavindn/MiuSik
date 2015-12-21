# -*- coding: utf-8 -*-

import gzip
from random import randrange
try:
    import cPickle as pickle
except ImportError:
    import pickle
from PyQt4 import QtGui, QtCore
from src.metadata.tags import tag_data
from src.common import format_time
from src.playlist import Playlist


class CellWidget(QtGui.QWidget):
    def __init__(self, icon, parent=None):
        super(CellWidget, self).__init__(parent)
        self.label = QtGui.QLabel()
        self.label.setMaximumSize(12, 12)
        self.label.setScaledContents(True)
        self.label.setPixmap(QtGui.QPixmap(icon))
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(self.label)
        hbox.setAlignment(QtCore.Qt.AlignCenter)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)

class TrackContextMenu(QtGui.QMenu):
    def __init__(self, parent):
        super(TrackContextMenu, self).__init__(parent)
        action_names = ("Play", "Pause", None, "Cut", "Copy", "Paste", None,
                        "Remove from playlist", "Delete from disk", None, "Properties")
        for action in action_names:
            if action is None:
                self.addSeparator()
            else:
                self.addAction(action)
        self.loc = None
        self.row = None


class PlaylistTable(QtGui.QTableWidget, Playlist):
    __all_header = tuple(tag_data.keys())
    shown_header = ['title', 'album', 'artist', '__length']
    __horiz_header_state = None

    context_menu_triggered = QtCore.pyqtSignal(QtCore.QString, int, QtCore.QString)

    # def __new__(cls, *args, **kwargs):
    #     pass
    @staticmethod
    def save_header_state(instance=None, state=None):
        if state:
            PlaylistTable.__horiz_header_state = state
        elif isinstance(instance, PlaylistTable):
            PlaylistTable.__horiz_header_state = instance.horizontalHeader().saveState()
        else:
            return False
        return True

    def __init__(self, name, parent=None):
        QtGui.QTableWidget.__init__(self, parent)
        Playlist.__init__(self, name)
        self.setFrameShape(QtGui.QFrame.NoFrame)
        # self.setFrameShadow(QtGui.QFrame.Sunken)
        # self.setLineWidth(0)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.setShowGrid(False)
        self.setWordWrap(False)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.verticalHeader().setDefaultSectionSize(24)
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setRowCount(0)
        self.setAutoScroll(True)
        self.set_headers()
        if PlaylistTable.__horiz_header_state is None:
            self.horizontalHeader().setMovable(True)
            self.horizontalHeader().setDragEnabled(True)
            self.horizontalHeader().setDragDropMode(QtGui.QAbstractItemView.InternalMove)
            PlaylistTable.__horiz_header_state = self.horizontalHeader().saveState()
        else:
            horiz_header = QtGui.QHeaderView(QtCore.Qt.Horizontal)
            horiz_header.restoreState(PlaylistTable.__horiz_header_state)
            self.setHorizontalHeader(horiz_header)

        self.menu = TrackContextMenu(self)
        # TODO: creat menu when right click on header,
        # so user can set show or hide some tag raw
        # header_right_menu

    def set_headers(self):
        self.setColumnCount(len(self.__all_header) + 1)
        for col in range(self.columnCount()):
            if col == 0:
                self.setHorizontalHeaderItem(col, QtGui.QTableWidgetItem(QtCore.QString('Playing')))
            else:
                if tag_data.get(self.__all_header[col-1]):
                    item = QtGui.QTableWidgetItem(QtCore.QString(tag_data[self.__all_header[col-1]].name))
                    self.setHorizontalHeaderItem(col, item)
                if self.__all_header[col-1] not in self.shown_header:
                    self.hideColumn(col)

    def contextMenuEvent(self, event):
        # add other required actions
        self.menu.popup(QtGui.QCursor.pos())
        header_height = self.horizontalHeader().size().height()
        self.menu.row = self.rowAt(self.mapFromGlobal(QtGui.QCursor.pos()).y() - header_height)
        try:
            self.menu.loc = self.get_tag_in_row("__loc", self.menu.row)
        except AttributeError:
            pass

        self.menu.popup(QtGui.QCursor.pos())

    def get_headertag_index(self, tag):
        """
            Get index of tag in __all_header.
            This index is also logical index in table header.
        """
        try:
            return self.__all_header.index(tag) + 1
        except ValueError():
            return -1

    def get_tag_in_row(self, tag, row):
        """
            Get the tag's value in specific row.
            If not, return None.
        """
        col = self.get_headertag_index(tag)
        if col != -1:
            return unicode(self.item(row, col).text())
        else:
            return None

    def show_column(self, header):
        """
            Show hidden column with given header.
        """
        pass

    def get_loc_list_gui(self):
        """
            Get list of locations of all tracks on table.
            It's useful when the table is re-sorted.
        """
        loc_header_index = self.get_headertag_index("__loc")
        self.locs_gui.clear()
        for row in range(self.rowCount()):
            self.locs_gui[unicode(self.item(row, loc_header_index).text())] = row
            # yield unicode(self.item(row, loc_header_index).text())
        return self.locs_gui.keys()

    def add_track(self, loc, trackdb):
        """
            Fill the info of a track to a row in table.
        """
        track = Playlist.add_track(self, loc, trackdb)
        if track:
            self.fill_row(track)

    def fill_row(self, trackobj):
        row = self.rowCount()  # current row, cause it counts from 0 :))
        self.setRowCount(self.rowCount() + 1)
        for tag_index in range(len(self.__all_header)):
            # !!!: 0 index is "Playing" header
            raw = self.__all_header[tag_index]
            if raw.startswith("__"):
                value = trackobj.get_tag_raw(raw)
                if value == None:
                    value = u""
                if raw == "__length":
                    value = format_time(value)
            else:
                value = trackobj.get_tag_raw(raw, True)
            item = QtGui.QTableWidgetItem(QtCore.QString(value))
            col = tag_index + 1
            self.setItem(row, col, item)

    def del_row(self, row):
        pass


class TabNameLineEdit(QtGui.QLineEdit):
    editingFinished = QtCore.pyqtSignal(QtCore.QString)
    cancelingFinished = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(TabNameLineEdit, self).__init__(parent)
        # self.setMouseTracking(True)

    def focusOutEvent(self, event):
        self.cancelingFinished.emit()
        super(TabNameLineEdit, self).focusOutEvent(event)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return:  # lol, Key_Return means press Enter
            self.editingFinished.emit(self.text())
        elif e.key() == QtCore.Qt.Key_Escape:
            self.cancelingFinished.emit()
        super(TabNameLineEdit, self).keyPressEvent(e)
# end class TabNameLineEdit


class QTabBar(QtGui.QTabBar):
    """QTabBar with double click signal and tab rename behavior."""
    tabDoubleClicked = QtCore.pyqtSignal(int)
    finishedRename = QtCore.pyqtSignal(int, QtCore.QString)

    def __init__(self, parent=None):
        super(QTabBar, self).__init__(parent)
        self.__edited_tab = -1
        self.connect(self, QtCore.SIGNAL("currentChanged(int)"), self.current_changed_hdler)
        self.connect(self, QtCore.SIGNAL("tabMoved(int, int)"), self.tab_moved_hdler)
        self.connect(self, QtCore.SIGNAL("tabCloseRequested(int)"), self.tab_close_requested_hdler)

    def current_changed_hdler(self, index):
        """
            Signal emit and give index of choosed tab.
        """
        # print "from current_changed_hdler %d\n" %(index)

    def tab_moved_hdler(self, des, tar):
        """
            @des: means "to", move to index
            @tar: means "from"
        """
        print "from tab_moved_hdler: move tab index %d, to index %d\n" %(tar, des)
        if self.__edited_tab == tar:
            self.__edited_tab = des
        else:
            if des > tar:  # move forward to backward, dich tab tu truoc ra sau
                if self.__edited_tab in range(tar+1, des+1):
                    self.__edited_tab -= 1
            else:  # move backward to forward, dich tu sau ra truoc
                if self.__edited_tab in range(des, tar+1):
                    self.__edited_tab += 1

    def tab_close_requested_hdler(self, index):
        print "from tab_close_requested_hdler %d\n" %(index)
        if self.__edited_tab > index:
            self.__edited_tab -= 1

    def mouseDoubleClickEvent(self, event):
        tab_index = self.tabAt(event.pos())
        self.tabDoubleClicked.emit(tab_index)
        self.start_rename(tab_index)

    def tabLayoutChange(self):
        super(self.__class__, self).tabLayoutChange()
        if self.__edited_tab != -1:
            self.__line_edit.raise_()
            top_margin = 3
            left_margin = 6
            rect = self.tabRect(self.__edited_tab)
            self.__line_edit.move(rect.left() + left_margin, rect.top() + top_margin)
            self.__line_edit.resize(rect.width() - 2 * left_margin, rect.height() - 2 * top_margin)

    def start_rename(self, tab_index):
        self.__edited_tab = tab_index
        top_margin = 3
        left_margin = 6
        rect = self.tabRect(tab_index)
        try:  # Dang co rename mot tab nao do, va self.__line_edit da duoc tao
            self.__line_edit.clear()  # xoa text trong lineedit di
        except (AttributeError, RuntimeError):
            self.__line_edit = TabNameLineEdit(self)
            self.__line_edit.show()
        # di chuyen line_edit den tab can rename
        self.__line_edit.move(rect.left() + left_margin, rect.top() + top_margin)
        self.__line_edit.resize(rect.width() - 2 * left_margin,
                                rect.height() - 2 * top_margin)
        self.__line_edit.setText(self.tabText(tab_index))
        self.__line_edit.selectAll()
        self.__line_edit.setFocus()
        self.connect(self.__line_edit, QtCore.SIGNAL("editingFinished(QString)"),
                     self.finish_rename)
        self.__line_edit.cancelingFinished.connect(self.cancel_rename)
    # end mothod start_rename

    @QtCore.pyqtSlot()
    def finish_rename(self, qname):
        if len(self.__line_edit.text()) != 0:
            self.setTabText(self.__edited_tab, qname)
            self.finishedRename.emit(self.__edited_tab, qname)
        self.__edited_tab = -1
        self.__line_edit.deleteLater()

    @QtCore.pyqtSlot()
    def cancel_rename(self):
        self.__edited_tab = -1
        self.__line_edit.deleteLater()

# end clss QTabBar


class CustomTabWidget(QtGui.QTabWidget):
    """Tab Widget that that can have new tabs easily added to it."""
    tab_added = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(CustomTabWidget, self).__init__(parent)
        ################
        # For managering
        ################
        # The right current playlist is a playlist that has a track is playing,
        # if no track is playling, current playlist
        # will be current tab (that contains a playlist).
        # TODO: so, how to set current_playlist satifying this condition.
        self.current_playlist_index = -1
        self.current_song = None  # a tuple of row in table and location of current song.
        self.current_album = None  # Album obj of current album.
        self.played_songs = []  # tuple of row, song, index

        # Tab Bar
        # self.tab = QtGui.QTabBar()
        self.tab_bar = QTabBar()
        self.setTabBar(self.tab_bar)
        self.tables = set([])

        # Properties
        self.setMovable(True)
        self.setTabsClosable(True)

        self.plusButton = QtGui.QToolButton(self.tab_bar)
        self.plusButton.setText("+")
        self.plusButton.setMaximumSize(20, 20) # Small Fixed size
        self.plusButton.setMinimumSize(20, 20)
        self.setCornerWidget(self.plusButton)

        # Signals and slots
        self.tabCloseRequested.connect(self.removeTab)
        self.connect(self.tab_bar, QtCore.SIGNAL("finishedRename(int, QString)"),
                     self.rename_playlist)
        # self.connect(self, QtCore.SIGNAL("tabCloseRequested(int)"), self.del_tab_handler)

    def del_tab_handler(self, inx):
        # self.tab_bar.
        pass

    def get_current_playlist(self):
        return self.widget(self.current_playlist_index)

    def addTab(self, table=None):
        if not table:
            pl_name = QtCore.QString("Playlist " + str(self.get_playlist_num()+1))
            table = PlaylistTable(pl_name)
        else:
            pl_name = table.get_name()
        self.tables.add(table)
        index = super(CustomTabWidget, self).addTab(table, pl_name)
        self.setCurrentIndex(index)
        self.tab_added.emit(index)
        return index

    def rename_playlist(self, int, qname):
        """
            Method called when finish rename.
        """
        name = unicode(qname)
        self.widget(int).rename(name)
        # print self.widget(int).get_name()

    def get_playlist_num(self):
        """
            Get number of playlists.
        """
        return self.count()

    def get_list_for_play(self, repeat, use_locs_gui=False):
        """
            Get a list contains song from which can choose the next song.
            If repeat off or playlist, return whole current playlist,
            if repeat is song, return a list has only current song,
            if repeat is album, return a list that is album of current song.
        """
        # nah = list(self.get_current_playlist().get_loc_list_gui())
        # print
        # for i in nah:
        #     print i
        if self.current_playlist_index != -1:
            get_lst = lambda: self.get_current_playlist().locs_gui.keys() if use_locs_gui \
                              else self.get_current_playlist().get_loc_list_gui()
            if repeat == "Off" or repeat == "Playlist":
                self.list_for_play = get_lst()  # self.get_current_playlist().get_loc_list_gui()
            elif repeat == "Song":
                self.list_for_play = [self.current_song]
            elif repeat == "Album":
                cr_album_tracks = self.current_album.get_songs()
                self.list_for_play = [loc for loc in get_lst()
                                      if loc in cr_album_tracks]
        else:
            self.list_for_play = []
        # print self.list_for_play

    def choose_next_song(self, shuffle):
        """
            Chosse next song for playing.
        """
        # We have para track list because when shuffle, repeat change,
        # the playing list is being play will change or when user sorts the playlist table.
        if shuffle == "Off":
            try:
                self.current_song = self.list_for_play[self.list_for_play.index(self.current_song) + 1]
            except (ValueError, IndexError):
                self.current_song = self.list_for_play[0]
        else:
            self.current_song = self.list_for_play[randrange(len(self.list_for_play))]
        return self.current_song

    def load_previous_session(self, loc, trackdb):
        try:
            with gzip.open(loc, "rb") as f:
                while True:
                    try:
                        data = pickle.load(f)
                        table = PlaylistTable(data[0])
                        table.load_data(data[:3])
                        table.setSortingEnabled(False)
                        for loc in data[-1]:
                            track = trackdb.get_track_by_loc(loc)
                            if track is None:
                                table.add_track(loc, trackdb)
                            else:
                                table.fill_row(track)
                        self.addTab(table)
                        table.setSortingEnabled(True)
                    except EOFError:
                        break  # break when end of pickle file
        except IOError:
            pass

    def save_session(self, loc):
        with gzip.open(loc, "w+b") as f:
            for index in range(self.get_playlist_num()):
                playlist = self.widget(index)
                data = (playlist.get_name(), playlist.get_albums_dict(),
                        playlist.get_total_duration(), list(playlist.get_loc_list_gui()))
                pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

# end class CustomTabWidget

class AppDemo(QtGui.QMainWindow):
    def __init__(self):
        super(AppDemo, self).__init__()
        self.centralwidget = QtGui.QWidget(self)
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)

        self.playlist_manager = CustomTabWidget(self.centralwidget)
        # self.playlist_manager = QtGui.QTabWidget(self.centralwidget)
        self.horizontalLayout.addWidget(self.playlist_manager)

        self.playlist_manager.addTab()
        self.setCentralWidget(self.centralwidget)

        self.show()
# end class AppDemo
