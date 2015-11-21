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

    def __init__(self, parent=None):
        super(QTabBar, self).__init__(parent)

    tabDoubleClicked = QtCore.pyqtSignal(int)

    def mouseDoubleClickEvent(self, event):
        tab_index = self.tabAt(event.pos())
        self.tabDoubleClicked.emit(tab_index)
        self.start_rename(tab_index)

    def start_rename(self, tab_index):
        self.__edited_tab = tab_index
        rect = self.tabRect(tab_index)
        top_margin = 3
        left_margin = 6
        self.__edit = TabNameLineEdit(self)
        self.__edit.show()
        print self.__edit
        self.__edit.move(rect.left() + left_margin, rect.top() + top_margin)
        self.__edit.resize(rect.width() - 2 * left_margin, rect.height() - 2 * top_margin)
        self.__edit.setText(self.tabText(tab_index))
        self.__edit.selectAll()
        self.__edit.setFocus()
        self.__edit.editingFinished.connect(self.finish_rename)
        self.__edit.cancelingFinished.connect(self.cancel_rename)

    @QtCore.pyqtSlot()
    def finish_rename(self):
        self.__edit = self.sender()
        self.setTabText(self.__edited_tab, self.__edit.text())
        self.__edit.deleteLater()
        # print self.__edit

    @QtCore.pyqtSlot()
    def cancel_rename(self):
        self.__edit = self.sender()
        self.__edit.deleteLater()


class TabBarPlus(QtGui.QTabBar):
    """Tab bar that has a plus button floating to the right of the tabs."""

    # plusClicked = QtCore.Signal()

    def __init__(self):
        super(TabBarPlus, self).__init__()

        # Plus Button
        self.plusButton = QtGui.QToolButton(self)
        self.plusButton.setText("+")
        self.plusButton.setMaximumSize(20, 20) # Small Fixed size
        self.plusButton.setMinimumSize(20, 20) # Small Fixed size
        # self.plusButton.clicked.connect(self.plusClicked.emit)
        self.movePlusButton() # Move to the correct location
    # end Constructor

    def sizeHint(self):
        """Return the size of the TabBar with increased width for the plus button."""
        sizeHint = QtGui.QTabBar.sizeHint(self)
        width = sizeHint.width()
        height = sizeHint.height()
        return QtCore.QSize(width+25, height+10)
    # end tabSizeHint

    def resizeEvent(self, event):
        """Resize the widget and make sure the plus button is in the correct location."""
        super(TabBarPlus, self).resizeEvent(event)

        self.movePlusButton()
    # end resizeEvent

    def tabLayoutChange(self):
        """This virtual handler is called whenever the tab layout changes.
        If anything changes make sure the plus button is in the correct location.
        """
        super(TabBarPlus, self).tabLayoutChange()

        self.movePlusButton()
    # end tabLayoutChange

    def movePlusButton(self):
        """Move the plus button to the correct location."""
        # Find the width of all of the tabs
        size = 0
        for i in range(self.count()):
            size += self.tabRect(i).width()

        # Set the plus button location in a visible area
        h = self.geometry().top()
        w = self.width()
        if size > w: # Show just to the left of the scroll buttons
            self.plusButton.move(w-54, h)
        else:
            self.plusButton.move(size, h)
    # end movePlusButton
# end class MyClass


class CustomTabWidget(QtGui.QTabWidget):
    """Tab Widget that that can have new tabs easily added to it."""

    def __init__(self, parent=None):
        super(CustomTabWidget, self).__init__(parent)
        # QtGui.QTabWidget.__init__(self, parent)

        # Tab Bar
        # self.tab = QtGui.QTabBar()
        self.tab = QTabBar()
        self.setTabBar(self.tab)

        # Properties
        self.setMovable(True)
        self.setTabsClosable(True)

        self.plusButton = QtGui.QToolButton(self.tab)
        self.plusButton.setText("+")
        self.plusButton.setMaximumSize(20, 20) # Small Fixed size
        self.plusButton.setMinimumSize(20, 20)
        self.setCornerWidget(self.plusButton)

        # Signals
        # self.connect(self.plusButton, QtCore.SIGNAL('clicked()'),
        #             lambda tab_name="Playlist": self.addTab(tab_name))
        # self.tab.plusClicked.connect(self.addTab)
        self.tab.tabMoved.connect(self.tab.moveTab)
        self.tabCloseRequested.connect(self.removeTab)
        self.tabBar().tabDoubleClicked.connect(self.tabBarDoubleClicked)

    tabBarDoubleClicked = QtCore.pyqtSignal(int)

    def addTab(self, tab_name):
        string = QtCore.QString.fromUtf8(tab_name)
        tab = PlaylistTable()
        index = super(CustomTabWidget, self).addTab(tab, string)
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
