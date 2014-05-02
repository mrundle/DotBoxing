# DotBoxing Game Code
# Matt Mahan and Matt Rundle
# Programming Paradigms PyGameTwisted Project
import pygame
import math

class GameSpace:

	def __init__(self):
		# Initialize pygame
		pygame.init()
		pygame.mixer.init()

		# colors
		self.black  =  0, 0, 0
		self.white = 255, 255, 255
		self.grey = 224, 224, 224

		# Set up the screen
		self.size   =  self.width, self.height = 640, 480
		self.screen =  pygame.display.set_mode(self.size)
		self.screen.fill(self.black)

		# set up button click values
		self.upButton    = False
		self.downButton  = False
		self.leftButton  = False
		self.rightButton = False
		self.mouseClick  = False

		# set up game objects
		self.board = GameBoard(self)
		
		print "GameSpace initialized"

	def loop(self):

		# Code for one loop of the game logic
		# Note: loop will be called by client.py, not in this file
		
		# handle user input

		# send ticks to game objects

		# blit game objects
		self.screen.blit(self.board,(0,0))

		# Flip the display
		pygame.display.flip()

	def identify(self, msg):
		# identify to server (pick username)
		# NOTE: This is stored in client.py,
		#       as it shouldn't be needed for game logic.
		#       The prompt needs to go here because the 
		#       it needs to be handled graphically via pygame.
		# TODO: Handle via pygame instead of command line
		msg = msg.rstrip()
		if msg == "identify":
			# initial prompt
			return raw_input("Enter a username: ")
		elif msg == "reidentify":
			# username already taken
			return raw_input("Name already taken. Enter a username: ")
			

# The screen when the game is being played (as opposed to the lobby)
class GameBoard(pygame.Surface):

	def __init__(self,gs):
	
		# initial setup
		self.gs = gs
		pygame.Surface.__init__(self,(self.gs.width,self.gs.height))
		self.fill(self.gs.white)
		
		self.dot_x = 10 # number of dots on one side of the square
		self.margin = 30
		self.x = self.margin
		self.y = self.margin
		self.width = self.gs.width-self.margin
		self.height = self.gs.height-self.margin
		self.interval = (self.width-self.x)/self.dot_x
		self.dot_radius = 3
		
		# make the dots
		for i in range(self.x, self.width, self.interval):
			for j in range(self.y, self.height, self.interval):
				
				# Make a dot
				pygame.draw.circle(self, self.gs.black,(i,j),self.dot_radius)
				
		# make the separators
		
		
# A "Separator" surface - the things that connect the dots.
# The actual surface is a rectangle, with the polygon drawn on it
class Separator(pygame.Surface):

	def __init__(self,gs,width,height):
	
		# initial setup
		pygame.Surface.__init__(self,width,height)
		self.height = height
		self.width = width
		self.gs = gs
		self.fill(self.gs.white)
		self.spacing = 5
		self.x = 5
		self.y = 0
		
		# draw polygon
		self.head = (self.x, self.y)
		self.tail = (self.x, self.y+self.height)
		self.r_shoulder = (self.x+self.spacing, self.y+self.spacing)
		self.l_shoulder = (self.x-self.spacing, self.y+self.spacing)
		self.r_leg = (self.x+self.spacing, self.y-self.spacing)
		self.l_leg = (self.x-self.spacing, self.y-self.spacing)
		pointlist = (self.head,self.tail,self.r_shoulder,self.l_shoulder,self.r_leg,self.l_leg)
		#pygame.draw.polygon(self,self.gs,game




