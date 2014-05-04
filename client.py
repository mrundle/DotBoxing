# DotBoxing Client Code
# Matt Mahan and Matt Rundle
# Programming Paradigms PyGameTwisted Project

# import pygame gamespace
from dotboxing import GameSpace

# import networking
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.task import LoopingCall
from twisted.internet.defer import DeferredQueue

# import system stuff
import os, sys
import threading

# import pyQt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from mainwindow import Ui_MainWindow

SERVER_HOST = 'localhost'   # (global) should be whatever host server.py is running on
SERVER_PORT = 40035        # (global) should match the server.py file

######################################################################
#
#	SERVER PROTOCOL CLASS
#	------------------------------------------------------------------
#	- Handles the connection with the server
#	- Instantiates a PyQt GUI which mediates user/server interaction
#		- Note: the GUI is passed a reference of this protocol
######################################################################
class Server(Protocol,QObject):
	# Set up signals (THESE WILL BE USED BY GUI)
	chatSignal       = pyqtSignal(QString)
	userUpdateSignal = pyqtSignal(QString)
	challengeSignal  = pyqtSignal(QString)
	
	def __init__(self):
		# initialize vars
		self.username = ''
		self.opponent = ''
		self.inGame = False
		self.challenger = ''
		# Make sure Protocol.__init__() and QObject.__init__() get called
		super(Server, self).__init__()
		# initialize queue
		self.queue = DeferredQueue()
		self.startQueuing()
		# Start the GUI
		thread = threading.Thread(target = run_gui, args = (self,))
		thread.daemon = True
		thread.start()

	def connectionMade(self):
		print "Connected to server."

	def handleData(self, msg):
		#### DEBUG ####
		#toSend = ">>debug: " + msg
		#self.chatSignal.emit(toSend)
		#### DEBUG ####

		data = msg.split(':')
		if (data[0] == 'opponent'):
			print data
			# This will come in the form of "opponent:<username>:<1|2|...|n>", where the last
			# argument indicates the order of turn
			self.inGame = True
			self.opponent = data[1]
			print "Matched to opponent: " + self.opponent
			print "Initializing game between " + self.username + " and " + self.opponent
			self.initializeGame()
			# tell the game who's turn it is
			turn = data[2]
			if turn == "1":
				print "It is my turn."
				reactor.gs.turn = "Mine"
			else:
				print "It is not my turn."
				reactor.gs.turn = "Other"

		if (data[0] == 'reject'):
			self.inGame = False
			self.chatSignal.emit("Game rejected")

		if (data[0] == 'identify'):
			# identify to server
			self.username = self.identify("identify")		
			msg = "id:" + self.username
			self.transport.write(msg)

		elif (data[0] == 'reidentify'):
			# username already taken, try again
			self.username = self.identify("reidentify")
			msg = "id:" + self.username
			self.transport.write(msg)

		elif (data[0] == 'challenge'):
			# the user has received a challenge
			self.challenger = data[1]
			self.chatSignal.emit("SERVER MESSAGE: You have received a challenge from " + data[1])
			self.challengeSignal.emit(data[1])

		elif (data[0] == 'idConfirmed'):
			msg = "SERVER MESSAGE: Username \"" + self.username + "\" confirmed."
			self.chatSignal.emit(msg)

		elif (data[0] == 'opponentMove'):
			moveID = data[1]
			reactor.gs.opponentMove(moveID)

		elif (data[0] == 'users' and data[2] == 'available'):
			userList = data[1]
			availableList = data[3]
			self.userUpdateSignal.emit(userList + ":" + availableList)

		# This is for general messages from the server
		elif (data[0] == 'msg'):
			msg = "SERVER MESSAGE: " + data[1]
			self.chatSignal.emit(msg)

		elif (data[0] == 'chat'):
			self.chatSignal.emit(data[1])

		else:
			# data was receieved but was unable to be interpreted
			pass

	def sendMove(self,moveID):
		# send move to the opponent
		self.transport.write("move:" + self.opponent + ":" + moveID)

	def identify(self, msg):
		# identify to server (pick username)
		msg = msg.rstrip()
		if msg == "identify":
			# initial prompt
			return raw_input("Enter a username: ")
		elif msg == "reidentify":
			# username already taken
			return raw_input("Name already taken. Enter a username: ")

	# Game should only be initialized after 
	# opponents have been assigned and match has been made
	def initializeGame(self):
		# import GameSpace instance
		print "Initializing game instance..."
		reactor.gs = GameSpace(reactor)
		print "Game instance initialized."
		reactor.gs.protocol = self
		# start game loop
		lc = LoopingCall(reactor.gs.loop)
		lc.start(1/60)

	

	def dataReceived(self, data):
		self.queue.put(data)

	def queueData(self,data):
		data = data.rstrip()
		self.handleData(data)
		self.queue.get().addCallback(self.queueData)

	def startQueuing(self):
		self.queue.get().addCallback(self.queueData)
	
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

		# initially hide the challenge stuff
		self.challengeText.hide()
		self.yesButton.hide()
		self.noButton.hide()

		# CONNECTIONS
		# Connect signals from protocol
		self.protocol.chatSignal.connect(self.addToChat) # connects to "label"
		self.protocol.userUpdateSignal.connect(self.updateUserLists)
		self.protocol.challengeSignal.connect(self.receiveChallenge)
		# Connect button clicks
		self.challengeButton.clicked.connect(self.challengeUser)
		self.chatEdit.returnPressed.connect(self.sendChatMessage)
		self.yesButton.clicked.connect(self.acceptChallenge)
		self.noButton.clicked.connect(self.rejectChallenge)

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
			userToChallenge = str(self.availableList.currentItem().text())
			if userToChallenge == self.protocol.username:
				self.chatList.addItem("You cannot challenge yourself!")
				return
			else:
				self.chatList.addItem("Challenging " + userToChallenge)
				self.protocol.inGame = True
				self.protocol.transport.write("challenge:" + userToChallenge)
		else:
			self.chatList.addItem("Already either in a game or waiting for a game.")

	def sendChatMessage(self):
		toSend = str(self.chatEdit.text()).lstrip().rstrip()
		self.chatEdit.clear()
		self.protocol.transport.write("chat:" + toSend)

	def addToChat(self,msg):
		self.chatList.addItem(msg)
		self.chatList.scrollToBottom()

	def receiveChallenge(self,user):
		self.challengeText.setText("Accept challenge from " + user + "?")
		self.challengeText.show()
		self.yesButton.show()
		self.noButton.show()

	def acceptChallenge(self):
		self.challengeText.hide()
		self.yesButton.hide()
		self.noButton.hide()
		self.protocol.transport.write("confirmChallenge:" + self.protocol.username + ":" + self.protocol.challenger)

	def rejectChallenge(self):
		self.protocol.transport.write("rejectChallenge:" + self.protocol.challenger)
		self.challengeText.hide()
		self.yesButton.hide()
		self.noButton.hide()



def run_gui(protocol=None):
	app = QApplication(sys.argv)
	_gui = guiQT(protocol,None)
	_gui.show()
	app.exec_()
	return

class ServerClientFactory(ReconnectingClientFactory):
	def buildProtocol(self,addr):
		return Server()
	def clientConnectionLost(self,connector, reason):
		print "Lost connection to server. Attempting to reconnect..."
		ReconnectingClientFactory.clientConnectionLost(self,connector, reason)
	def clientConnectionFailed(self,connector,reason):
		print "Cannot connect to server. Attempting to reconnect..."
		ReconnectingClientFactory.clientConnectionLost(self,connector, reason)

def main():

	# connect to server
	reactor.connectTCP(SERVER_HOST, SERVER_PORT, ServerClientFactory())
	
	reactor.run()

if __name__ == "__main__":
	main()
