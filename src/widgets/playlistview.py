# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from src.metadata.tags import tag_data


class PlaylistTable(QtGui.QTableWidget):
    all_header = tag_data.keys()
    shown_header = ['title', 'album', 'artist', '__length']

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
        self.setRowCount(0)
        self.set_headers()

    def set_headers(self):
        self.setColumnCount(len(self.all_header) + 1)
        for col in range(self.columnCount()):
            if col == 0:
                self.setHorizontalHeaderItem(col, QtGui.QTableWidgetItem(QtCore.QString('Playing')))
            else:
                if tag_data.get(self.all_header[col-1]):
                    item = QtGui.QTableWidgetItem(QtCore.QString(tag_data[self.all_header[col-1]].name))
                    self.setHorizontalHeaderItem(col, item)
                if self.all_header[col-1] not in self.shown_header:
                    self.hideColumn(col)

    def show_column(self, header):
        """
            Show hidden column with given header.
        """
        pass


class TabNameLineEdit(QtGui.QLineEdit):
    editingFinished = QtCore.pyqtSignal()
    cancelingFinished = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(TabNameLineEdit, self).__init__(parent)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return:  # lol, Key_Return means press Enter
            self.editingFinished.emit()
        elif e.key() == QtCore.Qt.Key_Escape:
            self.cancelingFinished.emit()
        super(TabNameLineEdit, self).keyPressEvent(e)


class QTabBar(QtGui.QTabBar):
    """QTabBar with double click signal and tab rename behavior."""
    tabDoubleClicked = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(QTabBar, self).__init__(parent)
        self.__line_edit = None
        self.connect(self, QtCore.SIGNAL("currentChanged(int)"), self.current_changed_hdler)
        self.connect(self, QtCore.SIGNAL("tabMoved(int, int)"), self.tab_moved_hdler)
        self.connect(self, QtCore.SIGNAL("tabCloseRequested(int)"), self.tab_close_requested_hdler)

    def current_changed_hdler(self, index):
        print "from current_changed_hdler %d\n" %(index)

    def tab_moved_hdler(self, des, tar):
        """
            @des: means "to", move to index
            @tar: means "from"
        """
        print "from tab_moved_hdler: move tab index %d, to index %d\n" %(tar, des)
        if self.__edited_tab == tar:
            self.__line_edit.raise_()
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
        # FIXME: nah, khong the lay dung index cua edited_tab
        # khi tabbar co thay doi nhu move hay close 1 tab nao do
        if self.__line_edit:
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
        self.__line_edit.resize(rect.width() - 2 * left_margin, rect.height() - 2 * top_margin)
        self.__line_edit.setText(self.tabText(tab_index))
        self.__line_edit.selectAll()
        self.__line_edit.setFocus()
        self.__line_edit.editingFinished.connect(self.finish_rename)
        self.__line_edit.cancelingFinished.connect(self.cancel_rename)

    @QtCore.pyqtSlot()
    def finish_rename(self):
        if len(self.__line_edit.text()) != 0:
            print "nah"
            self.setTabText(self.__edited_tab, self.__line_edit.text())
        self.__line_edit.deleteLater()
        self.__line_edit = None

    @QtCore.pyqtSlot()
    def cancel_rename(self):
        print "wtf"
        self.__line_edit.deleteLater()
        self.__line_edit = None


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
