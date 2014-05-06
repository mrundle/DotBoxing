# DotBoxing Client Code
# Matt Mahan and Matt Rundle
# Programming Paradigms PyGameTwisted Project

SERVER_HOST = 'student01.cse.nd.edu'   # (global) should be whatever host server.py is running on
SERVER_PORT = 40035                    # (global) should match the server.py file

# system stuff
import os, sys
import threading
# import pygame gamespace
from dotboxing import GameSpace
# networking
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet.task import LoopingCall
from twisted.internet.defer import DeferredQueue
# gui
from gui import guiQT
# QtCore for Qt objects and signals
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Server(Protocol,QObject):

	# Initialize PyQt Signals
	#    For some godforsaken reason, these are necessarily declared within
	#    the class scope but outside the __init__() function. It doesn't
	#    work otherwise.
	chatSignal       = pyqtSignal(QString)
	userUpdateSignal = pyqtSignal(QString)
	challengeSignal  = pyqtSignal(QString)
	reidentifySignal = pyqtSignal()
	
	def __init__(self):
		# Make sure Protocol.__init__() and QObject.__init__() get called (double inheritance)
		super(Server, self).__init__()
		# initialize vars
		self.username = ''
		self.opponent = ''
		self.inGame = False
		self.challenger = ''
		# initialize queue
		self.queue = DeferredQueue()
		# initialize the incoming data queue
		self.startQueuing()
		self.quitting = False # to prevent notifying the user of disconnection when they exit
		
	# Called by reactor upon connection
	def connectionMade(self):
		self.startGUI()

	# Starts the PyQt GUI which will handle user input and ouptut
	def startGUI(self):
		thread = threading.Thread(target = run_gui, args = (self,))
		thread.daemon = True  # Thread will die when calling process dies
		thread.start()

	# Called by reactor when TCP packet received over this connection
	def dataReceived(self, data):
		self.queue.put(data)

	# Continuously grabs data from the 
	def queueData(self,data):
		data = data.rstrip()
		self.handleData(data)
		self.queue.get().addCallback(self.queueData)

	# Kicks off the queueData loop
	def startQueuing(self):
		self.queue.get().addCallback(self.queueData)
	
	# Handle data sent by the server
	def handleData(self, msg):

		# Server messages come colon-delineated:
		# <element>:<element>:<element>:<element>
		data = msg.split(':')
		cmmd = data[0]

		if (cmmd == 'opponent'):
			# Server is telling you to start a game with another user.
			# This will come in the form of: 
			#    "opponent:<username>:<1|2|...|n>"
			# where the last argument indicates the order of turn
			self.inGame = True
			self.opponent = data[1]
			self.challenger = data[1]
			# Update "Available" list to all users
			self.transport.write("refresh:null")
			# Start the game
			self.initializeGame()
			# tell the game who's turn it is
			turn = data[2]
			if turn == "1":
				reactor.gs.turn = "Mine"
			else:
				reactor.gs.turn = "Other"

		if (cmmd == 'reject'):
			# Someone has rejected your game challenge:
			#    reject:null
			self.inGame = False
			# Notify user in GUI chat box
			self.chatSignal.emit("Game rejected")

		elif (cmmd == 'reidentify'):
			self.reidentifySignal.emit() # This signal picked up by GUI

		elif (cmmd == 'challenge'):
			# Challenge receieved from another user
			#    challenge:<fromUserID>
			if self.inGame == False:
				self.challenger = data[1]
				# Notify user in GUI chat box
				self.chatSignal.emit("SERVER MESSAGE: You have received a challenge from " + data[1])
				# Prompt response from user via GUI
				self.challengeSignal.emit(data[1])

		elif (cmmd == 'opponentMove'):
			# Opponent has made a move; pass to game:
			#    opponentMove:<moveID>
			moveID = data[1]
			reactor.gs.opponentMove(moveID)

		elif (cmmd == 'forfeit'):
			# Opponent has forfeited the game
			#    forfeit:null
			# Notify the user via GUI chat box
			self.chatSignal.emit("SERVER MESSAGE: " + self.challenger + " forfeited.")
			self.inGame = False
			# Quietly exit the game (we already know the result - game shouldn't announce it)
			reactor.gs.quietQuit()
			# Since the 'forfeit' command from the other user triggered the server to set
			# both users (self and opponent) to available again, we need to send a global
			# refresh to reflect these changes
			self.transport.write("refresh:null")

		elif (cmmd == 'winner'):
			# Opponent has notified you that you have won your game
			self.chatSignal.emit("You won against " + self.challenger + "!")
			self.inGame = False
			# Tell the server that both you and your opponent are now available
			self.transport.write("available:" + self.username + ":" + self.challenger)
			# Quietly exit the game (we already know the result - game shouldn't announce it)
			reactor.gs.quietQuit()

		elif (cmmd == 'loser'):
			# Opponent has notified you that you have lost your game
			self.chatSignal.emit("You lost against " + self.challenger + ".")
			self.inGame = False
			# Tell the server that both you and your opponent are now available
			self.transport.write("available:" + self.username + ":" + self.challenger)
			# Quietly exit the game (we already know the result - game shouldn't announce it)
			reactor.gs.quietQuit()

		elif (cmmd == 'tied'):
			# Opponent has notified you that you have tied your game
			self.chatSignal.emit("You tied " + self.challenger + ".")
			self.inGame = False
			# Tell the server that both you and your opponent are now available
			self.transport.write("available:" + self.username + ":" + self.challenger)
			# Quietly exit the game (we already know the result - game shouldn't announce it)
			reactor.gs.quietQuit()

		elif (cmmd == 'users' and data[2] == 'available'):
			# The server is sending a list of Online and Available users:
			#     users:<u1+u2+u3+u4>:available:<u1+u2>
			# Note: user lists are '+' delineated
			userList = data[1]
			availableList = data[3]
			# Simply pass these lists (no parsing yet) to the GUI,
			# delineated with a colon between the two
			self.userUpdateSignal.emit(userList + ":" + availableList)

		elif (cmmd == 'msg'):
			# This is a general server message to the user:
			#     msg:<msg_string>
			# Simply pass it along to the GUI for display in the chat box,
			# after we prepend it with a special server stamp.
			msg = "SERVER MESSAGE: " + data[1]
			self.chatSignal.emit(msg)

		elif (cmmd == 'chat'):
			# Incoming chat message from another user (via the server)
			# Simply pass it to the GUI via the chatSignal
			msg = data[1]
			self.chatSignal.emit(msg)

		else:
			# data was receieved but was unable to be interpreted
			print "Received unrecognized message from server: " + msg

	# This function will be called by the PyGame instance,
	# and will notify the server of a game move like so:
	#     move:<opponent_username>:<move_id>
	def sendMove(self,moveID):
		self.transport.write("move:" + self.opponent + ":" + moveID)

	# Start the pygame instance
	def initializeGame(self):
		# Initialize the GameSpace.
		# Reactor needs to be passed to it so it can issue server calls.
		reactor.gs = GameSpace(reactor)
		# GameSpace also needs this protocol to issue server calls.
		reactor.gs.protocol = self
		# Start game loop
		self.lc = LoopingCall(reactor.gs.loop)
		self.lc.start(1/60)

	# Called by a PyGame instance (into which we had passed a
	# reference to this protocol.)
	def gameEnded(self,msg):
		self.inGame = False
		msg = msg.rstrip()    # remove any pesky trailing whitespace
		# Notify server (and, by extension, the opponent) that the game has ended, and how it has
		#    Note: 'msg' will be either "forfeit", "won", "lost", or "tied"
		self.transport.write(msg + ":" + self.challenger)
		# Write end game condition to the GUI chatbox
		if msg == "forfeit":
			self.chatSignal.emit("You forfeited the game against " + self.challenger + ".")
		elif msg == "won":
			self.chatSignal.emit("You won against " + self.challenger + "!")
		elif msg == "lost":
			self.chatSignal.emit("You lost against " + self.challenger + ".")
		elif msg == "tied":
			self.chatSignal.emit("You tied " + self.challenger + ".")

	# After the GUI exits, we want the program to exit as well
	def guiExit(self):
		self.quitting = True
		self.transport.loseConnection()
		reactor.stop()
		return

# Run the GUI (takes a protocol as an argument)
def run_gui(protocol=None):
	app = QApplication(sys.argv)
	_gui = guiQT(protocol,None)
	_gui.show()
	app.exec_()
	# Notify the protocol that the GUI has exited
	# (triggering exit from program)
	protocol.guiExit()

# Simply builds the Server protocol 
class ServerClientFactory(ClientFactory):
	def buildProtocol(self,addr):
		return Server()

def main():
	# connect to server
	reactor.connectTCP(SERVER_HOST, SERVER_PORT, ServerClientFactory())
	reactor.run()

if __name__ == "__main__":
	main()
