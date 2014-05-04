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
waiting = []

class Client(Protocol):
	def __init__(self):
		self.username = ''

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
			name = dataArray[1]
			# check to see if it is already in use
			if name in users or name == '':
				# if so, send "reidentify"
				self.transport.write("reidentify")
			else:
				# if not, add to users and waiting and send "idConfirmed"
				self.username = name
				users[self.username] = self
				waiting.append(self.username)
				#self.transport.write("idConfirmed")
				# NOW - LOOP UNTIL OPPENENTS ARE ASSIGNED
				assigned = False
				self.printUsers()
				self.printWaiting()
				for user in waiting:
					if user != self.username:
						print "ASSIGNED " + self.username + " TO " + user
						turn = 0
						# the user waiting the longest will have first turn
						turn = turn + 1
						self.transport.write("opponent:" + user + ":" + str(turn))
						# the user just joining will have the second turn
						turn = turn + 1
						users[user].transport.write("opponent:" + self.username + ":" + str(turn))
						waiting.remove(user)
						waiting.remove(self.username)
		elif dataArray[0] == "move":
			destination = dataArray[1].rstrip()
			moveID      = dataArray[2].rstrip()
			users[destination].transport.write("opponentMove:"+moveID)
			# TODO catch key error exception
			
		
	def printUsers(self):
		print "current list of users: "
		for key in users:
			print key

	def printWaiting(self):
		print "current list of waiting users: "
		for user in waiting:
			print user
		

	def connectionLost(self,reason):
		print "dropped client connection (" + self.username + ")"
		# delete from users list
		try:
			del users[self.username]
		except KeyError:
			pass
		# delete from waiting queue if there
		if self.username in waiting:
			waiting.remove(self.username)
		# TODO: Notify others that connection has been lost
		# necessary for ending games.

class ClientFactory(Factory):
	def buildProtocol(self,addr):
		return Client()

if __name__ == "__main__":
	reactor.listenTCP(LISTEN_PORT, ClientFactory())
	reactor.run()
