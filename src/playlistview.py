from PyQt4 import QtGui, QtCore


class PlaylistTable(QtGui.QWidget):
    def __init__(self):
        super(PlaylistTable, self).__init__()
        self.playlistTable = QtGui.QTableWidget(self)
        self.playlistTable.setFrameShape(QtGui.QFrame.NoFrame)
        self.playlistTable.setFrameShadow(QtGui.QFrame.Sunken)
        self.playlistTable.setLineWidth(0)
        self.playlistTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.playlistTable.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.playlistTable.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.playlistTable.setShowGrid(True)
        self.playlistTable.setGridStyle(QtCore.Qt.SolidLine)
        self.playlistTable.setWordWrap(True)
        self.playlistTable.setCornerButtonEnabled(True)
        self.playlistTable.verticalHeader().setVisible(False)


class CustomTabWidget(QtGui.QTabWidget):
    """Tab Widget that that can have new tabs easily added to it."""

    def __init__(self, parent=None):
        super(CustomTabWidget, self).__init__(parent)
        # QtGui.QTabWidget.__init__(self, parent)

        # Tab Bar
        self.tab = QtGui.QTabBar()
        self.setTabBar(self.tab)

        # Properties
        self.setMovable(True)
        self.setTabsClosable(True)

        self.plusButton = QtGui.QPushButton("+")
        #corner = QtCore.Qt.TopRightCorner
        self.setCornerWidget(self.plusButton)

        # Signals
        self.connect(self.plusButton, QtCore.SIGNAL('clicked()'), self.addTab)
        #self.tab.plusClicked.connect(self.addTab)
        self.tab.tabMoved.connect(self.tab.moveTab)
        self.tabCloseRequested.connect(self.removeTab)

    def addTab(self):
        string = QtCore.QString.fromUtf8("Playlist")
        tab = PlaylistTable()
        super(CustomTabWidget, self).addTab(tab, string)


class AppDemo(QtGui.QMainWindow):
    def __init__(self):
        super(AppDemo, self).__init__()
        self.centralwidget = QtGui.QWidget(self)
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)

        self.playlist_manager = CustomTabWidget(self.centralwidget)
        #self.tabbar = TabBarPlus(self.centralwidget)

        self.horizontalLayout.addWidget(self.playlist_manager)
        #self.horizontalLayout.addWidget(self.tabbar)
        #string = QtCore.QString('Ha')
        #self.tabbar.addTab(string)

        self.playlist_manager.addTab()
        self.setCentralWidget(self.centralwidget)

        self.show()
# end class AppDemo


def main():
    import sys
    app = QtGui.QApplication(sys.argv)

    w = AppDemo()
    w.setWindowTitle('AppDemo')
    w.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
