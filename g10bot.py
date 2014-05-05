import sys
from base_client import LiacBot
from g10Board import Board
from g10pieces import *

MIN = 1
MAX = 0

def maxPlay(board, level):
        M_INF = -10000
        P_INF = 10000
        move, i = maxMinWithPrune(board, level, M_INF, P_INF, MAX)
 	return move	

def maxMinWithPrune(board, depth, lim_inf, lim_sup, minMax):
	if depth == 0 or board.winner != None or board.draw:
		return board.heuristic() 
	possible_movements = board.generate()	
	best_move = None
	if minMax == MAX :
		best_chance = lim_inf
		for movement in possible_movements:
               		nextBoard = board.makeMove(movement)
			s, chance  = maxMinWithPrune(nextBoard, depth - 1, best_chance, lim_sup, MIN)
			if chance > best_chance:
				best_move = movement
				best_chance = chance
			if best_chance >= lim_sup:
				break
		return best_move, best_chance
	if minMax == MIN:
		best_chance = lim_sup
		for movement in possible_movements:
               		nextBoard = board.makeMove(movement)
			s, chance  = maxMinWithPrune(nextBoard, depth - 1, lim_inf, best_chance, MIN)
			if chance < best_chance:
				best_move = movement
				best_chance = chance
			if best_chance <= lim_inf:
				break
		return best_move, best_chance
#=====================================
class G10Bot(LiacBot):
	name = 'Bot do Grupo 10'
	ip = '127.0.0.1'
	port = 50100
	color = 0
	

	def __init__(self, color, port):
		super(G10Bot, self).__init__()
		self.port = port
		self.color = color

	def select_move(self, board):
		return maxPlay(board, 12)

	def on_move(self, state):
		board =	Board(state)
		move = self.select_move(board)
		self.send_move(move[0], move[1])
		
	def on_game_over(self, state):
		print 'Game Over'
#======================================
if __name__ == '__main__':
    color = 0
    port = 50100

    if len(sys.argv) > 1:
    	if sys.argv[1] == 'black':
    		color = 1
           	port = 50200
    bot = G10Bot(color, port)
    bot.port = port
    bot.start()
