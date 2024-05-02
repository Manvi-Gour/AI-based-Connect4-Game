#GUI version of Connect-4 Game

# import numpy as np
#from new import WINNER_FONT
import numpy
import math
import pygame


pygame.init()

from math import inf
import random

#colors
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)
yellow = (255,255,0)
green = (0, 255, 0)

MAX_COLS = 7#maximum rows
MAX_ROWS = 6#maximum columns
ongoing = True #Tells if the game is ongoing
moves = 0 #number of moves till now

#fonts
Initial_Font  = pygame.font.SysFont('Arial', 100)
Winning_Font  = pygame.font.SysFont('Arial', 75)
Final_Font  = pygame.font.SysFont('Arial', 140)

#creating a board for the new game   
def create_board():
	return[[0 for j in range (MAX_COLS)] for i in range (MAX_ROWS)]

#Defining size
width = MAX_COLS*100
height = (MAX_ROWS+1)*100
size = (width,height)


#setting up screen
screen = pygame.display.set_mode(size)
screen.fill(black)
pygame.display.update()

#Drawing the board
def draw_board():
    for r in range(MAX_ROWS):
        for c in range (MAX_COLS):
            pygame.draw.rect(screen, blue, (c*100,r*100 + 100, 100, 100))
            pygame.draw.circle(screen,black,(c*100+50, r*100 + 150),40)
    pygame.display.update()

#check if column is valid
def valid_choice(board, col):
    if(0<=col<MAX_COLS) and board[0][col] == 0:
        return True
    return False

#put the piece on the board
def drop_piece(board, col, row, who_moved):
	board[row][col] = who_moved

#putting a token in the board
def put_token(c,r,p):
    if p == 1:
        pygame.draw.circle(screen,red,(c*100+50, r*100 + 150),40)
        #pygame.draw.circle(screen,yellow,(c*100+50, 50),40)
    else:
        pygame.draw.circle(screen,yellow,(c*100+50, r*100 + 150),40)
        #pygame.draw.circle(screen,red,(c*100+50, 50),40)
    pygame.display.update()

#get the first free row
def get_row(board, col):
	for i in range (MAX_ROWS-1,-1,-1):
         if board[i][col] == 0:
            return i 

#check if the last move was winning   
def winning_check(board,player):
    x = -1
    a = player
    #checking rows
    for i in range (MAX_ROWS):
        for j in range (MAX_COLS-3):
            for l in range (j,j+4):
                if board[i][l] != a:
                    x = -1
                    break
                else:
                    x = a
            if(x>-1):
                return x
    #checking columns
    for i in range (MAX_ROWS-3):
        for j in range (MAX_COLS):
            for l in range (i,i+4):
                if board[l][j] != a:
                    x = -1
                    break
                else:
                    x = a
            if(x>-1):
                return x
    #checking positive diagonals
    for i in range (MAX_ROWS-1,2,-1): 
        for j in range (MAX_COLS-3):
            for l in range(0,4):
                if board[i-l][j+l] != a:
                    x = -1
                    break
                else:
                    x = a
            if(x>-1):
                return x   
    #checking negative diagonals
    for i in range (MAX_ROWS-1,2,-1):
        for j in range (MAX_COLS-1,2,-1):
            for l in range(0,4):
                if board[i-l][j-l] != a:
                    x = -1
                    break
                else:
                    x = a
            if(x>-1):
                return x
    return x

#evaluating scores
def evaluate(a,p):
    s1 = 0
    if p == 2:
        opp = 1
    else:
        opp = 2
    #if a.count(p) == 4:
    #    s += 10000
    if a.count(p) == 3 and a.count(0) == 1:
        s1 += 10
    elif a.count(p) == 2 and a.count(0) == 2:
        s1 += 7
    #deducting scores if the opponent has an advantage
    #if a.count(opp) == 4:
    #    s -= 10000
    if a.count(opp) == 3 and a.count(0) == 1:
        s1 -= 150
    #elif a.count(opp) == 2 and a.count(0) == 2:
    #    s -= 15
    return s1

