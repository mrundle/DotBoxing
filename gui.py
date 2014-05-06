# DotBoxing PyQt GUI Code
# Matt Mahan and Matt Rundle
# Programming Paradigms PyGameTwisted Project

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from mainwindow import Ui_MainWindow
from username import Ui_username
from challenge import Ui_challenge

class guiQT(QMainWindow, Ui_MainWindow):

	def __init__(self,protocol,parent=None):
		super(guiQT, self).__init__()
		# Set up user interface
		self.setupUi(self)

		# Twisted protocol for sending messages to server
		self.protocol = protocol
		
		self.setWindowTitle("DotBoxing!")

		# Initialize the username input popup dialogue
		self.idBox = usernamePopup()
		self.idBox.show()

		# Initialize the challenge popup dialogue
		self.challengeBox = challengePopup()
		self.challengeBox.hide()

		# Connect signals from protocol (defined in client.py)
		self.protocol.chatSignal.connect(self.addToChat)
		self.protocol.userUpdateSignal.connect(self.updateUserLists)
		self.protocol.challengeSignal.connect(self.receiveChallenge)
		self.protocol.reidentifySignal.connect(self.reidentify)

		# Connect button clicks
		self.challengeButton.clicked.connect(self.challengeUser)
		self.chatEdit.returnPressed.connect(self.sendChatMessage)
		self.randomGameButton.clicked.connect(self.randomGame)

		# idBox connections
		self.idBox.yesButton.clicked.connect(self.sendUsername)
		self.idBox.noButton.clicked.connect(self.close)
		self.idBox.lineEdit.returnPressed.connect(self.sendUsername)

		# challengeBox connections
		self.challengeBox.acceptButton.clicked.connect(self.acceptChallenge)
		self.challengeBox.rejectButton.clicked.connect(self.rejectChallenge)

	# Update the online and available lists
	def updateUserLists(self,inputString):
		# comes in the form of two lists, each list delineated with '+' symbols
		# between elements. The two lists are delineated with ':' marks. For example:
		#    onlineUser1+onlineUser2+onlineUser3+onlineUser4+:availableUser1+availableUser2+
		data = str(inputString).split(':')
		# Remove trailing "+" from both lists, and split by "+" into arrays
		online = data[0].rstrip('+').split('+')
		available = data[1].rstrip('+').split('+')
		# Clear the existing GUI lists to prepare for repopulation
		self.onlineList.clear()
		self.availableList.clear()
		# Populate the online user list
		if data[0] != '':
			for user in online:
				self.onlineList.addItem(user)
		# populate the available user list
		if data[1] != '':
			for user in available:
				self.availableList.addItem(user)

	# The user has clicked the challenge button and is trying to challenge
	# the user that is selected from the "available" GUI list element.
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
					# Send a message to the server in the form of:
					#     challenge:<userToChallenge>
					self.protocol.transport.write("challenge:" + userToChallenge)
			else:
				# This shouldn't ever happen because you should always at least 
				# see yourself in the available queue if you aren't in a game.
				self.chatList.addItem("Error: Please restart the program and log in.")
		else:
			self.chatList.addItem("Already either in a game or waiting for a game.")

	# User has sent a chat message.
	def sendChatMessage(self):
		# Strip leading and trailing whitespace from message
		toSend = str(self.chatEdit.text()).lstrip().rstrip()
		# Clear the lineEdit box (users will expect this behavior)
		self.chatEdit.clear()
		# Send message to server in the form of:
		#    chat:<chat text to send>
		self.protocol.transport.write("chat:" + toSend)

	# Incoming message, triggered by a signal from the protocol in client.py
	def addToChat(self,msg):
		msg = str(msg)
		self.chatList.addItem(msg)
		self.chatList.scrollToBottom()

	# Received a challenge from another user
	def receiveChallenge(self,user):
		user = str(user)
		if user == self.protocol.username:
			self.protocol.inGame = False
			self.chatList.addItem("Rejected self-challenge.")
		else:
			# We don't want to handle challenges if we're already in a game
			if self.protocol.inGame == False:
				self.protocol.challenger = user
				self.challengeBox.label.setText("You've been challenged by " + user)
				self.challengeBox.show()
			else:
				# Automatically reject the challenge via server message:
				#    rejectChallenge:<userWhoChallenged>
				self.protocol.transport.write("rejectChallenge:" + user)

	# Accept a challenge from a user
	def acceptChallenge(self):
		self.challengeBox.hide()
		self.protocol.transport.write("confirmChallenge:" + self.protocol.username + ":" + self.protocol.challenger)

	# Reject a challenge from a user
	def rejectChallenge(self):
		self.challengeBox.hide()
		self.protocol.transport.write("rejectChallenge:" + self.protocol.challenger)

	# Identify to the server, and set appropriate variables
	def sendUsername(self):
		self.idBox.hide()
		username = str(self.idBox.lineEdit.text())
		self.protocol.username = username
		self.usernameLable.setText(username + " >>")
		self.protocol.transport.write("id:" + username)
	
	# Username is already taken, need to reidentify
	def reidentify(self):
		self.idBox.label.setText("Username either taken or invalid, try again:")
		self.idBox.show()

	# User wants to wait for a random matchup
	def randomGame(self):
		if self.protocol.inGame == False:
			self.protocol.transport.write("getGame")
			self.chatList.addItem("Waiting for opponent...")
		else:
			self.chatList.addItem("You are already in a game.")
	
	# Triggered by window closing
	def closeEvent(self, event):
		self.idBox.hide()
		event.accept()

class usernamePopup(QDialog, Ui_username):
	def __init__(self,parent=None):
		QDialog.__init__(self,parent)
		self.setupUi(self)

class challengePopup(QDialog, Ui_challenge):
	def __init__(self,parent=None):
		QDialog.__init__(self,parent)
		self.setupUi(self)
