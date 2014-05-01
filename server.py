# DotBoxing Server Code
# Matt Mahan and Matt Rundle
# Programming Paradigms PyGameTwisted Project
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.defer import DeferredQueue

LISTEN_PORT = 40035
users = {}

class Client(Protocol):
	def __init__(self):
		self.clientName = ''
	def connectionMade(self):
		print "connected to client"
		self.transport.write("identify")
	def dataReceived(self,data):
		pass
	def connectionLost(self,reason):
		print "dropped a client connection"

class ClientFactory(Factory):
	def buildProtocol(self,addr):
		return Client()

if __name__ == "__main__":
	reactor.listenTCP(LISTEN_PORT, ClientFactory())
	reactor.run()
