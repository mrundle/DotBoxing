# DotBoxing Client Code
# Matt Mahan and Matt Rundle
# Programming Paradigms PyGameTwisted Project

# import pygame gamespace
from dotboxing import GameSpace

# import networking
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.task import LoopingCall

# import system stuff
import os, sys
import threading

# import pyQt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from mainwindow import Ui_MainWindow

SERVER_HOST = 'localhost'   # (global) should be whatever host server.py is running on
SERVER_PORT = 40035        # (global) should match the server.py file


class Server(Protocol,QObject):
	# Set up signals (THESE WILL BE USED BY GUI)
	chatSignal      = pyqtSignal(QString)
	availableSignal = pyqtSignal(QString)
	onlineSignal    = pyqtSignal(QString)
	
	def __init__(self):
		# . . .
		# initialize vars
		self.username = ''
		self.opponent = ''
		self.beingChallenged = False
		self.challenger = ''
		# Make sure Protocol.__init__() and QObject.__init__() get called
		super(Server, self).__init__()
		# Start the GUI
		thread = threading.Thread(target = run_gui, args = (self,))
		thread.daemon = True
		thread.start()

	def connectionMade(self):
		print "Connected to server."

	def dataReceived(self, msg):
		msg = msg.rstrip()

		#### DEBUG ####
		toSend = ">>debug: " + msg
		self.chatSignal.emit(toSend)
		#### DEBUG ####

		data = msg.split(':')
		if (data[0] == 'opponent'):
			print data
			# This will come in the form of "opponent:<username>:<1|2|...|n>", where the last
			# argument indicates the order of turn
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
			os.system('clear')
			print "SERVER MESSAGE: You have received a challenge from " + data[1]

		elif (data[0] == 'idConfirmed'):
			msg = "SERVER MESSAGE: Username \"" + self.username + "\" confirmed."
			self.chatSignal.emit(msg)
			self.lobby(msg)	

		elif (data[0] == 'opponentMove'):
			moveID = data[1]
			reactor.gs.opponentMove(moveID)

		elif (data[0] == 'online'):
			userList = data[1]
			self.onlineSignal.emit(userList)

		elif (data[0] == 'available'):
			userList = data[1]
			self.availableSignal.emit(userList)

		# This is for general messages from the server
		# Simply print them and go back to the lobby
		elif (data[0] == 'msg'):
			msg = "SERVER MESSAGE: " + data[1]
			self.chatSignal.emit(msg)
			self.lobby(data[1])

		else:
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

	def lobby(self,msg=None):
		os.system('clear')
		if msg != None:
			msg = msg.rstrip(',')
			print "\nSERVER MESSAGE: " + msg + "\n"
		print_guide()
		while 1:
			# check the transport
			#
			uinput = raw_input("> ").rstrip()
			elements = uinput.split(' ')
			command  = elements[0]
			if   command == "help":
				os.system('clear')
				print_commands()
			elif command == '1':
				# view available users
				self.transport.write("viewAvailable")
				return
			elif command == '2':
				# view online users
				self.transport.write("viewOnline")
				return
			elif command == '3':
				# challenge another user
				if len(elements) == 2:
					toChallenge = elements[1]
					print "Waiting for response..."
					self.transport.write("challenge:" + toChallenge)
					return
				else:
					print "Invalid command."
			elif command == '4':
				print "Waiting for match..."
				self.transport.write("getGame")

class ServerClientFactory(ReconnectingClientFactory):

	def buildProtocol(self,addr):
		#lobby = threading.Thread(target=self.lobby, args=None)
		#lobby.daemon = True
		#lobby.start
		# PASS THE LOBBY THE PROTOCOL
		return Server()

	def clientConnectionLost(self,connector, reason):
		#print "Lost connection to server.. Reason: " + str(reason)
		print "Lost connection to server. Attempting to reconnect..."
		ReconnectingClientFactory.clientConnectionLost(self,connector, reason)
	def clientConnectionFailed(self,connector,reason):
		#print "Connection to server failed.. " + str(reason)
		print "Cannot connect to server. Attempting to reconnect..."
		ReconnectingClientFactory.clientConnectionLost(self,connector, reason)
		
def lobby_print():
	# Clear the screen
	os.system('clear')
	print "+-+-+-+ +-+-+-+-+-+-+"
	print "|D|O|T| |B|O|X|I|N|G|"
	print "+-+-+-+ +-+-+-+-+-+-+"

def print_guide():
	print "(Enter \"help\" to see commands)"
	

def print_commands():
	print "-----------------------------------"
	print "Options: \n"
	print "View available users  [1]"
	print "View online users     [2]"
	print "Challenge a user      [3] [username]"
	print "Get random game       [4]"
	print "-----------------------------------"

class guiQT(QMainWindow, Ui_MainWindow):
	def __init__(self,protocol,parent=None):
		self.protocol = protocol
		super(guiQT, self).__init__()
		self.setWindowTitle("DotBoxing")
		QMainWindow.__init__(self,parent)
		self.setupUi(self)

		# Do some connecting
		self.protocol.chatSignal.connect(self.chatList.addItem) # connects to "label"
		self.protocol.onlineSignal.connect(self.onlineList.addItem)
		self.protocol.availableSignal.connect(self.availableList.addItem)

def run_gui(protocol=None):
	app = QApplication(sys.argv)
	_gui = guiQT(protocol,None)
	_gui.show()
	#sys.exit(app.exec_())
	app.exec_()
	return

def main():
	lobby_print()

	# connect to server
	reactor.connectTCP(SERVER_HOST, SERVER_PORT, ServerClientFactory())
	
	reactor.run()

if __name__ == "__main__":
	main()
