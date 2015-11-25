from PyQt4 import QtGui, QtCore
import sys
import os
from src.metadata.mp3 import MP3Format
from src.metadata.tags import tag_data
from src import common

SONGS = ['D:\Drive E\Music\Arms - Christina Perri.mp3',
         'D:\Drive E\Music\Air Supply - All Out Of Love.mp3',
         'D:\Drive E\Music\Hoang Ton - Bai Hat Tang Em.mp3',
         'D:\Drive E\Music\M-TP - Con Mua Ngang Qua.mp3']
TAGS = ['Playing', 'Title', 'Album', 'Artist', 'Length']
type_format = []



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

class CustomTable(QtGui.QTableWidget):
    sort_items = QtCore.pyqtSignal(int, QtCore.Qt.SortOrder)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.connect(self, QtCore.SIGNAL("sort_items(int)"), self.print_sorted_col)
        # self.connect(self.horizontalHeader(),
        #              QtCore.SIGNAL("sortIndicatorChanged(int, Qt::SortOrder)"),
        #              self.print_sorted_col)
        self.setSortingEnabled(True)

    def sortItems(self, col, order):
        super(self.__class__, self).sortItems(col, order)
        self.sort_items.emit(col)

    def print_sorted_col(self, col, order):
        print col, order

class Example(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Example, self).__init__(parent)
        self.table = CustomTable()
        self.table.setSortingEnabled(True)
        # Enable dragging horizontal header
        self.table.horizontalHeader().setMovable(True)
        self.table.horizontalHeader().setDragEnabled(True)
        self.table.horizontalHeader().setDragDropMode(QtGui.QAbstractItemView.InternalMove)

        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setColumnCount(5)
        for index in range(len(TAGS)):
            item = QtGui.QTableWidgetItem(QtCore.QString(TAGS[index]))
            self.table.setHorizontalHeaderItem(index, item)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.table)

        self.print_tags_button = QtGui.QPushButton("Print tags")
        self.print_tags_button.clicked.connect(self.print_tags)
        vbox.addWidget(self.print_tags_button)

        self.setLayout(vbox)
        qss_file = open('D:\Cloud\Dropbox\Programming\Code\py\Miusik\Example\stylesheet\example.qss').read()
        self.setStyleSheet(qss_file)
        self.table.hideColumn(0)

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
                        string = common.format_time(value)
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

    def print_tags(self):
        all_tags = []
        for row in range(self.table.rowCount()):
            row_content = []
            for col in range(self.table.columnCount()):
                if self.table.item(row, col) is not None:
                    row_content.append(self.table.item(row, col).text().__str__())
                # print self.table.item(row, col)
            all_tags.append(row_content)
        for item in all_tags:
            print item


def test_tag():
    print get_tags(SONGS[0])


def test():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.set_content(SONGS)
    sys.exit(app.exec_())
