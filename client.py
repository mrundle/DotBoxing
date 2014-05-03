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

	def connectionMade(self):
		print "Connected to server."

		# create client, pass connection
		

	def dataReceived(self, data):
		data = data.rstrip()
		if (data == 'identify'):
			# identify to server
			#self.username = reactor.gs.identify("identify")
			reactor.gs.identify("identify")			
			# msg = "id:" + self.username
			# self.transport.write(msg)
		elif (data == 'reidentify'):
			# username already taken, try again
			self.username = reactor.gs.identify("reidentify")
			msg = "id:" + self.username
			self.transport.write(msg)
		elif (data == 'idConfirmed'):
			print "ID " + self.username + " confirmed!"

	def checkGame(self):
		pass
	

class ServerClientFactory(ReconnectingClientFactory):

	def buildProtocol(self,addr):

		connection = Server()
		
		# start game loop
		lc = LoopingCall(reactor.gs.loop)
		lc.start(1/60)

		reactor.gs.protocol = connection
		return connection

	def clientConnectionLost(self,connector, reason):
		print "Lost connection to server.. Reason: " + str(reason)
		ReconnectingClientFactory.clientConnectionLost(self,connector, reason)
	def clientConnectionFailed(self,connector,reason):
		print "Connection to server failed.. " + str(reason)
		ReconnectingClientFactory.clientConnectionLost(self,connector, reason)
		

if __name__ == "__main__":

	# import GameSpace instance
	print "Initializing game instance..."
	reactor.gs = GameSpace(reactor)
	print "Game instance initialized."

	# connect to server
	reactor.connectTCP(SERVER_HOST, SERVER_PORT, ServerClientFactory())
	
	reactor.run()
