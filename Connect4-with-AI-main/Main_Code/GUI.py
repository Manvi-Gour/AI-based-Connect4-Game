#CLI version of Connect-4 Game

import numpy as np
import pygame

#Pygame initialisation
pygame.init()

#COLORS
BLACK = (0,0,0)
LIGHT_BLUE = (0,100,235)
GREY = (220,220,220)
RED = (235,0,0)
YELLOW = (255,255,0)

#GLOBAL VARS
MAX_COLS = 7#maximum rows
MAX_ROWS = 6#maximum columns
ongoing = True #Tells if the game is ongoing
moves = 0 #number of moves till now

#FONTS
WINNER_FONT = pygame.font.SysFont('arial', 75)
FINISH_FONT = pygame.font.SysFont('Verdana', 100)

#creating a board for the new game
def create_board():
	board = np.zeros((6,7))
	return board


#check if choice is valid
def valid_choice(board, col):
	return board[0][col] == 0

#put the piece on the board
def drop_piece(board, col, row, who_moved):
	board[row][col] = who_moved

#get the first free row
def get_row(board, col):
	for r in reversed(range(MAX_ROWS)):
		if board[r][col] == 0:
			return r

#check if the last move was winning
def winning_check(board, last):
	#Horizontal checks
	for r in range(MAX_ROWS):
		for c in range(MAX_COLS-3):
			if board[r][c] == last and board[r][c+1] == last and board[r][c+2] == last and board[r][c+3] == last:
				return True

	#vertical checks
	for r in range(MAX_ROWS-3):
		for c in range(MAX_COLS):
			if board[r][c] == last and board[r+1][c] == last and board[r+2][c] == last and board[r+3][c] == last:
				return True
				
	#right diagonal checks (\)
	for r in range(MAX_ROWS-3):
		for c in range(MAX_COLS-3):
			if board[r][c] == last and board[r+1][c+1] == last and board[r+2][c+2] == last and board[r+3][c+3] == last:
				return True

	#left diagonal checks (/)
	for r in range(3, MAX_ROWS):
		for c in range(MAX_COLS-3):
			if board[r][c] == last and board[r-1][c+1] == last and board[r-2][c+2] == last and board[r-3][c+3] == last:
				return True

#Pygame functions
#Initial Drawing	
def draw_board(board):
	for r in range(MAX_ROWS):
		for c in range(MAX_COLS):
			pygame.draw.rect(screen, BLACK, (c*100,r*100 + 100, 100, 100)) # rect => (x,y,w,h)
			# pygame.draw.rect(surface, color, rect)

	for r in range(MAX_ROWS):
		for c in range(MAX_COLS):
			pygame.draw.circle(screen, GREY, (c*100 + 50, r*100 + 150), 40)

	pygame.display.update()

#put a token in the board
def change_board(board, c, r, token):
	if (token == 1):
		pygame.draw.circle(screen, RED, (c*100 + 50, r*100 + 150), 40)
	else:
		pygame.draw.circle(screen, YELLOW, (c*100 + 50, r*100 + 150), 40)

	pygame.display.update()



#MAIN_FUNCTION


#Creating the board
board = create_board()


#Define size
width = (MAX_COLS)*100
height = (MAX_ROWS+1)*100
size = (width, height)

#Set up the drawing window for pygame
screen = pygame.display.set_mode(size)
screen.fill(LIGHT_BLUE)
pygame.display.update()

#draw the board before the game starts
draw_board(board)


#Let the games begin!!
while ongoing:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			ongoing = False
			exit()

		if event.type == pygame.MOUSEMOTION:
			x_pos = event.pos[0] 
			pygame.draw.rect(screen, LIGHT_BLUE, (0,0,width,100))

			if not (moves&1):
				pygame.draw.circle(screen, RED, (x_pos, 50), 40)
			else:
				pygame.draw.circle(screen, YELLOW, (x_pos, 50), 40)

			pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:

			print(board)
			
			#If number of moves is even Player 1 is going to move
			if not (moves&1):
				x_val = event.pos[0]
				choice = int(x_val/100) 
				# print(choice)
				# choice = int(input("Player 1 enter which column you want to select from 0 to 6: "))

				#If choice is valid
				if valid_choice(board, choice):
					row = get_row(board, choice)
					drop_piece(board, choice, row, 1)
					change_board(board, choice, row, 1)
					moves += 1
					if winning_check(board, 1):
						print(board)
						print("Player %d won after %d moves!!" %(1, moves))
						ongoing = False

				#If choice isn't valid		
				else:
					print("Enter valid choice!!")
					continue

			#If number of moves is odd Player 2 is going to move
			else:
				x_val = event.pos[0]
				choice = int(x_val/100)
				print(choice)
				# choice = int(input("Player 2 enter which column you want to select from 0 to 6: "))

				#If choice is valid
				if valid_choice(board, choice):
					row = get_row(board, choice)
					drop_piece(board, choice, row, 2)
					change_board(board, choice, row, 2)
					moves += 1
					if winning_check(board, 2):
						print(board)
						print("Player %d won after %d moves!!" %(2, moves))
						ongoing = False

				#If the choice isn't valid
				else:
					print("Enter valid choice!!")
					continue

if (moves&1):
	winner = WINNER_FONT.render("Player 1 Won !!!", True, RED)

else:
	winner = WINNER_FONT.render("Player 2 Won !!!", True, YELLOW)


game_over = FINISH_FONT.render("GAME OVER!", True, (0,255,0))

screen.blit(winner, (70,140))
screen.blit(game_over, (60,240))
pygame.display.update()
pygame.time.wait(5000)

