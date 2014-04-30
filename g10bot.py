import sys
from base_client import LiacBot
from g10Board import Board
#=====================================
class G10Bot(LiacBot):
	name = 'Bot do Grupo 10'
	ip = '127.0.0.1'
	port = 50100
	color = 0
	
	def select_move(self, moves, board):
		# min max...
		return moves[0]
	
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
