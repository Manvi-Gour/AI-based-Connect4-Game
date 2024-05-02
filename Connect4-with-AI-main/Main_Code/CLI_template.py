#CLI version of Connect-4 Game

# import numpy as np

MAX_COLS = 7#maximum rows
MAX_ROWS = 6#maximum columns
ongoing = True #Tells if the game is ongoing
moves = 0 #number of moves till now

#creating a board for the new game   
def create_board():
	pass

#check if column is valid
def valid_choice(board, col):
	pass

#put the piece on the board
def drop_piece(board, col, row, who_moved):
	pass

#get the first free row
def get_row(board, col):
	pass

#check if the last move was winning   
def winning_check(board, last):		
	#Horizontal checks
	pass

	#vertical checks
	pass
				
	#right diagonal checks (\)
	pass

	#left diagonal checks (/)
	pass
	
#Creating the board
board = create_board()

#Let the games begin!!				
while ongoing:							 
	print(board)
	
	#If number of moves is even Player 1 is going to move
		#If choice is valid
		#If choice isn't valid

	#If number of moves is odd Player 2 is going to move
		#If choice is valid
		#If choice isn't valid
