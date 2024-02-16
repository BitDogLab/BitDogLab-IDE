import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *

class NeoPixelControl(QWidget):
  def __init__(self, *args, **kwargs):
    super(NeoPixelControl, self).__init__(*args, **kwargs)
    uic.loadUi("./src/interface/NeoPixel-control/ui/neopixel_control.ui", self)
    self.widget_RGBselect.setColorMaximum(255)

class BaseWindow(QMainWindow):
  def __init__(self):
    super(BaseWindow, self).__init__()
    uic.loadUi("./src/interface/NeoPixel-control/ui/main.ui", self)

if __name__=="__main__":
  app = QApplication(sys.argv)
  window = BaseWindow()
  window.show()
  sys.exit(app.exec_())