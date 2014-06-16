import sys
from base_client import LiacBot
from g10Board import (Board)
from g10color import (white, black)
from random import choice

M_INF = -10000
P_INF = 10000

def nega_max_with_prune(board, depth, lim_inf, lim_sup):
    moves = board.generate()
    best_move = choice(moves)
    best_chance = lim_inf
    for movement in moves:
        if best_chance >= lim_sup:
            break

        nextBoard = board.makeMove(movement)
        chance = - justNegamaxWork(nextBoard, depth - 1,
                -lim_sup, -best_chance)

        if chance > best_chance:
            best_move = movement
            best_chance = chance
    print "Best Chance %s" % best_chance 
    return best_move, best_chance

def justNegamaxWork(b, d, li, ls):
    ms = b.generate()
    if ms == [] or d == 0:
        return b.heuristic() 
    bc = li
    for m in ms:
        if bc >= ls:
            break
        nb = b.makeMove(m)
        c = - justNegamaxWork(nb, d - 1, -ls, -bc)
        if c > bc:
            bc = c
    return bc

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
        move = nega_max_with_prune(board, self.depth, 
                M_INF, P_INF)
        return move	

    def on_move(self, state):
        board =	Board(state)
        move = self.select_move(board)
        self.send_move(move[0], move[1])
        print "Move (%s) -> (%s)" % (move[0], move[1])
    def on_game_over(self, state):
        print 'Game Over'
#======================================
if __name__ == '__main__':
    color = white() 
    port = 50100

    if len(sys.argv) > 1:
        if sys.argv[1] == 'black':
            color = black()
            port = 50200
    bot = G10Bot(color, port)
    bot.port = port
    bot.start()
