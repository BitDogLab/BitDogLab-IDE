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
      [self.checkBox_m11, self.checkBox_m12, self.checkBox_m13, self.checkBox_m14, self.checkBox_m15],
      [self.checkBox_m21, self.checkBox_m22, self.checkBox_m23, self.checkBox_m24, self.checkBox_m25],
      [self.checkBox_m31, self.checkBox_m32, self.checkBox_m33, self.checkBox_m34, self.checkBox_m35],
      [self.checkBox_m41, self.checkBox_m42, self.checkBox_m43, self.checkBox_m44, self.checkBox_m45],
      [self.checkBox_m51, self.checkBox_m52, self.checkBox_m53, self.checkBox_m54, self.checkBox_m55],
    ]
    self.pushButton_selCols = [
      self.pushButton_selCol1, self.pushButton_selCol2, self.pushButton_selCol3, self.pushButton_selCol4, self.pushButton_selCol5
    ]
    self.pushButton_selRows = [
      self.pushButton_selRow1, self.pushButton_selRow2, self.pushButton_selRow3, self.pushButton_selRow4, self.pushButton_selRow5
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
    self.pushButton_selAll.clicked.connect(self.selectAll)
    self.pushButton_clearMatrix.clicked.connect(self.clearMatrix)
    self.pushButton_resetMatrix.clicked.connect(self.resetMatrix)

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
    r, g, b = self.horizontalSlider_R.value(), self.horizontalSlider_G.value(), self.horizontalSlider_B.value()
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
        self.ser.write("""\x03
from machine import Pin\r
import neopixel\r
np = neopixel.NeoPixel(Pin(7), 25)\r
np_queue = []\r
\r
def resetLEDs():\r
global np, np_queue\r
for i in range(25):\r
np[i] = (0, 0, 0)\r
\bnp.write()\r
np_queue = []\r
\b\r
def setLED(pos: tuple[int, int], color: tuple[int, int, int]):\r
global np_queue\r
y = pos[1]\r
x = (4 - pos[0]) if y%2==1 else pos[0]\r
np_queue.append((5*y + x, color))\r
\b\r
def updateLEDs():\r
global np, np_queue\r
while len(np_queue) > 0:\r
i, color = np_queue.pop(0)\r
np[i] = color\r
\bnp.write()\r
\b\r
""".encode())
        self.label_statusIsConnected.setText("Conectado")
        self.pushButton_connect.setText("Desconectar")
        return

  def disconnect(self):
    self.ser.write("""resetLEDs()\r
from machine import reset\r
reset()\r
""".encode()
    )
    self.ser.close()
    self.ser = None
    self.label_statusIsConnected.setText("Desconectado")
    self.pushButton_connect.setText("Conectar")

if __name__=="__main__":
  app = QApplication(sys.argv)
  window = Window()
  window.show()
  sys.exit(app.exec_())