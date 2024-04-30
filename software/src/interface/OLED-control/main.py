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

    self.OLEDEdit.send_button.clicked.connect(self.sendStringToOLED)

    self.pushButton_connect.clicked.connect(lambda: self.connect() if self.ser is None else self.disconnect())

  def sendStringToOLED(self):
    if self.ser is None:
      return
    lines = self.OLEDEdit.getLines()
    command = f"\n\rsendStringToOLED({lines})\n\r"
    self.ser.write(command.encode())

  def connect(self):
    for p in sorted(serial.tools.list_ports.comports()):
      if p.vid is not None and p.pid is not None:
        self.ser = serial.Serial(port=p.device, baudrate=115200)
        assert(self.ser is not None)
        
        # Load setup.py with exec function via serial.
        with open('./src/interface/OLED-control/commands/setup.py', 'r') as f:
          command = '\x03exec(\'\'\'' + f.read().replace('\n', '\n\r') + '\'\'\')\n\r'
          self.ser.write(command.encode())

        self.label_statusIsConnect.setText("Status: Conectado")
        self.pushButton_connect.setText("Desconectar")
        return
      
  def disconnect(self):
    # Load reset.py with exec function via serial.
    with open('./src/interface/OLED-control/commands/reset.py', 'r') as f:
      command = '\x03exec(\'\'\'' + f.read().replace('\n', '\n\r') + '\'\'\')\n\r'
      self.ser.write(command.encode())

    self.ser.close()
    self.ser = None
    self.label_statusIsConnect.setText("Status: Desconectado")
    self.pushButton_connect.setText("Conectar")

if __name__=="__main__":
  app = QApplication(sys.argv)
  window = Window()
  window.show()
  sys.exit(app.exec_())