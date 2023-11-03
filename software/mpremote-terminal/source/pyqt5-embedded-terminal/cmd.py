import sys
import os
import re
from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess

class ConsoleLineEdit(QtWidgets.QLineEdit):
    newline = QtCore.pyqtSignal(str)

    def __init__(self, history: int = 100):
        super().__init__()
        self.history_max = history
        self.history = []
        self.line_index = 0
        self.clearHistory()
        self.prompt_pattern = re.compile('^[\>\.]')

    def clearHistory(self):
        self.history = []
        self.history_index = 0
        self.line_index = 0

    def event(self, ev: QtCore.QEvent) -> bool:
        if ev.type() == QtCore.QEvent.KeyPress:
            if ev.key() == int(QtCore.Qt.Key_Tab):
                self.insert('    ')
                return True
            elif ev.key() == int(QtCore.Qt.Key_Return):
                self.ret()
                return True
        return super().event(ev)
    
    def ret(self):
        text = self.text().rstrip()
        self.record(text)
        self.newline.emit(text)
        self.setText('')

    def record(self, line):
        self.history_index += 1
        while len(self.history) >= self.history_max - 1:
            self.history.pop()
        self.history.append(line)
        