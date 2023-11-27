# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'shell_windowIuaFrP.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_ShellWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(692, 399)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.shellBox = QGroupBox(self.centralwidget)
        self.shellBox.setObjectName(u"shellBox")
        self.shellBox.setGeometry(QRect(10, 29, 671, 351))
        self.output = QPlainTextEdit(self.shellBox)
        self.output.setObjectName(u"output")
        self.output.setGeometry(QRect(10, 20, 651, 301))
        self.input = QLineEdit(self.shellBox)
        self.input.setObjectName(u"input")
        self.input.setGeometry(QRect(10, 330, 651, 20))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.shellBox.setTitle(QCoreApplication.translate("MainWindow", u"Serial Monitor", None))
    # retranslateUi

