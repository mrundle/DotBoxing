# DotBoxing Game Code
# Matt Mahan and Matt Rundle
# Programming Paradigms PyGameTwisted Project
import pygame
import math
import sys
import os
import time
import getopt
from socket import *
from pygame.locals import *

class GameSpace:

	def __init__(self,reactor):

		# Initialize pygame
		pygame.init()
		pygame.mixer.init()

		# set up gamespace variable
		self.turn = "Mine"
		self.quit_condition = "forfeit"
		self.GameOver = False

		# Initialize networking vars
		self.reactor  = reactor
		self.protocol = None
		
		# colors
		self.black  =   0, 0, 0
		self.white  = 255, 255, 255
		self.grey   = 200, 200, 200
		self.blue   =   0,   0,204
		self.red = 255,0,0
		
		
		# visual parameters - set here for ease of adjusting game layout
		self.dot_number = 3 # number of dots on one side of the square
		self.player_color = self.blue # color of player seperators and won squares
		self.opponent_color = self.red # color of opponent seperators and won squares
		self.margin = 80 # margin between dots and edge of screen
		

		# Set up the screen
		self.size   =  self.width, self.height = 640, 640
		self.screen =  pygame.display.set_mode(self.size)
		self.screen.fill(self.black)
		pygame.display.set_caption("DotBoxing")

		# set up button click values
		self.upButton    = False
		self.downButton  = False
		self.leftButton  = False
		self.rightButton = False
		self.mouseClick  = False

		# set up game objects
		self.board = GameBoard(self)
		self.MyScore = Score(self)
		self.MyScore.text = "My score: "
		self.MyScore.update()
		self.OpponentScore = Score(self)
		self.OpponentScore.text = "Opponent's Score: "
		self.OpponentScore.update()
		
		print "GameSpace initialized"

	def loop(self):

		# Code for one loop of the game logic
		# Note: loop will be called by client.py, not in this file
		
		# do nothing if game is over
		if self.GameOver == True:
			return
		
		# handle user input
		for event in pygame.event.get():
			if event.type == QUIT:
				# Close pygame
				self._Quit()
				return "GameOver"
				#self.reactor.stop()
			elif event.type == MOUSEBUTTONUP:
				#print "Mouse clicked!" 
				self.On_Click()

		# update game objects
		self.CompleteSquares()

		# do nothing if game is over
		if self.GameOver == True:
			return

		# blit game objects
		self.screen.blit(self.board,(0,0))
		for Separator in self.board.separators:
			self.screen.blit(Separator.image,Separator.rect)
		self.screen.blit(self.MyScore.image,(5,5))
		self.screen.blit(self.OpponentScore.image,(5,20))
		
		# Flip the display
		pygame.display.flip()
		
		
	# calls game objects On_Click functions
	def On_Click(self):
		for Separator in self.board.separators:
			Separator.On_Click()
			
	# actions to take when move data received
	def opponentMove(self,_id):
		
		# ignore if game is over
		if self.GameOver == True:
			return
		
		# skip if its my turn
		if self.turn == "Mine":
			return
			
		# error check for improper turn handling
		if self.turn != "Other":
			print "Error: Improper turn handling"
			self._Quit()
			
		# Find Separator
		Separator = self.board.FindSeparator(_id)
			
		# if no separator found, ignore
		if Separator == None:
			return
			
		# change separator color
		Separator.color = self.opponent_color
		pygame.draw.polygon(Separator.image,Separator.color,Separator.pointlist)
			
		# switch turn
		self.turn = "Mine"
		Separator.clicked = True
		self.lastclick = "Opponent"
		
		# check for win
		self.CheckForWin()
		
		
		
	# check for completed squares, mark accordingly
	def CompleteSquares(self):
	
		# print "Complete Square function called"
		
		for Separator in self.board.separators:
			Separator.CompleteSquare()

	
	# close the gamespace
	def _Quit(self):
	
		# ignore if has already quit
		if self.GameOver == True:
			return
			
		self.GameOver = True
		
		# temporarily default to forfeit
		if self.protocol == None:
			print "Error: no protocol supplied to gamestate."
			pygame.quit()
		else:
			self.protocol.gameEnded(self.quit_condition)
			pygame.quit()	
			
			
	# close the gamespace without a protocol message
	def quietQuit(self):
	
		# ignore if has already quit
		if self.GameOver == True:
			return

		self.GameOver = True
		pygame.quit()
		
		
	# check for the end of the game
	def CheckForWin(self):
	
		# check to see if all Separators have been clicked
		for Separator in self.board.separators:
			if Separator.clicked == False:
				return
		
		print "WIN_COND_TRIGGERED"
		# if so, determine winner
		if self.MyScore.score > self.OpponentScore.score:
			# I win!
			self.quit_condition = "won"
			self._Quit()
		elif self.MyScore.score < self.OpponentScore.score:
			# I lose!
			self.quit_condition = "lost"
			self._Quit()
		else:
			# I tied!
			self.quit_condition = "tied"
			self._Quit()
		

