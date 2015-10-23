from PyQt4 import QtGui, QtCore
import sys
from src.metadata.mp3 import MP3Format

SONGS = ['D:\Drive E\Music\Arms - Christina Perri.mp3',
         'D:\Drive E\Music\Air Supply - All Out Of Love.mp3',
         'D:\Drive E\Music\Hoang Ton - Bai Hat Tang Em.mp3',
         'D:\Drive E\Music\M-TP - Con Mua Ngang Qua.mp3']
TAGS = ['Playing', 'Title', 'Album', 'Artist', 'Length']


def get_tags(uri):
    tags_pair = {}
    song = MP3Format(uri)
    tags_temp = song.read_all()
    for tag in TAGS:
        for key, value in tags_temp.iteritems():
            key_temp = key
            if '__' in key:
                key_temp = key[2:]
            if tag.lower() == key_temp:
                tags_pair[tag] = value
    return tags_pair


class Example(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Example, self).__init__(parent)
        self.table = QtGui.QTableWidget()
        # tags = ['Playing', 'Title', 'Album', 'Artist', 'Length']
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setMovable(True)
        self.table.horizontalHeader().setDragEnabled(True)
        self.table.horizontalHeader().setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setColumnCount(5)
        for index in range(len(TAGS)):
            item = QtGui.QTableWidgetItem(QtCore.QString(TAGS[index]))
            self.table.setHorizontalHeaderItem(index, item)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.table)
        self.setLayout(hbox)
        self.show()

    def set_row_content(self, row, uri):
        tags_pair = get_tags(uri)
        for col in range(self.table.columnCount()):
            for key, value in tags_pair.iteritems():
                if self.table.horizontalHeaderItem(col).text().__str__() == unicode(key):
                    string = ''
                    if type(value) is list:
                        string = ', '.join(value)
                    elif type(value) is float:
                        string = str(value)
                    # self.table.setCurrentCell(row, col)
                    # print self.table.currentRow(), self.table.currentColumn()
                    self.table.setItem(row, col, QtGui.QTableWidgetItem(QtCore.QString(string)))

    def set_content(self, songs):
        if self.table.rowCount() == 0:
            self.table.setRowCount(len(songs))
        else:
            self.table.insertRow(len(songs))
        print self.table.rowCount()
        curent_row = self.table.currentRow()
        for index in range(len(songs)):
            row = curent_row + index + 1
            self.set_row_content(row, songs[index])


def test_tag():
    print get_tags(SONGS[0])


def test():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.set_content(SONGS)
    sys.exit(app.exec_())
