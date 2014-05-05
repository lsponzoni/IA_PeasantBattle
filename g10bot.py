import sys
from base_client import LiacBot
from g10Board import Board
from g10pieces import *

WHITE = 1
BLACK = -1

def complemento(cor):
    return - cor

def negaMaxMinWithPrune(board, depth, lim_inf, lim_sup, color):
    moves = board.generate() 
    if depth == 0 or moves == None:
        return None, board.heuristic(color) 
    best_move = None
    best_chance = lim_inf
    for movement in moves:
        nextBoard = board.makeMove(movement)
        compl = complemento(color)
        predicao, mchance = negaMaxMinWithPrune(nextBoard, 
                depth -1, -lim_sup, -lim_inf, compl )
        chance = - mchance	
        if chance > best_chance:
            best_move = movement
            best_chance = chance
        if lim_inf >= lim_sup:
            break


    return best_move, best_chance

#=====================================
class G10Bot(LiacBot):
    name = 'Bot do Grupo 10'
    ip = '127.0.0.1'
    depth =  2

    def __init__(self, color, port):
        super(G10Bot, self).__init__()
        self.port = port
        self.color = color

    def select_move(self, board):
        M_INF = -10000
        P_INF = 10000
        move, ignore = negaMaxMinWithPrune(board, self.depth,M_INF, P_INF,self.color)
        return move	

    def on_move(self, state):
        board =	Board(state)
        move = self.select_move(board)
        self.send_move(move[0], move[1])
        print move
        
    def on_game_over(self, state):
        print 'Game Over'
#======================================
if __name__ == '__main__':
    color = WHITE 
    port = 50100

    if len(sys.argv) > 1:
        if sys.argv[1] == 'black':
            color = BLACK
            port = 50200
    bot = G10Bot(color, port)
    bot.port = port
    bot.start()
