# DotBoxing Client Code
# Matt Mahan and Matt Rundle
# Programming Paradigms PyGameTwisted Project

# import pygame gamespace
from dotboxing import GameSpace

# import networking
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.task import LoopingCall

SERVER_HOST = 'localhost'   # (global) should be whatever host server.py is running on
SERVER_PORT = 40035        # (global) should match the server.py file


class Server(Protocol):	
	def __init__(self):
		# initialize vars
		self.username = ''
		self.opponent = ''

	def connectionMade(self):
		print "Connected to server."
		

	def dataReceived(self, msg):
		print msg #debug
		msg = msg.rstrip()
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
		elif (data[0] == 'idConfirmed'):
			print "Username \"" + self.username + "\" confirmed."
			print "Waiting for game match..."
		elif (data[0] == 'opponentMove'):
			moveID = data[1]
			reactor.gs.opponentMove(moveID) 

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
	

class ServerClientFactory(ReconnectingClientFactory):

	def buildProtocol(self,addr):

		connection = Server()
		
		# start lobby loop

		return connection

	def clientConnectionLost(self,connector, reason):
		print "Lost connection to server.. Reason: " + str(reason)
		ReconnectingClientFactory.clientConnectionLost(self,connector, reason)
	def clientConnectionFailed(self,connector,reason):
		print "Connection to server failed.. " + str(reason)
		ReconnectingClientFactory.clientConnectionLost(self,connector, reason)
		
def lobby():
	print "lobby"

if __name__ == "__main__":

	# connect to server
	reactor.connectTCP(SERVER_HOST, SERVER_PORT, ServerClientFactory())
	
	reactor.run()
