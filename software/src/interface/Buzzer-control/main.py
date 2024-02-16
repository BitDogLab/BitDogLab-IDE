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

    # Connect piano buttons to notes dict.
    self.notes = {
      'B3': 247,
      'C4': 262,
      'Cs4': 277,
      'D4': 294,
      'Ds4': 311,
      'E4': 330,
      'F4': 349,
      'Fs4': 370,
      'G4': 392,
      'Gs4': 415,
      'A4': 440,
      'As4': 466,
      'B4': 494,
      'C5': 523
    }
    self.pushButton_B3.pressed.connect(lambda: self.playNote('B3'))
    self.pushButton_C4.pressed.connect(lambda: self.playNote('C4'))
    self.pushButton_Cs4.pressed.connect(lambda: self.playNote('Cs4'))
    self.pushButton_D4.pressed.connect(lambda: self.playNote('D4'))
    self.pushButton_Ds4.pressed.connect(lambda: self.playNote('Ds4'))
    self.pushButton_E4.pressed.connect(lambda: self.playNote('E4'))
    self.pushButton_F4.pressed.connect(lambda: self.playNote('F4'))
    self.pushButton_Fs4.pressed.connect(lambda: self.playNote('Fs4'))
    self.pushButton_G4.pressed.connect(lambda: self.playNote('G4'))
    self.pushButton_Gs4.pressed.connect(lambda: self.playNote('Gs4'))
    self.pushButton_A4.pressed.connect(lambda: self.playNote('A4'))
    self.pushButton_As4.pressed.connect(lambda: self.playNote('As4'))
    self.pushButton_B4.pressed.connect(lambda: self.playNote('B4'))
    self.pushButton_C5.pressed.connect(lambda: self.playNote('C5'))

    # Connect release buttons to release note.
    self.pushButton_B3.released.connect(self.stopNote)
    self.pushButton_C4.released.connect(self.stopNote)
    self.pushButton_Cs4.released.connect(self.stopNote)
    self.pushButton_D4.released.connect(self.stopNote)
    self.pushButton_Ds4.released.connect(self.stopNote)
    self.pushButton_E4.released.connect(self.stopNote)
    self.pushButton_F4.released.connect(self.stopNote)
    self.pushButton_Fs4.released.connect(self.stopNote)
    self.pushButton_G4.released.connect(self.stopNote)
    self.pushButton_Gs4.released.connect(self.stopNote)
    self.pushButton_A4.released.connect(self.stopNote)
    self.pushButton_As4.released.connect(self.stopNote)
    self.pushButton_B4.released.connect(self.stopNote)
    self.pushButton_C5.released.connect(self.stopNote)

  def playNote(self, note):
    if self.ser is None:
      print("Serial port not connected! Note not played.")
      return
    self.ser.write(f"buzzerA_pwm.freq({self.notes[note]})\r\nbuzzerA_pwm.duty_u16({self.buzzer_volume})\r\nbuzzerB_pwm.freq({self.notes[note]})\r\nbuzzerB_pwm.duty_u16({self.buzzer_volume})\r\n".encode())

  def stopNote(self):
    if self.ser is None:
      return
    self.ser.write("buzzerA_pwm.duty_u16(0)\r\nbuzzerB_pwm.duty_u16(0)\r\n".encode())

  def connect(self):
    for p in sorted(serial.tools.list_ports.comports()):
      if p.vid is not None and p.pid is not None:
        self.ser = serial.Serial(port=p.device, baudrate=115200)
        assert(self.ser is not None)
        
        # Load setup.py with exec function via serial.
        with open('./src/interface/Buzzer-control/commands/setup.py', 'r') as f:
          command = '\x03exec(\'\'\'' + f.read().replace('\n', '\n\r') + '\'\'\')\n\r'
          self.ser.write(command.encode())

        self.label_statusIsConnect.setText("Status: Conectado")
        self.pushButton_connect.setText("Desconectar")
        return

  def disconnect(self):
    # Load reset.py with exec function via serial.
    with open('./src/interface/Buzzer-control/commands/reset.py', 'r') as f:
      command = '\x03exec(\'\'\'' + f.read().replace('\n', '\n\r') + '\'\'\')\n\r'
      self.ser.write(command.encode())

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