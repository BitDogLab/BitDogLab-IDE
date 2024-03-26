# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
from .ui.ui import BaseWindow
import serial
from serial.tools.list_ports import comports

class Window(BaseWindow):
  STATE__INDEX_CHANGING = False

  def __init__(self):
    super(Window, self).__init__()
    self.ser = None

    # Connect pushButton_connect to connection lambda
    self.pushButton_connect.clicked.connect(lambda: self.connect() if self.ser is None else self.disconnect())

    # Setting up button widgets
    self.buttons = [self.buttonA, self.buttonB] # Creating list reference to make things easier when executing functions that rely on button ID.
    self.indices = [0, 1] # Initial pages.

    # Repeat setup steps for both buttons
    self.buttonA.funcSelect.setCurrentIndex(self.indices[0])
    self.buttonB.funcSelect.setCurrentIndex(self.indices[1])
    self.buttonA.modeSelect.currentIndexChanged.connect(lambda: self.updateButtonMode(0))
    self.buttonB.modeSelect.currentIndexChanged.connect(lambda: self.updateButtonMode(1))

    # Setting up NeoPixel widget
    self.buttonA.options.widget(0).RGBSelect.sendColorButton.setText("Enviar")
    self.buttonA.options.widget(0).RGBSelect.sendColorButton.clicked.connect(self.sendNeoPixel)
    self.buttonA.options.widget(0).drawingSelect.currentIndexChanged.connect(self.sendNeoPixel)
    self.buttonB.options.widget(0).RGBSelect.sendColorButton.setText("Enviar")
    self.buttonB.options.widget(0).RGBSelect.sendColorButton.clicked.connect(self.sendNeoPixel)
    self.buttonB.options.widget(0).drawingSelect.currentIndexChanged.connect(self.sendNeoPixel)

    # Setting up RGB LED widget
    self.buttonA.options.widget(1).RGBSelect.sendColorButton.clicked.connect(self.sendColorLED)
    self.buttonB.options.widget(1).RGBSelect.sendColorButton.clicked.connect(self.sendColorLED)

    # Setting up Buzzer widgets
    self.buttonA.options.widget(2).setID(0)
    self.buttonA.options.widget(2).toneSelect.currentIndexChanged.connect(lambda: self.buttonA.options.widget(2).freqShowLabel.setText(f" {self.buttonA.options.widget(2).getFrequency()}Hz"))
    self.buttonA.options.widget(2).pitchSelect.valueChanged.connect(lambda: self.buttonA.options.widget(2).freqShowLabel.setText(f" {self.buttonA.options.widget(2).getFrequency()}Hz"))
    self.buttonA.options.widget(2).sendButton.clicked.connect(lambda: self.sendBuzzerFrequency(2))
    self.buttonA.options.widget(3).setID(1)
    self.buttonA.options.widget(3).toneSelect.currentIndexChanged.connect(lambda: self.buttonA.options.widget(3).freqShowLabel.setText(f" {self.buttonA.options.widget(3).getFrequency()}Hz"))
    self.buttonA.options.widget(3).pitchSelect.valueChanged.connect(lambda: self.buttonA.options.widget(3).freqShowLabel.setText(f" {self.buttonA.options.widget(3).getFrequency()}Hz"))
    self.buttonA.options.widget(3).sendButton.clicked.connect(lambda: self.sendBuzzerFrequency(3))

    self.buttonB.options.widget(2).setID(0)
    self.buttonB.options.widget(2).toneSelect.currentIndexChanged.connect(lambda: self.buttonB.options.widget(2).freqShowLabel.setText(f" {self.buttonB.options.widget(2).getFrequency()}Hz"))
    self.buttonB.options.widget(2).pitchSelect.valueChanged.connect(lambda: self.buttonB.options.widget(2).freqShowLabel.setText(f" {self.buttonB.options.widget(2).getFrequency()}Hz"))
    self.buttonB.options.widget(2).sendButton.clicked.connect(lambda: self.sendBuzzerFrequency(2))
    self.buttonB.options.widget(3).setID(1)
    self.buttonB.options.widget(3).toneSelect.currentIndexChanged.connect(lambda: self.buttonB.options.widget(3).freqShowLabel.setText(f" {self.buttonB.options.widget(3).getFrequency()}Hz"))
    self.buttonB.options.widget(3).pitchSelect.valueChanged.connect(lambda: self.buttonB.options.widget(3).freqShowLabel.setText(f" {self.buttonB.options.widget(3).getFrequency()}Hz"))
    self.buttonB.options.widget(3).sendButton.clicked.connect(lambda: self.sendBuzzerFrequency(3))
    
    # Lambdas are set separately to avoid any issues.
    self.buttonA.funcSelect.currentIndexChanged.connect(lambda: self.handleFuncChange(0))
    self.buttonB.funcSelect.currentIndexChanged.connect(lambda: self.handleFuncChange(1))

  def updateButtonMode(self, buttonid: int):
    if self.ser is None:
      return
    mode = self.buttons[buttonid].modeSelect.currentIndex()
    command = ("exec('''" + 
      f"ButtonHandler.BUTTONS_MODE[{buttonid}] = {mode}\n\r" + 
      f"ButtonHandler.BUTTONS_STATE[{buttonid}] = False\n\r" + 
      "''')\n\r"
    )
    self.ser.write(command.encode())

  def handleFuncChange(self, buttonid: int):
    # Check for state variable.
    if self.STATE__INDEX_CHANGING:
      return
    self.STATE__INDEX_CHANGING = True

    # If two indices are the same, perform switch. Widgets can't be the same page at the same time.
    new_indices = [self.buttonA.funcSelect.currentIndex(), self.buttonB.funcSelect.currentIndex()]
    # self.buttons[1 - buttonid].funcSelect.view().setRowHidden(self.indices[buttonid], False)
    # self.buttons[1 - buttonid].funcSelect.view().setRowHidden(new_indices[buttonid], True)
    if new_indices[buttonid] == self.indices[1 - buttonid]: # Switch pages.
      self.buttons[1 - buttonid].funcSelect.setCurrentIndex(self.indices[buttonid])
      new_indices[1 - buttonid] = self.indices[buttonid]
    self.indices = new_indices

    # Copy settings between buttons. Keeps things the same when changing pages.
    for i in range(2):
      match self.indices[i]:
        case 0:
          self.buttons[i].options.widget(0).RGBSelect.setColor(self.buttons[1 - i].options.widget(0).RGBSelect.getColor())
          self.buttons[i].options.widget(0).drawingSelect.setCurrentIndex(self.buttons[1 - i].options.widget(0).drawingSelect.currentIndex())
        case 1:
          self.buttons[i].options.widget(1).RGBSelect.setColor(self.buttons[1 - i].options.widget(1).RGBSelect.getColor())
        case 2:
          self.buttons[i].options.widget(2).toneSelect.setCurrentIndex(self.buttons[1 - i].options.widget(2).toneSelect.currentIndex())
          self.buttons[i].options.widget(2).pitchSelect.setValue(self.buttons[1 - i].options.widget(2).pitchSelect.value())
        case 3:
          self.buttons[i].options.widget(3).toneSelect.setCurrentIndex(self.buttons[1 - i].options.widget(3).toneSelect.currentIndex())
          self.buttons[i].options.widget(3).pitchSelect.setValue(self.buttons[1 - i].options.widget(3).pitchSelect.value())

    # Update state variable.
    self.STATE__INDEX_CHANGING = False

    # Update Pico interrupts if serial port is open.
    if self.ser is not None:
      self.updateInterrupts()

  def sendNeoPixel(self):
    # If serial is disconnected, don't do anything.
    if self.ser is None:
      return  # This can be replaced with a print error message or QMessageBox.
    buttonid = self.indices.index(0) # Gets button ID from which widget is NeoPixel.
    rgb = self.buttons[buttonid].options.widget(0).RGBSelect.getColor()
    pattern_id = self.buttons[buttonid].options.widget(0).drawingSelect.currentIndex()
    pattern_name = self.buttons[buttonid].options.widget(0).getPattern(pattern_id)
    command = ("exec('''" + 
      f"ButtonHandler.BUTTONS_FALLING_IRQ[{buttonid}] = NeoPixelDesenhos.{pattern_name}\n\r" + 
      f"ButtonHandler.BUTTONS_RISING_IRQ[{buttonid}] = NeoPixelDesenhos.apaga\n\r" + 
      f"NeoPixelDesenhos.COLOR = {rgb}\n\r" + 
      "NeoPixelDesenhos.apaga()\n\r" + 
      "''')\n\r"
    )
    self.ser.write(command.encode())

  def sendColorLED(self):
    # If serial is disconnected, don't do anything.
    if self.ser is None:
      return  # This can be replaced with a print error message or QMessageBox.
    rgb = self.buttons[
      self.indices.index(1)
    ].options.widget(1).RGBSelect.getColor()
    command = ("exec('''" + 
      f"LedRGB.COLOR = {rgb}\n\r" + 
      "LedRGB.atualizar()\n\r" + 
      "''')\n\r"
    )
    self.ser.write(command.encode())

  def sendBuzzerFrequency(self, widgetid):
    # If serial is disconnected, don't do anything.
    if self.ser is None:
      return  # This can be replaced with a print error message or QMessageBox.
    id = self.indices.index(widgetid)
    freq = self.buttons[id].options.widget(widgetid).getFrequency()
    volume = self.buttons[id].options.widget(widgetid).getVolume()
    buzzerid = self.buttons[id].options.widget(widgetid).getID()
    command = ("exec('''" + 
      # f"Buzzer.definirNota({buzzerid}, {freq})\n\r" + 
      f"Buzzer.VOLUMES[{buzzerid}] = {volume}\n\r" + 
      f"Buzzer.BUZZERS[{buzzerid}].freq({freq})\n\r" + 
      f"Buzzer.atualizar({buzzerid})\n\r" + 
      "''')\n\r"
    )
    self.ser.write(command.encode())

  def updateInterrupts(self):
    # Updates interrupts in acoordance with the currently selected widgets.
    for i in range(2):
      match self.indices[i]:
        case 0: # If the NeoPixel widget is open...
          command = ("exec('''" + 
            f"ButtonHandler.BUTTONS_RISING_IRQ[{i}] = NeoPixelDesenhos.apaga\n\r" + 
            "''')\n\r"
          )
          self.ser.write(command.encode())
        case 1: # If the RGB LED widget is open...
          # Update color and both IRQs.
          command = ("exec('''" + 
            f"LedRGB.COLOR = {self.buttons[i].options.widget(1).RGBSelect.getColor()}\n\r" + 
            f"ButtonHandler.BUTTONS_FALLING_IRQ[{i}] = LedRGB.ligar\n\r" + 
            f"ButtonHandler.BUTTONS_RISING_IRQ[{i}] = LedRGB.desligar\n\r" + 
            "''')\n\r"
          )
          self.ser.write(command.encode())
        case 2: # If the Buzzer A widget is open...
          self.sendBuzzerFrequency(2)
          command = ("exec('''" + 
            f"ButtonHandler.BUTTONS_FALLING_IRQ[{i}] = lambda: Buzzer.ligar(0)\n\r" + 
            f"ButtonHandler.BUTTONS_RISING_IRQ[{i}] = lambda: Buzzer.desligar(0)\n\r" + 
            "''')\n\r"
          )
          self.ser.write(command.encode())
        case 3: # If the Buzzer B widget is open...
          self.sendBuzzerFrequency(3)
          command = ("exec('''" + 
            f"ButtonHandler.BUTTONS_FALLING_IRQ[{i}] = lambda: Buzzer.ligar(1)\n\r" + 
            f"ButtonHandler.BUTTONS_RISING_IRQ[{i}] = lambda: Buzzer.desligar(1)\n\r" + 
            "''')\n\r"
          )
          self.ser.write(command.encode())

  def connect(self):
    # Checks all available ports. If one is serial-compatible, open it and begin communication.
    for p in sorted(serial.tools.list_ports.comports()):
      if p.vid is not None and p.pid is not None:
        self.ser = serial.Serial(port=p.device, baudrate=115200)
        assert(self.ser is not None)

        # Load setup.py with exec function via serial.
        with open('./src/interface/Button-control/commands/setup.py', 'r') as f:
          command = '\x03exec(\'\'\'' + f.read().replace('\n', '\n\r') + '\'\'\')\n\r'
          self.ser.write(command.encode())
        
        # Update interrupts via serial
        self.updateInterrupts()

        self.label_statusIsConnect.setText("Status: Conectado")
        self.pushButton_connect.setText("Desconectar")
        return

  def disconnect(self):
    # Load setup.py with exec function via serial.
    with open('./src/interface/Button-control/commands/reset.py', 'r') as f:
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