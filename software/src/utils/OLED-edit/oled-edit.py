import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *

class OLEDEdit(QWidget):
  def __init__(self, *args, **kwargs):
    super(OLEDEdit, self).__init__(*args, **kwargs)
    uic.loadUi("./src/utils/OLED-edit/oled-edit.ui", self)

    self.__is_adjusting_text_flag = False
    self.__lines = [
      self.oled_title,
      self.oled_text1,
      self.oled_text2,
      self.oled_text3
    ]
    self.oled_title.textChanged.connect(lambda: self.__adjustText(0))
    self.oled_text1.textChanged.connect(lambda: self.__adjustText(1))
    self.oled_text2.textChanged.connect(lambda: self.__adjustText(2))
    self.oled_text3.textChanged.connect(lambda: self.__adjustText(3))
  
  def __adjustText(self, id: int):
    if self.__is_adjusting_text_flag:
      return
    self.__is_adjusting_text_flag = True

    content = self.__lines[id].toPlainText()[0:17]
    if len(content) > 16:
      content = content[0:16]
    
    if "\n" in content:
      index = content.find("\n")
      content = content[:index] + content[index+1:]
    
    self.__lines[id].clear()
    self.__lines[id].insertPlainText(content)

    self.__is_adjusting_text_flag = False
  
  def getLines(self):
    return [
      self.__lines[0].toPlainText(),
      self.__lines[1].toPlainText(),
      self.__lines[2].toPlainText(),
      self.__lines[3].toPlainText()
    ]

if __name__=="__main__":
  app = QApplication(sys.argv)
  widget = OLEDEdit()
  widget.show()
  sys.exit(app.exec_())