#assigning scores for moves
def score_move(board,p):
    s = 0
    #checking for rows
    for i in range (MAX_ROWS):
        for j in range (MAX_COLS-3):
            r = board[i][j:j+4]
            s += evaluate(r,p)
    #checking for columns
    col_arr = [[board[i][j] for i in range (MAX_ROWS)] for j in range (MAX_COLS)]
    for i in range (MAX_COLS):
        for j in range (MAX_ROWS-3):
            c = col_arr[i][j:j+4]
            s += evaluate(c,p)
    #positive diagonals
    for i in range (MAX_ROWS-1,2,-1):
        for j in range (MAX_COLS-3):
            pd = [board[i-x][j+x] for x in range (4)]
            s += evaluate(pd,p)
    #negative diagonals
    for i in range (MAX_ROWS-1,2,-1):
        for j in range (MAX_COLS-1,2,-1):
            nd = [board[i-x][j-x] for x in range (4)]
            s += evaluate(nd,p)
    #giving preference for center col so its easier to build stuff in the future
    center_arr = col_arr[MAX_COLS//2]
    s += center_arr.count(p)*7
    return s

def valid_cols(board):
    v = []
    for i in range(MAX_COLS):
        if(valid_choice(board,i)):
            v.append(i)
    return v

def minimax(board,max_player,d,m,alpha,beta):
    if winning_check(board,2)>0:
        return (None,math.inf)
    if winning_check(board,1)>0:
        return (None,-math.inf)
    if moves >= 42:
        return (None,0)
    if d == 0:
        return (None,score_move(board,2))
    vc = valid_cols(board)
    if max_player:
        val = -math.inf
        col = random.choice(vc)
        for c in vc:
            r = get_row(board,c)
            drop_piece(board,c,r,2)
            score = minimax(board,False,d-1,m+1,alpha,beta)[1]
            drop_piece(board,c,r,0)
            if score> val:
                val = score
                col = c
            alpha = max(alpha,val)
            if alpha >= beta:
                break
        return col,val
    else:
        val = math.inf
        col = random.choice(vc)
        for c in vc:
            r = get_row(board,c)
            drop_piece(board,c,r,1)
            score = minimax(board,True,d-1,m+1,alpha,beta)[1]
            drop_piece(board,c,r,0)
            if score< val:
                val = score
                col = c
            beta = min(val,beta)
            if beta <= alpha:
                break
        return col,val


def draw_main_screen():
	screen.fill(black)

	Welcome = Initial_Font.render("Connect-4 Game", True, blue).convert_alpha()
	screen.blit(Welcome, (60,100))

	Name = Initial_Font.render("     By Group 18", True, green).convert_alpha()
	screen.blit(Name, (40,230))

	pygame.draw.rect(screen, (255,0,0), (180, 390, 380, 100))
	pygame.draw.rect(screen, (255,255,0), (180, 520, 380, 100))
	
	SinglePlayer = Winning_Font.render("Singleplayer", True, white)
	MultiPlayer = Winning_Font.render("Multiplayer", True, white)
	screen.blit(SinglePlayer, (200,390))
	screen.blit(MultiPlayer, (210,520))
	
	pygame.display.update()

def set_mode():
	while(True):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				x_val = event.pos[0]
				y_val = event.pos[1]
				if x_val >= 180 and x_val <= 180 + 380:
					if y_val >= 390 and y_val <= 490:
						return 1
					elif y_val >= 520 and y_val <= 620:
						return 2

def draw_singleplayer():
	screen.fill(black)
	
	Diff = Winning_Font.render("Choose Difficulty", True, blue)
	screen.blit(Diff, (130,100))
	pygame.draw.rect(screen, (255,0,0), (200, 260, 300, 100))
	pygame.draw.rect(screen, (255,255,0), (200, 390, 300, 100))
	pygame.draw.rect(screen, (0,255,0), (200, 520, 300, 100))	

	Easy = Winning_Font.render("Easy", True, white)
	Medium = Winning_Font.render("Medium", True, white)
	Hard = Winning_Font.render("Hard", True, white)
	
	screen.blit(Easy, (280,260))
	screen.blit(Medium, (240,390))
	screen.blit(Hard, (280,520))

	pygame.display.update()


def set_diff():
	while(True):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				x_val = event.pos[0]
				y_val = event.pos[1]
				if x_val >= 200 and x_val <= 500:
					if y_val >= 260 and y_val <= 360:
						return 1
					elif y_val >= 390 and y_val <= 490:
						return 3
					elif y_val >= 520 and y_val <= 620:
						return 5
def set_player():
	screen.fill(black)

	Welcome = Initial_Font.render("Who will make the", True, green)
	screen.blit(Welcome, (20,100))

	Name = Initial_Font.render("First Move", True, green)
	screen.blit(Name, (150,200))

	pygame.draw.rect(screen, red, (200, 370, 300, 100))
	pygame.draw.rect(screen, yellow, (200, 500, 300, 100))
	
	You = Winning_Font.render("You", True, white)
	Comp = Winning_Font.render("Computer", True, white)
	screen.blit(You, (300,370))
	screen.blit(Comp, (210,500))
	
	pygame.display.update()

	while(True):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				x_val = event.pos[0]
				y_val = event.pos[1]
				if x_val >= 200 and x_val <= 500:
					if y_val >= 370 and y_val <= 470:
						return 1
					elif y_val >= 500 and y_val <= 600:
						return 2


while(True):
    moves = 0
    ongoing = True
#Drawing the main screen and setting the mode
    draw_main_screen()
    mode = set_mode()


#Creating and drawing the board
    board = create_board()
    draw_board()


#Let the games begin!!
#mode = 1

    if mode == 1:
        draw_singleplayer()
        d = set_diff()
        first = set_player()
        draw_board()
        while ongoing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ongoing = False
                    exit()
            
                if(moves%2 == 0):
                    p = 1
                else:
                    p = 2
                if p==first:
                    if event.type == pygame.MOUSEMOTION:
                        x_pos = event.pos[0]
                        pygame.draw.rect(screen,black,(0,0,width,100))
                        if first == 1:
                            pygame.draw.circle(screen, red, (x_pos,50), 40)
                        else:
                            pygame.draw.circle(screen, yellow, (x_pos,50), 40)
                        pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x_val = event.pos[0]
                        c = int(x_val/100)
                        if(valid_choice(board,c)):
                            r = get_row(board,c)
                            drop_piece(board,c,r,p)
                            put_token(c,r,p)
                            moves += 1
                            w = winning_check(board,1)
                        if(w>0):
                            for i in range (MAX_ROWS):
                                print(*board[i])
                            print("GAME OVER!")
                            print("PLAYER",p,"HAS WON!", sep = ' ')
                            ongoing = False
                            break
                        if(moves >= 42):
                            print("GAME OVER!")
                            for i in range (MAX_ROWS):
                                print(*board[i])
                            print("DRAW")
                            ongoing = False

                    
            #for i in range (MAX_ROWS):
            #    print(*board[i])
            #print()
            #if p == 1:
            #    c = int(input("Enter the column:"))
                else:
                    c, minimax_score = minimax(board,True,d,moves,-math.inf,math.inf)
                #print(minimax_score)
                    r = get_row(board,c)
                    drop_piece(board,c,r,p)
                    put_token(c,r,p)
                    moves += 1
                    w = winning_check(board,p)
                    if(w>0):
                        for i in range (MAX_ROWS):
                            print(*board[i])
                        print("GAME OVER!")
                        print("PLAYER",p,"HAS WON!", sep = ' ')
                        ongoing = False
                        break
                    if(moves >= 42):
                        print("GAME OVER!")
                        for i in range (MAX_ROWS):
                            print(*board[i])
                        print("DRAW")
                        ongoing = False
        if p == 1:
            if first == 1:
                winner = Winning_Font.render("THE USER HAS WON!", True, red)
            else:
                winner = Winning_Font.render("COMPUTER HAS WON!", True, red)
        elif p==2:
            if first == 1:
                winner = Winning_Font.render("COMPUTER HAS WON!", True, yellow)
            else:
                winner = Winning_Font.render("THE USER HAS WON!", True, yellow)
        elif moves>=42:
            winner = Winning_Font.render("DRAW", True, white)
        game_over = Final_Font.render("GAME OVER!", True, white)
        pygame.draw.rect(screen,black,(0,0,width,100))
        pygame.display.update()
        screen.blit(winner, (10,0))
        screen.blit(game_over, (0,250))
        pygame.display.update()
        pygame.time.wait(5000)
    if mode == 2:
        while ongoing:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ongoing = False
                    exit()
                                        
                for i in range (MAX_ROWS):
                    print(*board[i])
            
                if (moves%2 == 0):
                    p = 1
                else:
                    p = 2
            
                if event.type == pygame.MOUSEMOTION:
                    x_pos = event.pos[0]
                    pygame.draw.rect(screen, black, (0,0,width,100))
                    if p == 1:
                        pygame.draw.circle(screen,red,(x_pos,50),40)
                    else:
                        pygame.draw.circle(screen,yellow,(x_pos,50),40)
                    pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos = event.pos[0]
                    c = int(x_pos/100)
                
            #c = int(input("Enter the column:"))
                    if valid_choice(board,c):
            #while (b == False):
            #    c = int(input("Enter the column:"))
            #    b = valid_choice(board,c)
                        r = get_row(board,c)
                        drop_piece(board,c,r,p)
                        put_token(c,r,p)
                        moves += 1
                        w = winning_check(board,p)
                        if(w>0):
                            for i in range (MAX_ROWS):
                                print(*board[i])
                            print("GAME OVER!")
                            print("PLAYER",p,"HAS WON!", sep = ' ')
                            pygame.draw.rect(screen, black, (0,0,width,100))
                            ongoing = False
                            break
                        if(moves >= 42):
                            print("GAME OVER!")
                            for i in range (MAX_ROWS):
                                print(*board[i])
                            print("DRAW")
                            ongoing = False
                            break
        if p == 1:
            winner = Winning_Font.render("PLAYER 1 HAS WON!", True, red)
        elif p==2:
            winner = Winning_Font.render("PLAYER 2 HAS WON!", True, yellow)
        elif moves>=42:
            winner = Winning_Font.render("DRAW", True, white)
        game_over = Final_Font.render("GAME OVER!", True, white)
        pygame.draw.rect(screen,black,(0,0,width,100))
        pygame.display.update()
        screen.blit(winner, (45,0))
        screen.blit(game_over, (0,250))
        pygame.display.update()
        pygame.time.wait(5000)
