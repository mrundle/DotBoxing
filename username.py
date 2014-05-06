# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/username.ui'
#
# Created: Tue May  6 12:02:09 2014
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_username(object):
    def setupUi(self, username):
        username.setObjectName("username")
        username.resize(303, 115)
        username.setStyleSheet("background-color: rgb(117,38,39)")
        self.gridLayout = QtGui.QGridLayout(username)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtGui.QLineEdit(username)
        self.lineEdit.setStyleSheet("background-color: rgb(237,242,201)")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 0, 1, 1)
        self.label = QtGui.QLabel(username)
        font = QtGui.QFont()
        font.setFamily("Liberation Sans")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255,255,255)")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.yesButton = QtGui.QPushButton(username)
        font = QtGui.QFont()
        font.setFamily("Liberation Sans")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.yesButton.setFont(font)
        self.yesButton.setStyleSheet("background-color: rgb(237,242,201)")
        self.yesButton.setObjectName("yesButton")
        self.horizontalLayout.addWidget(self.yesButton)
        self.noButton = QtGui.QPushButton(username)
        font = QtGui.QFont()
        font.setFamily("Liberation Sans")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.noButton.setFont(font)
        self.noButton.setStyleSheet("background-color: rgb(237,242,201)")
        self.noButton.setObjectName("noButton")
        self.horizontalLayout.addWidget(self.noButton)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 1)

        self.retranslateUi(username)
        QtCore.QMetaObject.connectSlotsByName(username)

    def retranslateUi(self, username):
        username.setWindowTitle(QtGui.QApplication.translate("username", "Identify Yourself", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("username", "Enter a username:", None, QtGui.QApplication.UnicodeUTF8))
        self.yesButton.setText(QtGui.QApplication.translate("username", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.noButton.setText(QtGui.QApplication.translate("username", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

