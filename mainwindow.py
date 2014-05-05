# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created: Mon May  5 14:12:54 2014
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(510, 561)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.availableList = QtGui.QListWidget(self.centralwidget)
        self.availableList.setObjectName("availableList")
        self.gridLayout.addWidget(self.availableList, 1, 0, 2, 1)
        self.challengeButton = QtGui.QPushButton(self.centralwidget)
        self.challengeButton.setObjectName("challengeButton")
        self.gridLayout.addWidget(self.challengeButton, 1, 1, 1, 1)
        self.randomGameButton = QtGui.QPushButton(self.centralwidget)
        self.randomGameButton.setObjectName("randomGameButton")
        self.gridLayout.addWidget(self.randomGameButton, 2, 1, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.chatList = QtGui.QListWidget(self.centralwidget)
        self.chatList.setEnabled(True)
        self.chatList.setAutoScroll(True)
        self.chatList.setObjectName("chatList")
        self.gridLayout.addWidget(self.chatList, 5, 0, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.usernameLable = QtGui.QLabel(self.centralwidget)
        self.usernameLable.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.usernameLable.setTextFormat(QtCore.Qt.PlainText)
        self.usernameLable.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.usernameLable.setObjectName("usernameLable")
        self.horizontalLayout.addWidget(self.usernameLable)
        self.chatEdit = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chatEdit.sizePolicy().hasHeightForWidth())
        self.chatEdit.setSizePolicy(sizePolicy)
        self.chatEdit.setMinimumSize(QtCore.QSize(258, 0))
        self.chatEdit.setObjectName("chatEdit")
        self.horizontalLayout.addWidget(self.chatEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 6, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 7, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 7, 1, 1, 1)
        self.onlineList = QtGui.QListWidget(self.centralwidget)
        self.onlineList.setEnabled(False)
        self.onlineList.setObjectName("onlineList")
        self.gridLayout.addWidget(self.onlineList, 4, 0, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 6, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 510, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Available", None, QtGui.QApplication.UnicodeUTF8))
        self.challengeButton.setText(QtGui.QApplication.translate("MainWindow", "Challenge User", None, QtGui.QApplication.UnicodeUTF8))
        self.randomGameButton.setText(QtGui.QApplication.translate("MainWindow", "Random Game", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Online", None, QtGui.QApplication.UnicodeUTF8))
        self.usernameLable.setText(QtGui.QApplication.translate("MainWindow", ">>", None, QtGui.QApplication.UnicodeUTF8))

