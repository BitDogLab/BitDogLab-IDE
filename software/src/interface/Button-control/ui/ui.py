import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *

class ButtonOptions(QWidget):
  def __init__(self, *args, **kwargs):
    super(ButtonOptions, self).__init__(*args, **kwargs)
    uic.loadUi("./src/interface/Button-control/ui/options/container.ui", self)

class NeoPixelPresets(QWidget):
  def __init__(self, *args, **kwargs):
    super(NeoPixelPresets, self).__init__(*args, **kwargs)
    uic.loadUi("./src/interface/Button-control/ui/options/neopixel_presets.ui", self)

class RGBLED(QWidget):
  def __init__(self, *args, **kwargs):
    super(RGBLED, self).__init__(*args, **kwargs)
    uic.loadUi("./src/interface/Button-control/ui/options/rgbled.ui", self)
    self.RGBSelect.setColorMaximum(65535)

class Buzzer(QWidget):
  TONES = [ # In order: C, C#, D, D#, E, F, F#, G, G#, A, A#, B.
    [16, 17, 18, 19, 21, 22, 23, 25, 26, 28, 29, 31],
    [33, 35, 37, 39, 41, 44, 46, 49, 52, 55, 58, 62],
    [65, 69, 73, 78, 82, 87, 93, 98, 104, 110, 117, 123],
    [131, 139, 147, 156, 165, 175, 185, 196, 208, 220, 233, 247],
    [262, 277, 294, 311, 330, 349, 370, 392, 415, 440, 466, 494],
    [523, 554, 587, 622, 659, 698, 740, 784, 831, 880, 932, 988],
    [1047, 1109, 1175, 1245, 1319, 1397, 1480, 1568, 1661, 1760, 1865, 1976],
    [2093, 2217, 2349, 2489, 2637, 2794, 2960, 3136, 3322, 3520, 3729, 3951],
    [4186, 4435, 4698, 4978, 5274, 5588, 5920, 6272, 6645, 7040, 7459, 7902]
  ]

  def __init__(self, *args, **kwargs):
    super(Buzzer, self).__init__(*args, **kwargs)
    uic.loadUi("./src/interface/Button-control/ui/options/buzzer.ui", self)
    self.buzzerid = -1
    self.toneSelect.setCurrentIndex(9)

    self.restoreButton.clicked.connect(self.restore)
  
  def setID(self, id: int):
    self.buzzerid = id

  def getID(self):
    return self.buzzerid

  def restore(self):
    self.pitchSelect.setValue(4)
    self.toneSelect.setCurrentIndex(9)

  def getTone(self):
    return self.toneSelect.currentIndex()

  def getPitch(self):
    return self.pitchSelect.value()

  def getFrequency(self):
    return self.TONES[self.getPitch()][self.getTone()]

class BaseWindow(QMainWindow):
  def __init__(self):
    super(BaseWindow, self).__init__()
    
    # Load .ui file.
    uic.loadUi("./src/interface/Button-control/ui/main.ui", self)

if __name__=="__main__":
  app = QApplication(sys.argv)
  window = BaseWindow()
  window.show()
  sys.exit(app.exec_())