from PyQt4 import QtGui, QtCore


class TabBarPlus(QtGui.QTabBar):
    """Tab bar that has a plus button floating to the right of the tabs."""

    #plusClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(TabBarPlus, self).__init__(parent)

        # Plus Button
        self.plusButton = QtGui.QToolButton()
        plusButtonIcon = QtGui.QIcon()
        plusButtonIcon.addPixmap(QtGui.QPixmap("D:/Cloud/Dropbox/Programming/Code/py/Music_App/Icons/TabBar/add_tab.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.plusButton.setIcon(plusButtonIcon)
        self.plusButton.setIconSize(QtCore.QSize(22, 22))
        self.plusButton.setParent(self)
        self.plusButton.setMaximumSize(20, 20)  # Small Fixed size
        self.plusButton.setMinimumSize(20, 20)  # Small Fixed size
        #self.plusButton.clicked.connect(self.plusClicked.emit)
        self.movePlusButton()  # Move to the correct location
    # end Constructor

    def sizeHint(self):
        """Return the size of the TabBar with increased width for the plus button."""
        sizeHint = QtGui.QTabBar.sizeHint(self)
        width = sizeHint.width()
        height = sizeHint.height()
        return QtCore.QSize(width + 25, height)
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
        if size > w:  # Show just to the left of the scroll buttons
            self.plusButton.move(w + 54, h)
        else:
            self.plusButton.move(size, h)
    # end movePlusButton
# end class TabBarPlus


class CustomTabWidget(QtGui.QTabWidget):
    """Tab Widget that that can have new tabs easily added to it."""

    def __init__(self, parent=None):
        super(CustomTabWidget, self).__init__(parent)
        # QtGui.QTabWidget.__init__(self, parent)

        # Tab Bar
        self.tab = QtGui.QTabBar()
        #self.tab = TabBarPlus()
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
        tab = QtGui.QWidget()
        super(CustomTabWidget, self).addTab(tab, string)
    # end Constructor
# end class CustomTabWidget


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
