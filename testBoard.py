import unittest 
from should_dsl import * #matchers
from g10Board import *

INITIAL = "r.b..b.rpppppppp................................PPPPPPPPR.B..B.R"

class BoardTest(unittest.TestCase):
    def simpleState(self):
        state = {}
        state['board'] = INITIAL
        state['who_moves'] = 1
        return state
        
    def testPieceMovement(self):
        b = Board(self.simpleState())
	s = b.makeMove([(0,1),(0,2)])
        self.assertIsNot(s, b, " Assert makeMove is immutable. ")			
if __name__ == '__main__':
	unittest.main()
