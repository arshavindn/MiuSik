from PyQt4 import QtGui
from src.widgets.playlistview import AppDemo

def main_appdemo():
    import sys
    app = QtGui.QApplication(sys.argv)

    w = AppDemo()
    w.setWindowTitle('AppDemo')
    # style = open('style.qss').read()
    # w.setStyleSheet(style)
    w.show()

    sys.exit(app.exec_())
