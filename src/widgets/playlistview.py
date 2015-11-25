# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from src.metadata.tags import tag_data
from src.common import format_time


class PlaylistTable(QtGui.QTableWidget):
    __all_header = tuple(tag_data.keys())
    shown_header = ['title', 'album', 'artist', '__length']
    sort_items = QtCore.pyqtSignal(int)

    def __init__(self):
        super(PlaylistTable, self).__init__()
        self.setFrameShape(QtGui.QFrame.NoFrame)
        self.setFrameShadow(QtGui.QFrame.Sunken)
        self.setLineWidth(0)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.setShowGrid(True)
        self.setGridStyle(QtCore.Qt.SolidLine)
        self.setWordWrap(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setMovable(True)
        self.horizontalHeader().setDragEnabled(True)
        self.horizontalHeader().setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setRowCount(0)

        self.set_headers()
        # TODO: creat menu when right click on header,
        # so user can set show or hide some tag raw
        # header_right_menu
        # self.connect(self, QtCore.SIGNAL("sort_items(int)"), self.print_sorted_col)

    # def sortItems(self, column, order):
    #     super(self.__class__, self).sortItems(column, order)
    #     self.sort_items.emit(column)

    def print_sorted_col(self, col):
        print col

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

    def get_headertag_index(self, tag):
        """
            Get index of tag in __all_header.
            This index is also logical index in table header.
        """
        try:
            return self.__all_header.index(tag)
        except ValueError():
            return -1

    def show_column(self, header):
        """
            Show hidden column with given header.
        """
        pass

    def get_loc_list(self):
        """
            Get list of location of all tracks on table.
            It useful when the table is re-sorted.
        """
        loc_header_index = self.get_headertag_index("__loc")
        result = []
        for row in self.rowCount():
            result.append(unicode(self.item(row, loc_header_index).text()))
        return result

    def add_track(self, track):
        """
            Fill the info of a track to a row in table.
        """
        row = self.rowCount()  # current row, cause it counts from 0 :))
        self.setRowCount(self.rowCount() + 1)
        for tag_index in range(len(self.__all_header)):
            # !!!: 0 index is "Playing" header
            raw = self.__all_header[tag_index]
            if raw.startswith("__"):
                value = track.get_tag_raw(raw)
                if value == None:
                    value = u""
                if raw == "__length":
                    value = format_time(value)
            else:
                value = track.get_tag_raw(raw, True)
            item = QtGui.QTableWidgetItem(QtCore.QString(value))
            col = tag_index + 1
            self.setItem(row, col, item)


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
        self.__line_edit = None
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
        if self.__line_edit:
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
        if not self.__line_edit:  # K co tab nao dang rename
            self.__line_edit = TabNameLineEdit(self)
            self.__line_edit.show()
        else:  # Dang co rename mot tab nao do, va self.__line_edit da duoc tao
            self.__line_edit.clear()  # xoa text trong lineedit di
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
        self.__line_edit.deleteLater()
        self.__line_edit = None

    @QtCore.pyqtSlot()
    def cancel_rename(self):
        self.__line_edit.deleteLater()
        self.__line_edit = None
# end clss QTabBar


class CustomTabWidget(QtGui.QTabWidget):
    """Tab Widget that that can have new tabs easily added to it."""

    def __init__(self, parent=None):
        super(CustomTabWidget, self).__init__(parent)

        # Tab Bar
        # self.tab = QtGui.QTabBar()
        self.tab_bar = QTabBar()
        self.setTabBar(self.tab_bar)

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

    def addTab(self, tab_name):
        string = QtCore.QString.fromUtf8(tab_name)
        table = PlaylistTable()
        index = super(CustomTabWidget, self).addTab(table, string)
        self.setCurrentIndex(index)
        return index
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
