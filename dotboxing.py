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

		# Set up the screen
		self.size   =  self.width, self.height = 640, 480
		self.black  =  0, 0, 0
		self.screen =  pygame.display.set_mode(self.size)

		# set up button click values
		self.upButton    = False
		self.downButton  = False
		self.leftButton  = False
		self.rightButton = False
		self.mouseClick  = False

		# set up game objects
		
		print "GameSpace initialized"

	def loop(self):

		# Code for one loop of the game logic
		# Note: loop will be called by client.py, not in this file
		
		# handle user input

		# send ticks to game objects

		# blit game objects

		pass

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
			
		
		







