import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *

class BaseWindow(QMainWindow):
  def __init__(self):
    super(BaseWindow, self).__init__()

    # Load .ui file
    uic.loadUi("src/NeoPixel-control/ui/main.ui", self)

      # RGB selection widget!
    # Set color widget background to black initially
    self.widget_RGB.setStyleSheet("QWidget#widget_RGB { background-color: #000000 }")

    # Connect background color changes
    self.horizontalSlider_R.valueChanged.connect(self.handleColorChange)
    self.horizontalSlider_G.valueChanged.connect(self.handleColorChange)
    self.horizontalSlider_B.valueChanged.connect(self.handleColorChange)
  
  def handleColorChange(self):
    r, g, b = self.horizontalSlider_R.value(), self.horizontalSlider_G.value(), self.horizontalSlider_B.value()
    self.widget_RGB.setStyleSheet(f"QWidget#widget_RGB {{ background-color: rgb({r}, {g}, {b}) }}")

if __name__=="__main__":
  app = QApplication(sys.argv)
  window = BaseWindow()
  window.show()
  sys.exit(app.exec_())