import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *

class BaseWindow(QMainWindow):
  def __init__(self):
    super(BaseWindow, self).__init__()
    
    # Load .ui file.
    uic.loadUi("src/Button-control/ui/main.ui", self)

if __name__=="__main__":
  app = QApplication(sys.argv)
  window = BaseWindow()
  window.show()
  sys.exit(app.exec_())