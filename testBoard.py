import unittest
from should_dsl import * #matchers
from g10Board import *
from g10color import (white, black)
INITIAL = "r.b..b.rpppppppp................................PPPPPPPPR.B..B.R"
def sizeW(board):
    return len(board.white_pieces)
def sizeB(board):
    return len(board.black_pieces)
 
class BoardTest(unittest.TestCase):
    def setUp(self):
        self.board = Board(self.simpleState())

       
    def simpleState(self):
        state = {}
        state['board'] = INITIAL
        state['who_moves'] = white()
        state['bad_move'] = False
        state['enpassant'] = (1, 2)
        return state

    def testPieceRecover(self):
        b  = self.board
        p = [6, 2]
        p2 =[0, 0]
        p3 =[0, 2]
        p4 =[0, 1]
        c = b[p]
        self.assertItemsEqual(p, c.position,\
                "Assert in synchro with pieces position.")
        self.assertIsNotNone(b[p2],\
                "Assert there is something at %s" % p2)
        self.assertIsNotNone(b[p3],\
                "Assert there is something at %s" % p3)
        self.assertIsNone(b[p4],\
                "Assert there is nothing at %s" % p4)

    def testMovementMovesPieces(self):
        b  = self.board
        from_ = (0, 0)
        to_ = (0, 1)
        s = b.makeMove([from_, to_])
        self.assertEquals(b[from_].kind, s[to_].kind,\
                "move works.")
        self.assertEquals(sizeW(b), sizeB(b),\
                "both sides sizes start same.")
        self.assertEquals(sizeW(b), sizeW(s),\
                "when no piece is killed,\
                size is invariant to movement.")
 
    def testKillAPiece(self):
        b = self.board
        from_ = (1,1)
        to_ = (6,1)
        unrelated_position1 = (6,2)
        unrelated_position2 = (5,2)
        s = b.makeMove([from_, to_])
        g = s.makeMove([unrelated_position1, unrelated_position2])
        self.assertEquals(sizeW(b), sizeB(b),\
                "before killing sizes are same.")
        self.assertLess(sizeB(s), sizeB(b),
                "black piece has been killed and \
               \n black size dwindles.")
        self.assertEquals(sizeB(g), sizeB(s),\
                "don't change size in normal moves")
        self.assertGreater(sizeW(s), sizeB(s),\
                "after killing one black piece white has more pieces")
        self.assertGreater(g.heuristic(), s.heuristic(),\
                "After kill, heuristic goes up")
 
    def testPieceMakeMoveIsImutable(self):
        b  = self.board
        from_ = (0, 0)
        to_ = (0, 1)
        unrelated_position = [6,1] 
        s = b.makeMove([from_, to_])
        self.assertIsNot(s, b, " makeMove is immutable.")
        self.assertIsNot(s[unrelated_position],\
                b[unrelated_position],\
                "should work on a deep :copy.")
        self.assertNotEqual(s[unrelated_position],
                b[unrelated_position], "shouldn't change caller.")

    def testWhatAreMyPieces(self):
        b = self.board
        b.who_moves = white()
        self.assertIsNotNone(b.my_pieces(),\
                "Should return my pieces aren't empty")
        self.assertItemsEqual(b.my_pieces(), b.white_pieces,\
                "my pieces should be white pieces\
                when who_moves is white") 
        b.who_moves = black()
        self.assertIsNotNone(b.my_pieces(),\
                "Should return my pieces when black aren't empty")
        self.assertItemsEqual(b.my_pieces(), b.black_pieces,\
                "my pieces should be black pieces\
                when who_moves is black") 
 
    def testMoveGenerate(self):
        b = self.board
        self.assertNotEquals([], b.generate(),\
                "Generates a set of moves.")

if __name__ == '__main__':
    unittest.main()
