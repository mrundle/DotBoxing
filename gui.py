# import pyQt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from mainwindow import Ui_MainWindow
from username import Ui_username
from challenge import Ui_challenge

######################################################################
#
#	PyQT GUI
#	------------------------------------------------------------------
#
######################################################################
class guiQT(QMainWindow, Ui_MainWindow):
	def __init__(self,protocol,parent=None):
		self.protocol = protocol
		super(guiQT, self).__init__()
		self.setWindowTitle("DotBoxing")
		QMainWindow.__init__(self,parent)
		self.setupUi(self)
		self.setWindowTitle("DotBoxing!")

		# Initialize the username input popup
		self.idBox = usernamePopup()
		self.idBox.show()
		# Initialize the challenge popup
		self.challengeBox = challengePopup()
		self.challengeBox.hide()

		# CONNECTIONS
		# Connect signals from protocol
		self.protocol.chatSignal.connect(self.addToChat) # connects to "label"
		self.protocol.userUpdateSignal.connect(self.updateUserLists)
		self.protocol.challengeSignal.connect(self.receiveChallenge)
		#self.protocol.identifySignal.connect(self.identify) # deprecated
		self.protocol.reidentifySignal.connect(self.reidentify)
		# Connect button clicks
		self.challengeButton.clicked.connect(self.challengeUser)
		self.chatEdit.returnPressed.connect(self.sendChatMessage)
		# idBox
		self.idBox.yesButton.clicked.connect(self.sendUsername)
		self.idBox.noButton.clicked.connect(self.close)
		self.idBox.lineEdit.returnPressed.connect(self.sendUsername)
		# challengeBox
		self.challengeBox.acceptButton.clicked.connect(self.acceptChallenge)
		self.challengeBox.rejectButton.clicked.connect(self.rejectChallenge)

	# Update the online and available lists
	def updateUserLists(self,inputString):
		data = str(inputString).split(':')
		online = data[0].rstrip('+').split('+')
		available = data[1].rstrip('+').split('+')
		# populate the online user list
		self.onlineList.clear()
		for user in online:
			self.onlineList.addItem(user)
		# populate the available user list
		self.availableList.clear()
		for user in available:
			self.availableList.addItem(user)

	def challengeUser(self):
		if self.protocol.inGame == False:
			if self.availableList.currentItem != None:
				userToChallenge = str(self.availableList.currentItem().text())
				if userToChallenge.lstrip().rstrip() == self.protocol.username:
					self.chatList.addItem("You cannot challenge yourself!")
					return
				else:
					self.chatList.addItem("Challenging " + userToChallenge)
					self.protocol.inGame = True
					self.protocol.transport.write("challenge:" + userToChallenge)
			else:
				self.chatList.addItem("Error: Please restart the program and log in.")
		else:
			self.chatList.addItem("Already either in a game or waiting for a game.")

	def sendChatMessage(self):
		toSend = str(self.chatEdit.text()).lstrip().rstrip()
		self.chatEdit.clear()
		self.protocol.transport.write("chat:" + toSend)

	def addToChat(self,msg):
		msg = str(msg)
		self.chatList.addItem(msg)
		self.chatList.scrollToBottom()

	def receiveChallenge(self,user):
		#self.idBox.setText("Accept challenge from " + user + "?")
		#self.challengeText.show()
		#self.yesButton.show()
		#self.noButton.show()
		#TODO HANDLE CHALLENGE RECEIVED!!!!
		user = str(user)
		if user == self.protocol.username:
			self.protocol.inGame = False
			self.chatList.addItem("Rejected self-challenge.")
		else:
			self.protocol.challenger = user
			self.challengeBox.label.setText("You've been challenged by " + user)
			self.challengeBox.show()

	def acceptChallenge(self):
		self.challengeBox.hide()
		self.protocol.transport.write("confirmChallenge:" + self.protocol.username + ":" + self.protocol.challenger)

	def rejectChallenge(self):
		self.challengeBox.hide()
		self.protocol.transport.write("rejectChallenge:" + self.protocol.challenger)

	def sendUsername(self):
		self.idBox.hide()
		username = str(self.idBox.lineEdit.text())
		self.protocol.username = username
		self.usernameLable.setText(username + " >>")
		self.protocol.transport.write("id:" + username)
		
	def reidentify(self):
		self.idBox.label.setText("Username taken, try again:")
		self.idBox.show()
	
	def closeEvent(self, event):
		self.idBox.hide()
		#quit_msg = "Are you sure you want to exit the program?"
		#reply = QMessageBox.question(self, 'Message', 
		#                 quit_msg, QMessageBox.Yes, QMessageBox.No)
		#if reply == QMessageBox.Yes:
		#self.protocol.guiExit()
		event.accept()
		#else:
		#    event.ignore()

class usernamePopup(QDialog, Ui_username):
	def __init__(self,parent=None):
		QDialog.__init__(self,parent)
		self.setupUi(self)

class challengePopup(QDialog, Ui_challenge):
	def __init__(self,parent=None):
		QDialog.__init__(self,parent)
		self.setupUi(self)
