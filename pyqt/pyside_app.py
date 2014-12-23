#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial

In this example, we create a simple
window in PyQt4.

author: Jan Bodnar
website: zetcode.com
last edited: October 2011
"""

import time
import sys
from PyQt4 import QtCore, QtGui

app = QtGui.QApplication(sys.argv)

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.resize(500, 500)
        self.move(300, 300)
        self.setWindowTitle('')
        self.label = QtGui.QLabel(self)
        self.label.setText('Label Text')

        self.show()

        self.printsomething()

    def printsomething(self):
        print ('1')
        time.sleep(2)
        print('2')

    def printsomethingelse(self):
        print ('3')
        time.sleep(2)
        print('4')


w = Window()

w.printsomethingelse()

sys.exit(app.exec_())
