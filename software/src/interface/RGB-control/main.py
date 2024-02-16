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
    self.pushButton_send.clicked.connect(self.sendColor)

  def connect(self):
    for p in sorted(serial.tools.list_ports.comports()):
      if p.vid is not None and p.pid is not None:
        self.ser = serial.Serial(port=p.device, baudrate=115200)
        assert(self.ser is not None)
        self.ser.write("""\x03
from machine import Pin, PWM\r
pinR = Pin(12)\r
pinG = Pin(11)\r
pinB = Pin(13)\r
pwmR = PWM(pinR)\r
pwmG = PWM(pinG)\r
pwmB = PWM(pinB)\r
pwmR.freq(500)\r
pwmG.freq(500)\r
pwmB.freq(500)\r
pwmR.duty_u16(0)\r
pwmG.duty_u16(0)\r
pwmB.duty_u16(0)\r
""".encode())
        self.label_statusIsConnect.setText("Conectado")
        self.pushButton_connect.setText("Desconectar")
        return

  def disconnect(self):
    self.ser.write(
      """pwmR.duty_u16(0)\r
pwmG.duty_u16(0)\r
pwmB.duty_u16(0)\r
from machine import reset\r
reset()\r
""".encode()
    )
    self.ser.close()
    self.ser = None
    self.label_statusIsConnect.setText("Desconectado")
    self.pushButton_connect.setText("Conectar")

  def sendColor(self):
    if self.ser is None:
      QMessageBox.critical(self, "Error! Port closed!", "Can't send color! Port is closed!")
      return
    r, g, b = self.hSlider_R.value(), self.hSlider_G.value(), self.hSlider_B.value()
    self.ser.write(
      f"""pwmR.duty_u16({r})\r
pwmG.duty_u16({g})\r
pwmB.duty_u16({b})\r
""".encode()
    )

  def closeEvent(self, event):
    if self.ser is not None:
      self.disconnect()
    event.accept()


if __name__=="__main__":
  app = QApplication(sys.argv)
  window = Window()
  window.show()
  sys.exit(app.exec_())