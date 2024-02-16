# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
from .ui.ui import BaseWindow
import serial
from serial.tools.list_ports import comports

class Window(BaseWindow):
  def __init__(self):
    super(Window, self).__init__()
    self.ser = None

    # Connect pushButton_connect to connection lambda
    self.pushButton_connect.clicked.connect(lambda: self.connect() if self.ser is None else self.disconnect())

  def connect(self):
    for p in sorted(serial.tools.list_ports.comports()):
      if p.vid is not None and p.pid is not None:
        self.ser = serial.Serial(port=p.device, baudrate=115200)
        assert(self.ser is not None)

        # Format and write boot.py command to serial.
        with open('./src/Button-control/commands/boot.py', 'r') as f:
          command = f.read()
          command_split = command.split('\n')
          for i, s in enumerate(command_split):
            command_split[i] = s.strip()
          command = '\n\r'.join(command_split)
          if not command.endswith('\n\r'):
            command += '\n\r'
          self.ser.write(command.encode())
        
        self.label_statusIsConnect.setText("Status: Conectado")
        self.pushButton_connect.setText("Desconectar")
        return

  def disconnect(self):
    self.ser.write(
      """from machine import reset\r
reset()\r
""".encode()
    )
    self.ser.close()
    self.ser = None
    self.label_statusIsConnect.setText("Status: Desconectado")
    self.pushButton_connect.setText("Conectar")

  def closeEvent(self, event):
    if self.ser is not None:
      self.disconnect()
    event.accept()

if __name__=="__main__":
  app = QApplication(sys.argv)
  window = Window()
  window.show()
  sys.exit(app.exec_())