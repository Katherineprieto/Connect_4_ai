import numpy as np
import pygame
import sys
import math


GREEN = (60,92,62)
GRAY = (164, 182, 165)
DARK = (10, 44, 12)
LIGHT = (217, 228, 218)
BLACK = (0,0,0)


# Static variables that do not change throughout the program are capitalized
ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    # 0 represents flipping the board along its axis because in numpy the top left corner is 0,0
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[c][r+2] == piece and board[c][r+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c]:
                return True
    # Check for diagonal locations -- positively sloped
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3]:
                return True

    # Check for diagonal locations -- negatively sloped
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, GREEN, (c*SQUARESIZE, (r*SQUARESIZE+SQUARESIZE), SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, GRAY, (c*SQUARESIZE+SQUARESIZE/2, r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, DARK, (c*SQUARESIZE+SQUARESIZE/2, height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, LIGHT, (c*SQUARESIZE+SQUARESIZE/2, height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

# Initialize your game board
board = create_board()
print_board(board)
game_over = False # Ensure that your while loop is continuous
turn = 0 # Helps distinguish player one and player two

pygame.init()
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, DARK, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, LIGHT, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.pos)
            # Ask for Player 1 input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    if winning_move(board, 1):
                        print(" Player 1 wins! ")
                        game_over = True

            #
            # Ask for Player 2 input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    if winning_move(board, 2):
                        print(" Player 2 Wins! ")
                        game_over = True
            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2