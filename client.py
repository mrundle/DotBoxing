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
SERVER_PORT = 40035         # (global) should match the server.py file


class Server(Protocol):	
	def __init__(self):
		# initialize vars
		self.username = ''
		self.opponent = ''

	def connectionMade(self):
		print "Connected to server."
		

	def dataReceived(self, msg):
		msg = msg.rstrip()
		data = msg.split(':')
		if (data[0] == 'oponent'):
			self.opponent = data[1]
			print "my opponent is " + self.opponent
		if (data[0] == 'identify'):
			# identify to server
			#self.username = reactor.gs.identify("identify")
			reactor.gs.identify("identify")			
			# msg = "id:" + self.username
			# self.transport.write(msg)
		elif (data[0] == 'reidentify'):
			# username already taken, try again
			self.username = reactor.gs.identify("reidentify")
			msg = "id:" + self.username
			self.transport.write(msg)
		elif (data[0] == 'idConfirmed'):
			print "ID " + self.username + " confirmed!"
		elif (data[0] == 'opponentMove'):
			moveID = data[1]
			reactor.gs.opponentMove(moveID) 

	def sendMove(self,moveID):
		# send move to the opponent
	

class ServerClientFactory(ReconnectingClientFactory):

	def buildProtocol(self,addr):

		connection = Server()
		# import GameSpace instance
		print "Initializing game instance..."
		reactor.gs = GameSpace(reactor)
		print "Game instance initialized."
		# start game loop
		lc = LoopingCall(reactor.gs.loop)
		lc.start(1/60)
		# start lobby loop

		reactor.gs.protocol = connection
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
