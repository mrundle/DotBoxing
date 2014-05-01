# DotBoxing Client Code
# Matt Mahan and Matt Rundle
# Programming Paradigms PyGameTwisted Project

# import pygame gamespace
from dotboxing import GameSpace

# import networking
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory

SERVER_HOST = 'localhost'   # (global) should be whatever host server.py is running on
SERVER_PORT = 40035         # (global) should match the server.py file

#objects  = {}               # (global) will contain the server connection


class Server(Protocol):	
	def __init__(self):
		# initialize vars
		self.username = ''

	def connectionMade(self):
		print "Connected to server."

		# create client, pass connection
		
		# import GameSpace instance
		print "Initializing game instance..."
		self.gs = GameSpace()
		print "Game instance initialized."

	def dataReceived(self, data):
		data = data.rstrip()
		if (data == 'identify'):
			# identify to server
			self.username = self.gs.identify("identify")
			msg = "id:" + self.username
			self.transport.write(msg)
		elif (data == 'reidentify'):
			# username already taken, try again
			self.username = self.gs.identify("reidentify")
			msg = "id:" + self.username
			self.transport.write(msg)
		elif (data == 'idConfirmed'):
			print "ID " + self.username + " confirmed!"


	def initialIdentify(self):
		c.gs.identify()
		print "un: " + client.username
	

class ServerClientFactory(ReconnectingClientFactory):

	def buildProtocol(self,addr):
		connection = Server()
		return connection
	def clientConnectionLost(self,connector, reason):
		print "Lost connection to server.. Reason: " + str(reason)
		ReconnectingClientFactory.clientConnectionLost(self,connector, reason)
	def clientConnectionFailed(self,connector,reason):
		print "Connection to server failed.. " + str(reason)
		ReconnectingClientFactory.clientConnectionLost(self,connector, reason)
		

if __name__ == "__main__":
	# connect to server
	reactor.connectTCP(SERVER_HOST, SERVER_PORT, ServerClientFactory())
	reactor.run()
