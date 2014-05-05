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

# import gui
from gui import guiQT

# import QtCore for Qt objects and signals
from PyQt4.QtCore import *
from PyQt4.QtGui import *

SERVER_HOST = 'student01.cse.nd.edu'   # (global) should be whatever host server.py is running on
SERVER_PORT = 40035        # (global) should match the server.py file

quitting = False           # to prevent notifying the user of disconnection when they exit
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
	#identifySignal   = pyqtSignal() # deprecated
	reidentifySignal = pyqtSignal()
	
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
		
	def connectionMade(self):
		print "Connected to server."
		# Start the GUI
		self.startGUI()

	def startGUI(self):
		# Start the GUI
		thread = threading.Thread(target = run_gui, args = (self,))
		thread.daemon = True
		thread.start()

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

		elif (data[0] == 'reidentify'):
			# Handled in GUI
			self.reidentifySignal.emit()

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

	# Game should only be initialized after 
	# opponents have been assigned and match has been made
	def initializeGame(self):
		# import GameSpace instance
		print "Initializing game instance..."
		reactor.gs = GameSpace(reactor)
		print "Game instance initialized."
		reactor.gs.protocol = self
		# start game loop
		self.lc = LoopingCall(self.runGameLoop)
		self.lc.start(1/60)

	

	def dataReceived(self, data):
		self.queue.put(data)

	def queueData(self,data):
		data = data.rstrip()
		self.handleData(data)
		self.queue.get().addCallback(self.queueData)

	def startQueuing(self):
		self.queue.get().addCallback(self.queueData)

	def runGameLoop(self):
		retValue = reactor.gs.loop()
		if retValue == "GameOver":
			reactor.gs.Quit()
			self.lc.stop()

	def guiExit(self):
		quitting = True
		self.transport.loseConnection()
		reactor.stop()
		return

def run_gui(protocol=None):
	app = QApplication(sys.argv)
	_gui = guiQT(protocol,None)
	_gui.show()
	app.exec_()
	protocol.guiExit()

class ServerClientFactory(ReconnectingClientFactory):
	def buildProtocol(self,addr):
		return Server()
	def clientConnectionLost(self,connector, reason):
		if quitting == False:
			print "Lost connection to server. Attempting to reconnect..."
			ReconnectingClientFactory.clientConnectionLost(self,connector, reason)
		else:
			print "Goodbye."
	def clientConnectionFailed(self,connector,reason):
		print "Cannot connect to server. Attempting to reconnect..."
		ReconnectingClientFactory.clientConnectionLost(self,connector, reason)

def main():
	# connect to server
	reactor.connectTCP(SERVER_HOST, SERVER_PORT, ServerClientFactory())
	reactor.run()

if __name__ == "__main__":
	main()
