import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *

class RGBSelect(QWidget):
  def __init__(self, *args, **kwargs):
    super(RGBSelect, self).__init__(*args, **kwargs)
    uic.loadUi("./src/utils/RGB-select/rgbselect.ui", self)

    # Set color widget background to black initially
    self.widget_RGB.setStyleSheet("QWidget#widget_RGB { background-color: #000000 }")

    # Connect background color changes
    self.horizontalSlider_R.valueChanged.connect(self.handleColorChange)
    self.horizontalSlider_G.valueChanged.connect(self.handleColorChange)
    self.horizontalSlider_B.valueChanged.connect(self.handleColorChange)

    # Define maximum color value. Default is 255.
    self.maximum = 255
    
    # Testing custom limits
    # self.maximum = 100
    # self.setLimits(self.maximum)
  
  def handleColorChange(self):
    r, g, b = self.horizontalSlider_R.value(), self.horizontalSlider_G.value(), self.horizontalSlider_B.value()
    r, g, b = r*255/self.maximum, g*255/self.maximum, b*255/self.maximum # Interpolates to show correct color in widget
    self.widget_RGB.setStyleSheet(f"QWidget#widget_RGB {{ background-color: rgb({int(r)}, {int(g)}, {int(b)}) }}")
  
  def getColor(self):
    r, g, b = self.horizontalSlider_R.value(), self.horizontalSlider_G.value(), self.horizontalSlider_B.value()
    return (r, g, b)
  
  def setColorMaximum(self, max_color_value: int):
    self.maximum = max_color_value
    self.horizontalSlider_R.setMaximum(self.maximum)
    self.horizontalSlider_G.setMaximum(self.maximum)
    self.horizontalSlider_B.setMaximum(self.maximum)
    self.spinBox_R.setMaximum(self.maximum)
    self.spinBox_G.setMaximum(self.maximum)
    self.spinBox_B.setMaximum(self.maximum)

if __name__=="__main__":
  app = QApplication(sys.argv)
  widget = RGBSelect()
  widget.show()
  sys.exit(app.exec_())
