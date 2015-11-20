from PyQt4 import QtGui, QtCore
from time import sleep

class MyThread(QtCore.QThread):
    def __init__(self):
        super(MyThread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            print "Tada"
            sleep(2)


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.btn_run = QtGui.QPushButton("Run", self)
        self.btn_run.move(50, 20)
        self.line_edit = QtGui.QLineEdit(self)
        self.line_edit.move(20, 40)
        self.btn_click = QtGui.QPushButton("Print", self)
        self.btn_click.move(20, 60)

        self.btn_click.clicked.connect(self.print_text)
        self.btn_run.clicked.connect(self.run_thread)

    def run_thread(self):
        self.thread = MyThread()
        self.thread.start()

    def print_text(self):
        print self.line_edit.text().decode("utf-8")

def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()