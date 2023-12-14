import os, sys
sys.path.insert(0, ".")

import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QRunnable, pyqtSlot, QThreadPool
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPlainTextEdit
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

from .commands import *
from .shell import State, COMMANDS, _runCommand
from .ui.shell_window import Ui_ShellWindow

state = State()

class SerialSignals(QObject):
    error = pyqtSignal(tuple)
    finished = pyqtSignal()

class SerialWorker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = SerialSignals()

    @pyqtSlot()
    def run(self):
        try:
            self.fn(*self.args, **self.kwargs)
        except:
            import traceback
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()

class ConsoleInterface(QMainWindow, Ui_ShellWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.output.setReadOnly(True)
        self.input.returnPressed.connect(self._sendCommand)
        self.attachState(state)
        self.thread_running = True
        worker = SerialWorker(self.__serialMonitorTask, self.state, self.output)
        self.threadpool = QThreadPool()
        self.threadpool.start(worker)

    def closeEvent(self, event):
        self.thread_running = False

    def attachState(self, state):
        self.state = state

    def _sendCommand(self):
        command = self.input.text()
        self.output.appendPlainText(f"$ {command}" if not self.state.connected else command)
        _runCommand(self.state, command)
        self.input.clear()
        # self.__serialMonitorTask()
    
    def __serialMonitorTask(self, state, output): # Was previously thread.
        while self.thread_running:
            if state.connected and state.serial.in_waiting > 0:
                string = ""
                remaining = state.serial.in_waiting
                while remaining > 0:
                    string += state.serial.read(min(256, remaining)).decode()
                    remaining = state.serial.in_waiting
                    time.sleep(0.01)
                lines = string.split('\n')
                if lines[-1] == ">>> ":
                    lines.pop()
                for line in lines:
                    output.appendPlainText(line)
            if state.hasBuf():
                for line in state.readBufLines():
                    output.appendPlainText(f"> {line}")
            time.sleep(0.01)

if __name__=="__main__":
    app = QApplication(sys.argv)
    console = ConsoleInterface()
    console.show()
    sys.exit(app.exec_())