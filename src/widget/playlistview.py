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


class TabBarPlus(QtGui.QTabBar):
    """Tab bar that has a plus button floating to the right of the tabs."""

    # plusClicked = QtCore.Signal()

    def __init__(self):
        super(TabBarPlus, self).__init__()

        # Plus Button
        self.plusButton = QtGui.QPushButton("+")
        self.plusButton.setParent(self)
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
        return QtCore.QSize(width+25, height)
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
        self.tab = QtGui.QTabBar()
        # self.tab = TabBarPlus()
        self.setTabBar(self.tab)

        # Properties
        self.setMovable(True)
        self.setTabsClosable(True)

        self.plusButton = QtGui.QToolButton(self.tab)
        self.plusButton.setText("+")
        # self.plusButton.setMaximumSize(20, 20) # Small Fixed size
        self.plusButton.setMinimumSize(24, 24)
        # self.plusButton.setGeometry(0, 0, 30, 22)
        self.setCornerWidget(self.plusButton)

        # Signals
        self.connect(self.plusButton, QtCore.SIGNAL('clicked()'), self.addTab)
        # self.tab.plusClicked.connect(self.addTab)
        self.tab.tabMoved.connect(self.tab.moveTab)
        self.tabCloseRequested.connect(self.removeTab)

    def addTab(self):
        string = QtCore.QString.fromUtf8("Playlist")
        tab = PlaylistTable()
        super(CustomTabWidget, self).addTab(tab, string)
        # self.tab.movePlusButton
        sizeHint = self.plusButton.sizeHint()
        width = sizeHint.width()
        height = sizeHint.height()
        print (width, height)
        # plusButton_geo = self.plusButton.geometry()
        # print plusButton_geo

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
        # self.playlist_manager.addTab()
        self.setCentralWidget(self.centralwidget)

        self.show()
# end class AppDemo


def main():
    import sys
    app = QtGui.QApplication(sys.argv)

    w = AppDemo()
    w.setWindowTitle('AppDemo')
    style = open('style.qss').read()
    w.setStyleSheet(style)
    w.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
