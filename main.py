import sys
import copy
import pygame
import asyncio
import numpy as np
WIDTH = 600
HEIGHT = 600

ROWS = 3 
COLS = 3

SQSIZE = WIDTH //COLS
LINE_WIDTH = 5

#COLORS
BG_COLOR = (20, 170, 156)
LINE_COLOR = (0, 0, 0)

#CIRCLE
CIRC_COLOR = (239, 231, 150)
RADIUS = SQSIZE//4
CIRC_WIDTH = 10

#CROSS
CRO_COLOR = (239, 131, 100)
CRO_WIDTH = 10

OFFSET = 50


# PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)

font = pygame.font.Font(None, 200)

class Board:
    
    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )
        self.empty_sqrs = self.squares
        self.mark_sqrs = 0
    
    def final_state(self):
        #return 0 if there is no win yet
        #return 1 if player 1 win
        #return 2 if player 2 

        #vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
        
        #horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]

        #decs diagnal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]
        
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[1][1]
        
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.mark_sqrs += 1
        
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0 
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row,col):
                    empty_sqrs.append( (row, col) )

        return empty_sqrs
    
    def isfull(self):
        return self.mark_sqrs == 9
    
    def isempty(self):
        return self.mark_sqrs == 0
    
    

class AI():
    
    def __init__(self, player=2):
        self.player = player
        
    def minimax(self, board, maximizing):

        case = board.final_state()

        #player 1 wins
        if case == 1:
            return 1, None

        #player 2 wins
        if case == 2:
            return -1, None
        
        #draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move =None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            
            return max_eval, best_move
        
        elif not maximizing:
            min_eval = 100
            best_move =None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            
            return min_eval, best_move
        
    def eval(self, main_board):
        eval, move = self.minimax(main_board, False)
        
        return move
    
class Game():

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.running = True
        self.show_line()
        self.player = 1 #1-x 2-o

    def show_line(self):
        # Vertical lines
        for i in range(1, 3):
            pygame.draw.line(screen, LINE_COLOR, (WIDTH * i // 3, 0), (WIDTH * i // 3, HEIGHT), LINE_WIDTH) 
        # Horizontal lines
        for i in range(1, 3):
            pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT * i // 3), (WIDTH, HEIGHT * i // 3), LINE_WIDTH) 

    
    def draw_icon(self, row, col):
        center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
        if self.player == 1:
            # Draw cross
            pygame.draw.line(screen, CRO_COLOR, (center[0] - RADIUS, center[1] - RADIUS), (center[0] + RADIUS, center[1] + RADIUS), CRO_WIDTH)
            pygame.draw.line(screen, CRO_COLOR, (center[0] - RADIUS, center[1] + RADIUS), (center[0] + RADIUS, center[1] - RADIUS), CRO_WIDTH)
        elif self.player == 2:
            # Draw circle
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)
    
    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_icon(row, col)
        self.next_player()
    
    def next_player(self):
        self.player = self.player % 2 + 1

    def isover(self):
        if self.board.final_state() == 1:
            text_surface = font.render('You Win', True, (255, 255, 0))  # Render the text onto a surface
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text_surface, text_rect)
        elif self.board.final_state() == 2:
            text_surface = font.render('You Lose', True, (200, 90, 100))
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text_surface, text_rect)
        elif self.board.isfull():
            text_surface = font.render('Draw', True, (90, 0, 255))
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text_surface, text_rect)
        
        
        return self.board.final_state() != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

async def main():
    game = Game()
    board = game.board
    ai = game.ai
    #main game
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game.running:
                    screen.fill(BG_COLOR)
                    game.reset()
                    board = game.board
                    ai = game.ai
                else:
                    pos = event.pos
                    row = pos[1]//SQSIZE
                    col = pos[0]//SQSIZE
                    
                    if board.empty_sqr(row, col) and game.running:
                        game.make_move(row, col)

                        if game.isover():
                            game.running = False
                
                

        if game.player == ai.player and game.running:

            # update the screen
            pygame.display.update()

            # eval
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False
    
        
            
        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())
