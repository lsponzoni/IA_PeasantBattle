import unittest
from should_dsl import * #matchers
from g10Board import *

INITIAL = "r.b..b.rpppppppp................................PPPPPPPPR.B..B.R"

class BoardTest(unittest.TestCase):
    def setUp(self):
        self.board = Board(self.simpleState())
        
    def simpleState(self):
        state = {}
        state['board'] = INITIAL
        state['who_moves'] = 1
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
        self.assertEquals(b[from_].kind, s[to_].kind, "Assert move works.")

    def testKillAPiece(self):
        b = self.board
        from_ = (1,1)
        to_ = (6,1)
        s = b.makeMove([from_, from_])
        self.assertGreater(s.heuristic(), b.heuristic(),"Values")

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

if __name__ == '__main__':
    unittest.main()
