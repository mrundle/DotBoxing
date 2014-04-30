# DotBoxing Client Code
# Matt Mahan and Matt Rundle
# Programming Paradigms PyGameTwisted Project

# import pygame gamespace
from dotboxing import GameSpace

# import networking
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory

SERVER_HOST = "localhost"	# (global) should be whatever host server.py is running on
SERVER_PORT = 40035			# (global) should match the server.py file

client      = None          # (global) will contain the client instance
connection  = None			# (global) will contain the server connection


class client:

	def __init__(self):
		print "Client initialized"

		# import GameSpace instance
		self.gs = GameSpace()

		# connect to server
		reactor.connectTCP(SERVER_HOST, SERVER_PORT, ServerClientFactory())
		reactor.run()

class Server(Protocol):

	def connectionMade(self):
		print "Connected to server"

	def dataReceived(self, data):
		pass
	

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
	client = client()
