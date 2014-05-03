# DotBoxing Game Code
# Matt Mahan and Matt Rundle
# Programming Paradigms PyGameTwisted Project
import pygame
import math
import sys
import os
import getopt
from socket import *
from pygame.locals import *

class GameSpace:

	def __init__(self,reactor):
		# Initialize pygame
		pygame.init()
		pygame.mixer.init()
		self.reactor=reactor

		# colors
		self.black  =  0, 0, 0
		self.white = 255, 255, 255
		self.grey = 200, 200, 200
		self.blue = 0,0,204

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
		
		# set up gamespace variable
		self.turn = "Mine"
		
		print "GameSpace initialized"

	def loop(self):

		# Code for one loop of the game logic
		# Note: loop will be called by client.py, not in this file
		
		# handle user input
		for event in pygame.event.get():
			if event.type == QUIT:
				self.reactor.stop()
			elif event.type == MOUSEBUTTONUP:
				print "Mouse clicked!"
				self.On_Click()

		# send ticks to game objects

		# blit game objects
		self.screen.blit(self.board,(0,0))
		for Separator in self.board.separators:
			self.screen.blit(Separator.image,Separator.rect)
		
		# Flip the display
		pygame.display.flip()
		
		
	# calls game objects On_Click functions
	def On_Click(self):
		for Separator in self.board.separators:
			Separator.On_Click()


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
		self.separators = pygame.sprite.Group()
		
		self.dot_x = 10 # number of dots on one side of the square
		self.margin = 50
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
		for i in range(self.x, self.width, self.interval):
			for j in range(self.y, self.height, self.interval):
			
				if j < (self.height-self.interval):
					temp = Separator(self.gs,10,self.interval-2*self.dot_radius,"vert")
					temp.rect.x = i - temp.spacing   # account for spacing
					temp.rect.y = j + self.dot_radius   # account for dot radius
					self.separators.add(temp)
					
				if i < (self.width-self.interval):
					temp = Separator(self.gs,self.interval-2*self.dot_radius,10,"horz")
					temp.rect.x = i + self.dot_radius   # account for dot radius
					temp.rect.y = j - temp.spacing   # account for spacing
					self.separators.add(temp)
				
# A "Separator" surface - the things that connect the dots.
# The actual surface is a rectangle, with the polygon drawn on it
class Separator(pygame.sprite.Sprite):

	def __init__(self,gs,width,height,mode):
	
		# initial setup
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((width,height))
		self.rect = self.image.get_rect()
		self.height = height
		self.width = width
		self.gs = gs
		self.image.fill(self.gs.white)
		self.spacing = 5
		self.mode = mode
		self.color = self.gs.grey
		
		# draw polygon
		if mode == "vert":
			self.x = 5
			self.y = 0
			self.head = (self.x, self.y)
			self.tail = (self.x, self.y+self.height)
			self.r_shoulder = (self.x+self.spacing, self.y+self.spacing)
			self.l_shoulder = (self.x-self.spacing, self.y+self.spacing)
			self.r_leg = (self.x+self.spacing, self.y+self.height-self.spacing)
			self.l_leg = (self.x-self.spacing, self.y+self.height-self.spacing)
		if mode == "horz":
			self.x = 0
			self.y = 5
			self.head = (self.x, self.y)
			self.tail = (self.x+self.width, self.y)
			self.r_shoulder = (self.x+self.spacing, self.y+self.spacing)
			self.l_shoulder = (self.x+self.spacing, self.y-self.spacing)
			self.r_leg = (self.x+self.width-self.spacing, self.y+self.spacing)
			self.l_leg = (self.x+self.width-self.spacing, self.y-self.spacing)
		self.pointlist = (self.head,self.r_shoulder,self.r_leg,self.tail,self.l_leg,self.l_shoulder)
		pygame.draw.polygon(self.image,self.color,self.pointlist)
		

	# check if object is clicked, takes action if so
	def On_Click(self):
	
		# skip if not my turn
		if self.gs.turn == "Other":
			return
			
		# error check for improper turn handling
		if self.gs.turn != "Mine":
			print "Error: Improper turn handling"
			self.gs.reactor.stop()
			
		# get mouse position
		mx, my = pygame.mouse.get_pos()
		
		# test if position is inside object rect
		if self.rect.collidepoint(mx,my) == True:
		
			# change separator color
			self.color = self.gs.blue
			pygame.draw.polygon(self.image,self.color,self.pointlist)
			
			# switch turn
			self.gs.turn = "Other"


