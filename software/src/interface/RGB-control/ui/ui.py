import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *

class BaseWindow(QMainWindow):
  def __init__(self):
    super(BaseWindow, self).__init__()
    
    # Load .ui file.
    uic.loadUi("./src/interface/RGB-control/ui/main.ui", self)

    # Set color widget background to black initially
    self.colorWidget.setStyleSheet("QWidget#colorWidget { background-color: #000000 }")

    # Connect background color changes
    self.hSlider_R.valueChanged.connect(self.handleColorChange)
    self.hSlider_G.valueChanged.connect(self.handleColorChange)
    self.hSlider_B.valueChanged.connect(self.handleColorChange)
  
  def handleColorChange(self):
    r, g, b = self.hSlider_R.value()//256, self.hSlider_G.value()//256, self.hSlider_B.value()//256
    self.colorWidget.setStyleSheet(f"QWidget#colorWidget {{ background-color: rgb({r}, {g}, {b}) }}")

if __name__=="__main__":
  app = QApplication(sys.argv)
  window = BaseWindow()
  window.show()
  sys.exit(app.exec_())