# The screen when the game is being played (as opposed to the lobby)
class GameBoard(pygame.Surface):

	def __init__(self,gs):
	
		# initial setup
		self.gs = gs
		pygame.Surface.__init__(self,(self.gs.width,self.gs.height))
		self.fill(self.gs.white)
		self.separators = pygame.sprite.Group()
		
		self.dot_x = self.gs.dot_number # number of dots on one side of the square
		self.margin = self.gs.margin
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
		for j in range(self.y, self.height, self.interval):
			for i in range(self.x, self.width, self.interval):
			
			
				if j < (self.height-self.interval):
					temp = Separator(self.gs,10,self.interval-2*self.dot_radius,"vert")
					temp.rect.x = i - temp.spacing   # account for spacing
					temp.rect.y = j + self.dot_radius   # account for dot radius
					temp.id = str(temp.rect.x) + "," + str(temp.rect.y)
					self.separators.add(temp)
					
				if i < (self.width-self.interval):
					temp = Separator(self.gs,self.interval-2*self.dot_radius,10,"horz")
					temp.rect.x = i + self.dot_radius   # account for dot radius
					temp.rect.y = j - temp.spacing   # account for spacing
					temp.id = str(temp.rect.x) + "," + str(temp.rect.y)
					
					# add neighbors (for checking win condition)
					# left neighbor is left and up, right neighbor is right and up, far neighbor is across the above square
					temp.left_neighbor = self.FindSeparator(str(i - temp.spacing) + "," + str(j - self.interval + self.dot_radius))
					temp.right_neighbor = self.FindSeparator(str(i - temp.spacing + self.interval) + "," + str(j - self.interval + self.dot_radius))
					temp.far_neighbor = self.FindSeparator(str(temp.rect.x) + "," + str(temp.rect.y - self.interval))
					
					#if temp.left_neighbor != None:
						#print "Left neighbor is not None!"
					#if temp.right_neighbor != None:
						#print "Right neighbor is not None!"
					#if temp.far_neighbor != None:
						#print "Far neighbor is not None!"
					
					self.separators.add(temp)
	
	
	# helper function that locates separators based on id				
	def FindSeparator(self,_id):
	
		for Separator in self.separators:
			if Separator.id == _id:
				return Separator
		
		# If none found, return None
		return None
					
				
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
		self.clicked = False
		self.complete = False
		
		# initialize neighbors
		self.left_neighbor = None
		self.right_neighbor = None
		self.far_neighbor = None
		
		
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
			self.gs._Quit()
			
		# skip if clicked already
		if self.clicked == True:
			return
			
		# get mouse position
		mx, my = pygame.mouse.get_pos()
		
		# test if position is inside object rect
		if self.rect.collidepoint(mx,my) == True:
		
			# change separator color
			self.color = self.gs.player_color
			pygame.draw.polygon(self.image,self.color,self.pointlist)
			
			# switch turn and indicate clicked
			self.clicked = True
			self.gs.lastclick = "Me"
			self.gs.turn = "Other"
			self.gs.protocol.sendMove(self.id)
			
		
	# check to see if square is completed, takes action if so
	def CompleteSquare(self):
	
		# print "CompleteSquare function called"	
		
		if self.complete == True:
			return

		if self.left_neighbor == None:
			return
		if self.right_neighbor == None:
			return
		if self.far_neighbor == None:
			return
		
		# print "Checking for complete square:"
		
		# check for squares
		if self.left_neighbor.clicked==self.right_neighbor.clicked==self.far_neighbor.clicked==self.clicked==True:
			
			# if square is complete, fill in the square with the appropriate color
			if self.gs.lastclick == "Opponent":
				fill_color = self.gs.opponent_color
				self.gs.OpponentScore.score += 1
				self.gs.OpponentScore.update()
				self.gs.turn = "Other" # Opponent gets another turn
			elif self.gs.lastclick == "Me":
				fill_color = self.gs.player_color
				self.gs.MyScore.score += 1
				self.gs.MyScore.update()
				self.gs.turn = "Mine" # I get another turn
			else:
				print "Error: Improper last click mechanism"
				self.gs.quietQuit()
				
			square_width = self.gs.board.interval - self.gs.board.dot_radius*2
			square = pygame.Rect(self.rect.x+3, self.rect.y-square_width+5,square_width-6,square_width-6)
			pygame.draw.rect(self.gs.board,fill_color,square)
			self.complete = True
	
		
class Score(pygame.font.Font):

	def __init__(self,gs):
		
		# initial setup
		pygame.font.Font.__init__(self,None,22)
		self.gs = gs
		
		# initialize score and surface
		self.score = 0
		self.text = " "
		self.full_text = self.text + str(self.score)
		self.image = self.render(self.full_text,1,self.gs.black)
	
	# change the score
	def update(self):
		
		# ignore if game is over
		if self.gs.GameOver == True:
			return
		
		self.full_text = self.text + str(self.score)
		self.image = self.render(self.full_text,1,self.gs.black)
	
	


