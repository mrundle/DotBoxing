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
waiting = [] # add to this when users want to randomly get assigned - then call getGame
available = []

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
				# if not, add to users and available and send "idConfirmed"
				self.username = name
				users[self.username] = self
				available.append(self.username)
				# Notify everyone what happened
				for user in users:
					if user == self.username:
						self.transport.write("idConfirmed")
					else:
						self.sendOnlineList(user)
						self.sendAvailableList(user)

		elif dataArray[0] == "challenge":
			print data
			toChallenge = dataArray[1].rstrip()
			if toChallenge in available:
				# challenge the other user
				print self.username + " is about to challenge " + toChallenge
				users[toChallenge].transport.write("challenge:" + self.username)
			else:
				self.transport.write("msg:" + "CHALLENGE FAILED. User \"" + toChallenge + "\" is either not available or doesn't exist.")

		elif dataArray[0] == "getGame":
			# LOOP UNTIL OPPENENTS ARE ASSIGNED
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

		elif dataArray[0] == "viewAvailable":
			self.sendAvailableList(self.username)

		elif dataArray[0] == "viewOnline":
			self.sendOnlineList(self.username)

	def sendAvailableList(self,destination):
		availableUsers = ''
		added = 0
		for user in available:
			if user != destination:
				availableUsers = availableUsers + user + ", "
				added += 1
		users[destination].transport.write("available:" + availableUsers)

	def sendOnlineList(self,destination):
		onlineUsers = ''
		added = 0
		for user in users:
			if user != destination:
				onlineUsers = onlineUsers + user + ", "
				added += 1
		users[destination].transport.write("online:" + onlineUsers)
			
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
		# delete from available if there
		if self.username in available:
			available.remove(self.username)
		# TODO: Notify others that connection has been lost
		# necessary for ending games.

class ClientFactory(Factory):
	def buildProtocol(self,addr):
		return Client()

if __name__ == "__main__":
	reactor.listenTCP(LISTEN_PORT, ClientFactory())
	reactor.run()
