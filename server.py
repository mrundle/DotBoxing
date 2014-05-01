# DotBoxing Server Code
# Matt Mahan and Matt Rundle
# Programming Paradigms PyGameTwisted Project
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.defer import DeferredQueue

LISTEN_PORT = 40035

# key: username
# val: connection instance
# use: users[username].transport.write(...)
users = {}

class Client(Protocol):
	def __init__(self):
		self.clientName = ''

	def connectionMade(self):
		print "connected to client"
		self.transport.write("identify")

	def dataReceived(self,data):
		print "received data = " + data
		data = data.rstrip()
		# should come in the form of "id:username"
		dataArray = data.split(':')
		if dataArray[0] == "id":
			# user is attempting to create a username
			username = dataArray[1]
			# check to see if it is already in use
			if username in users:
				# if so, send "reidentify"
				self.transport.write("reidentify")
			else:
				# if not, add to users and send "idConfirmed"
				users[username] = self
				self.transport.write("idConfirmed")
		
		# <DEBUG>
		print "current list of users: "
		for key in users:
			print key
		

	def connectionLost(self,reason):
		print "dropped a client connection"

class ClientFactory(Factory):
	def buildProtocol(self,addr):
		return Client()

if __name__ == "__main__":
	reactor.listenTCP(LISTEN_PORT, ClientFactory())
	reactor.run()
