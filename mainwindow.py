# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created: Sun May  4 13:05:09 2014
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(376, 598)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.availableList = QtGui.QListWidget(self.centralwidget)
        self.availableList.setGeometry(QtCore.QRect(10, 40, 191, 151))
        self.availableList.setObjectName("availableList")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 200, 351, 17))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 361, 17))
        self.label_2.setObjectName("label_2")
        self.challengeButton = QtGui.QPushButton(self.centralwidget)
        self.challengeButton.setGeometry(QtCore.QRect(210, 60, 151, 27))
        self.challengeButton.setObjectName("challengeButton")
        self.randomGameButton = QtGui.QPushButton(self.centralwidget)
        self.randomGameButton.setGeometry(QtCore.QRect(210, 120, 151, 27))
        self.randomGameButton.setObjectName("randomGameButton")
        self.onlineList = QtGui.QListWidget(self.centralwidget)
        self.onlineList.setGeometry(QtCore.QRect(10, 230, 351, 91))
        self.onlineList.setObjectName("onlineList")
        self.chatList = QtGui.QListWidget(self.centralwidget)
        self.chatList.setGeometry(QtCore.QRect(10, 330, 351, 211))
        self.chatList.setObjectName("chatList")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 376, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Online", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Available", None, QtGui.QApplication.UnicodeUTF8))
        self.challengeButton.setText(QtGui.QApplication.translate("MainWindow", "Challenge User", None, QtGui.QApplication.UnicodeUTF8))
        self.randomGameButton.setText(QtGui.QApplication.translate("MainWindow", "Random Game", None, QtGui.QApplication.UnicodeUTF8))

