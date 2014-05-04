import sys
from base_client import LiacBot
from g10Board import Board
from g10pieces import *

MIN = 1
MAX = 0
def maxPlay(board, level):
        M_INF = -10000
        P_INF = 10000
        return alphaBetaMaxMin(board, level, M_INF, P_INF)

def maxMin(board, alfa, beta, depth):
	maxMinWithCut(board, depth, alfa, beta, minMax)
	

def maxMinWithCut(board, depth, lim_inf, lim_sup, minMax):
        if level == 0:
		return board.heuristic()  
	if board.gameEnded() != None:
		return board.gameEnded()
	if minMax == MAX :
		bestMove = 
		for move in board.generate():
               		nextBoard = board.makeMove(move)
			= alfabeta(board, level , alfa, beta, MIN)
			
	if minMax == MIN:
		alfabeta(board, level - 1, alfa, beta, MAX)

def MinMax(moves, board):
	for move in moves:
		board.makeMove(move[0], move[1]) 

# :This is the line that theoretically
# changes between both functions...
# actually board takes care of that...        
def searchBestMove(moves, board):
        bestHeuristicValue = board.MIN_HEURISTIC
        bestMove = moves[0]
        for move in moves: 
                utility = board.makeMove(move).heuristic()
                if( bestHeuristicValue < utility):
                        bestMove = move
        return (bestMove, utility)
#=====================================
class G10Bot(LiacBot):
	name = 'Bot do Grupo 10'
	ip = '127.0.0.1'
	port = 50100
	color = 0
	
	def select_move(self, moves, board):
                return maxPlay(moves, board, 2)
		
	
	def __init__(self, color, port):
		super(G10Bot, self).__init__()
		self.port = port
		self.color = color

	def on_move(self, state):
		board =	Board(state)
		moves = board.generate()
		move = self.select_move(moves, board)
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
