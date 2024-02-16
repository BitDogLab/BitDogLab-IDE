import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *

class BaseWindow(QMainWindow):
  def __init__(self):
    super(BaseWindow, self).__init__()

    # Load .ui file
    uic.loadUi("./src/interface/Buzzer-control/ui/main.ui", self)

    # Setup button appearances
    WHITES_STYLESHEET = "QPushButton { padding-top: 100% 0; }"
    BLACKS_STYLESHEET = "QPushButton { padding-top: 50% 0; background-color: rgb(30, 30, 30); color: white; } QPushButton:pressed { background-color: rgb(60, 60, 60); }"

    self.pushButton_B3.setStyleSheet(WHITES_STYLESHEET)
    self.pushButton_C4.setStyleSheet(WHITES_STYLESHEET)
    self.pushButton_D4.setStyleSheet(WHITES_STYLESHEET)
    self.pushButton_E4.setStyleSheet(WHITES_STYLESHEET)
    self.pushButton_F4.setStyleSheet(WHITES_STYLESHEET)
    self.pushButton_G4.setStyleSheet(WHITES_STYLESHEET)
    self.pushButton_A4.setStyleSheet(WHITES_STYLESHEET)
    self.pushButton_B4.setStyleSheet(WHITES_STYLESHEET)
    self.pushButton_C5.setStyleSheet(WHITES_STYLESHEET)
    self.pushButton_Cs4.setStyleSheet(BLACKS_STYLESHEET)
    self.pushButton_Ds4.setStyleSheet(BLACKS_STYLESHEET)
    self.pushButton_Fs4.setStyleSheet(BLACKS_STYLESHEET)
    self.pushButton_Gs4.setStyleSheet(BLACKS_STYLESHEET)
    self.pushButton_As4.setStyleSheet(BLACKS_STYLESHEET)

    self.buzzer_volume = 32767
    self.verticalSlider_buzzerVolume.valueChanged.connect(self.handleVolumeChange)

  def handleVolumeChange(self):
    value = self.verticalSlider_buzzerVolume.value()
    self.buzzer_volume = value
    self.progressBar_buzzerVolume.setValue(value)
    # print(self.buzzer_volume)

if __name__=="__main__":
  app = QApplication(sys.argv)
  window = BaseWindow()
  window.show()
  sys.exit(app.exec_())