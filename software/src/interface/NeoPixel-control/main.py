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

    # Connect buttons
    self.pushButton_connect.clicked.connect(lambda: self.connect() if self.ser is None else self.disconnect())
    self.pushButton_sendColor.clicked.connect(self.sendColor)

    # Create checkbox, col select and row select object lists.
    self.np_matrix_select = [
      [self.npControl.checkBox_m11, self.npControl.checkBox_m12, self.npControl.checkBox_m13, self.npControl.checkBox_m14, self.npControl.checkBox_m15],
      [self.npControl.checkBox_m21, self.npControl.checkBox_m22, self.npControl.checkBox_m23, self.npControl.checkBox_m24, self.npControl.checkBox_m25],
      [self.npControl.checkBox_m31, self.npControl.checkBox_m32, self.npControl.checkBox_m33, self.npControl.checkBox_m34, self.npControl.checkBox_m35],
      [self.npControl.checkBox_m41, self.npControl.checkBox_m42, self.npControl.checkBox_m43, self.npControl.checkBox_m44, self.npControl.checkBox_m45],
      [self.npControl.checkBox_m51, self.npControl.checkBox_m52, self.npControl.checkBox_m53, self.npControl.checkBox_m54, self.npControl.checkBox_m55],
    ]
    self.pushButton_selCols = [
      self.npControl.pushButton_selCol1, self.npControl.pushButton_selCol2, self.npControl.pushButton_selCol3, self.npControl.pushButton_selCol4, self.npControl.pushButton_selCol5
    ]
    self.pushButton_selRows = [
      self.npControl.pushButton_selRow1, self.npControl.pushButton_selRow2, self.npControl.pushButton_selRow3, self.npControl.pushButton_selRow4, self.npControl.pushButton_selRow5
    ]
    self.pushButton_selCols_lambdas = [
      lambda: self.selectColumn(0), lambda: self.selectColumn(1), lambda: self.selectColumn(2), lambda: self.selectColumn(3), lambda: self.selectColumn(4)
    ]
    self.pushButton_selRows_lambdas = [
      lambda: self.selectRow(0), lambda: self.selectRow(1), lambda: self.selectRow(2), lambda: self.selectRow(3), lambda: self.selectRow(4)
    ]

    for i in range(5):
      self.pushButton_selCols[i].clicked.connect(self.pushButton_selCols_lambdas[i])
      self.pushButton_selRows[i].clicked.connect(self.pushButton_selRows_lambdas[i])
    self.npControl.pushButton_selAll.clicked.connect(self.selectAll)
    self.npControl.pushButton_clearMatrix.clicked.connect(self.clearMatrix)
    self.npControl.pushButton_resetMatrix.clicked.connect(self.resetMatrix)

  def selectColumn(self, col):
    for i in range(5):
      self.np_matrix_select[i][col].click()

  def selectRow(self, row):
    for j in range(5):
      self.np_matrix_select[row][j].click()

  def selectAll(self):
    for i in range(5):
      for j in range(5):
        self.np_matrix_select[i][j].click()

  def clearMatrix(self):
    for i in range(5):
      for j in range(5):
        self.np_matrix_select[i][j].setChecked(False)
  
  def resetMatrix(self):
    self.ser.write("resetLEDs()\r\n".encode())

  def sendColor(self):
    r, g, b = self.npControl.widget_RGBselect.getColor()
    for i in range(5):
      for j in range(5):
        if self.np_matrix_select[i][j].isChecked():
          print(f"{i} {j} checked!")
          self.ser.write(f"setLED(({j}, {i}), ({r}, {g}, {b}))\r\n".encode())
    self.ser.write("updateLEDs()\r\n".encode())

  def connect(self):
    for p in sorted(serial.tools.list_ports.comports()):
      if p.vid is not None and p.pid is not None:
        self.ser = serial.Serial(port=p.device, baudrate=115200)
        assert(self.ser is not None)
        
        # Load setup.py with exec function via serial.
        with open('./src/interface/NeoPixel-control/commands/setup.py', 'r') as f:
          command = '\x03exec(\'\'\'' + f.read().replace('\n', '\n\r') + '\'\'\')\n\r'
          self.ser.write(command.encode())
        
        self.label_statusIsConnected.setText("Conectado")
        self.pushButton_connect.setText("Desconectar")
        return

  def disconnect(self):
    # Load reset.py with exec function via serial.
    with open('./src/interface/NeoPixel-control/commands/reset.py', 'r') as f:
      command = '\x03exec(\'\'\'' + f.read().replace('\n', '\n\r') + '\'\'\')\n\r'
      self.ser.write(command.encode())
    
    self.ser.close()
    self.ser = None
    self.label_statusIsConnected.setText("Desconectado")
    self.pushButton_connect.setText("Conectar")

if __name__=="__main__":
  app = QApplication(sys.argv)
  window = Window()
  window.show()
  sys.exit(app.exec_())