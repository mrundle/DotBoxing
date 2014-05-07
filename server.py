# DotBoxing Server Code
# Matt Mahan and Matt Rundle
# Programming Paradigms PyGameTwisted Project

from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.defer import DeferredQueue

# Port that the server will run on
# Note: Clients (client.py) must connect to THIS port number.
LISTEN_PORT = 40035

# Other global data structures
users = {}      # Current Users 
                # key: username
                # val: connection instance
                # use: users[username].transport.write(...)
waiting = [] 	# users waiting for random assignment
available = []  # users available for gameplay

class Client(Protocol):

	def __init__(self):
		self.username = ''
		# initialize queue
		self.queue = DeferredQueue()
		# Start queueing incoming data
		self.startQueuing()

	# Called from Twisted upon new connection
	def connectionMade(self):
		pass

	# Called from Twisted upon incoming data
	# TODO: Queue this data
	def dataReceived(self,data):
		self.queue.put(data)

	# Continuously grabs data from the 
	def queueData(self,data):
		data = data.rstrip()
		self.handleData(data)
		self.queue.get().addCallback(self.queueData)

	# Kicks off the queueData loop
	def startQueuing(self):
		self.queue.get().addCallback(self.queueData)

	# Handle data sent by clients
	def handleData(self,data):

		# Get rid of pesky trailing whitespace
		data = data.rstrip()

		# All messages should come in the colon dilineated form:
		#    element:element:element ... and so on
		dataArray = data.split(':')
		cmmd = dataArray[0]

		if cmmd == "id":
			# Client is attempting to create a username
			#    id:<proposedName>
			name = dataArray[1]
			# check to see if it is already in use, or is blank, or contains '+' or ':'
			if name in users or name == '' or ':' in name or '+' in name or len(dataArray) > 2:
				self.transport.write("reidentify")
			else:
				# Name is valid!
				self.username = name             # store
				users[self.username] = self      # add ref to userList
				available.append(self.username)  # append name to available
				# Notify everyone what happened
				self.globalUserListUpdate()

		elif cmmd == "challenge":
			# Client is challenging another user
			#     challenge:<username>
			toChallenge = dataArray[1]
			if toChallenge in available:
				users[toChallenge].transport.write("challenge:" + self.username)
			else:
				self.transport.write("msg:" + "CHALLENGE FAILED. User \"" + toChallenge + "\" is either not available or doesn't exist.")

		elif cmmd == "confirmChallenge":
			# Client is accepting a challenge from another user
			#     confirmChallenge:<selfUsername>:<opponentUsername>
			user1 = dataArray[1]
			user2 = dataArray[2]
			# Remove from available
			if user1 in available: available.remove(user1)
			if user2 in available: available.remove(user2)
			# Notify each user of the game:
			#    opponent:<username>:<turnOrder>
			if user1 in users:
				users[user1].transport.write("opponent:" + user2 + ":1")
			else:
				available.add(user2)
			if user2 in users:
				users[user2].transport.write("opponent:" + user1 + ":2")
			else:
				available.add(user1)

		elif cmmd == "rejectChallenge":
			# Client is rejecting a challenge from another user:
			#    rejectChallenge:<username>
			rejectedChallenger = dataArray[1]
			# Notify the rejected challenger
			if rejectedChallenger in users:
				users[rejectedChallenger].transport.write("reject")

		# TODO: currently un-utilized. Useful for random placement.
		# Note: This is what uses the 'waiting' list
		elif cmmd == "getGame":
			# Add user to the waiting list
			waiting.append(self.username)
			# If anyone else in list, start game
			for user in waiting:
				if user != self.username:
					# Notify both users of gamee:
					#    opponent:<opponentName>:<turnOrder>
					if user in users: 
						self.transport.write("opponent:" + user + ":1")
						users[user].transport.write("opponent:" + self.username + ":2")
						# Remove users from waiting list
						if user in waiting:
							waiting.remove(user)
						if self.username in waiting:
							waiting.remove(self.username)
						# Also remove from available list
						if user in available:
							available.remove(user)
						if self.username in available:
							available.remove(self.username)
			# If no one else in list, they will wait for someone else to pick them up

		elif cmmd == "move":
			# Client is sending a move to another user
			#    move:<opponent>:<moveID>
			opponent = dataArray[1].rstrip()
			moveID = dataArray[2].rstrip()
			# Notify the opponent of the move
			if opponent in users:
				users[opponent].transport.write("opponentMove:"+moveID)
			else:
				# If the other user isn't there, they have forfeited
				self.transport.write("forfeit:null")

		elif cmmd == "forfeit":
			# Client has forfeited the game (or prematurely exited/quit)
			opponent = dataArray[1]
			# Add both users to Available list
			available.append(opponent)
			available.append(self.username)
			# Notify the opponent of the forfeit
			# The opponent will then call refresh and trigger a globalUserListUpdate
			if opponent in users:
				users[opponent].transport.write("forfeit:" + opponent)

		elif cmmd == "lost":
			# Client is notifying us that they have lost to their opponent:
			#    lost:<opponent>
			opponent = dataArray[1]
			# Notify the opponent of their win
			if opponent in users:
				users[opponent].transport.write("winner:null")
	
		elif cmmd == "won":
			# Client is notifying us that they have beat their opponent:
			#    won:<opponent>
			opponent = dataArray[1]
			# Notify the opponent of their loss
			if opponent in users:
				users[opponent].transport.write("loser:null")

		elif cmmd == "tied":
			# Client is notifying us that they have tied their opponent:
			#    tied:<opponent>
			opponent = dataArray[1]
			# Notify the opponent of tie game
			if opponent in users:
				users[opponent].transport.write("tied:null")

		elif cmmd == "available":
			# Client is notifying server that they (and an opponent) are available
			#     available:<user1>:<user2>
			available.append(dataArray[1])
			available.append(dataArray[2])
			# Everyone needs to know about this!
			self.globalUserListUpdate()

		elif cmmd == "chat":
			message = "chat:" + self.username + " >> " + dataArray[1]
			# send this message to all other users
			for user in users:
				users[user].transport.write(message)

		elif cmmd == "refresh":
			self.globalUserListUpdate()

	# Sends out list of Online and Available users to all connected users:
	#    users:bob+tom+amy+kim+:available:bot+amy+
	# Client file is responsible for stripping trailing '+' marks.
	def globalUserListUpdate(self):
		onlineUsers = ''
		availableUsers = ''
		for user in users:
			onlineUsers = onlineUsers + user + "+"
		for user in available:
			availableUsers = availableUsers + user + "+"
		for user in users:
			users[user].transport.write("users:" + onlineUsers + ":available:" + availableUsers)
		

	def connectionLost(self,reason):
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
		# Notify others that connection has been lost
		self.globalUserListUpdate()

# Simply builds the Client protocol
class ClientFactory(Factory):
	def buildProtocol(self,addr):
		return Client()

if __name__ == "__main__":
	reactor.listenTCP(LISTEN_PORT, ClientFactory())
	reactor.run()
