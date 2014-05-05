# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/challenge.ui'
#
# Created: Mon May  5 14:12:55 2014
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_challenge(object):
    def setupUi(self, challenge):
        challenge.setObjectName("challenge")
        challenge.resize(376, 134)
        self.gridLayout = QtGui.QGridLayout(challenge)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(challenge)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.acceptButton = QtGui.QPushButton(challenge)
        self.acceptButton.setObjectName("acceptButton")
        self.gridLayout.addWidget(self.acceptButton, 1, 1, 1, 1)
        self.rejectButton = QtGui.QPushButton(challenge)
        self.rejectButton.setObjectName("rejectButton")
        self.gridLayout.addWidget(self.rejectButton, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 3, 1, 1)

        self.retranslateUi(challenge)
        QtCore.QMetaObject.connectSlotsByName(challenge)

    def retranslateUi(self, challenge):
        challenge.setWindowTitle(QtGui.QApplication.translate("challenge", "Challenge!", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("challenge", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.acceptButton.setText(QtGui.QApplication.translate("challenge", "Accept", None, QtGui.QApplication.UnicodeUTF8))
        self.rejectButton.setText(QtGui.QApplication.translate("challenge", "Reject", None, QtGui.QApplication.UnicodeUTF8))

