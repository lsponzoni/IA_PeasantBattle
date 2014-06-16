import numbers
from g10color import (white,black)
__all__ = ['Pawn', 'Rook', 'Bishop']

PAWN = 'p'
ROOK = 'r'
BISHOP = 'b'

FREEDOOM = 3
PPAWN = 5
WPAWN = 5
PROOK = 5
WROOK = 15 
PBISHOP = [2, 4, 5, 7, 7, 6, 4, 2] 
WBISHOP = 14

MAX = 10000

class Piece(object):
    def __init__(self):
        self.board = None
        self.team = None
        self.position = None
        self.kind = None

    def is_valid_move(self, pos):
        pass

    def move_to(self, pos):
        self.position = pos

    def generate(self):
        pass

    def is_opponent(self, piece): 
        return piece is not None and piece.team != self.team
       
    def evaluations(self):
        pass

    def positioningEvaluation(self):
        pass
    
    def materialEvaluation(self):
        pass
        
    def freedomEvaluation(self): 
        if isinstance(self.generate, numbers.Number):
            if self.team == WHITE:
                return -(len(self.generate) * FREEDOOM)
            else:
                return len(self.generate) * FREEDOOM
        else:
            return 0

    def defenseEvaluation(self):
        pass

    def supportEvaluation(self):
        pass

    def is_white(self):
        return self.team == white()

    def is_black(self):
        return self.team != white()

    def repr(self):
        return "%s%s%s" % (self.kind, 
                self.position[0], self.position[1])

       

class Pawn(Piece):
    def __init__(self, board, team, position):
        self.board = board
        self.team = team
        self.position = position
        self.kind = PAWN
        if self.is_white():
            self._has_moved = self.position[0] != 1
        else:
            self._has_moved = self.position[0] != 6

    def generate(self):
        moves = []
        my_row, my_col = self.position

        d = self.team

	    # Movement to 1 :forward
        pos = (my_row + d*1, my_col)
        if self.board.is_empty(pos):
            moves.append(pos)

    	# Movement to 2 forward
        if not self._has_moved:
            pos = (my_row + d*2, my_col)
            if self.board.is_empty(pos):
                moves.append(pos)

        # Normal capture to right
        pos = (my_row + d*1, my_col+1)
        piece = self.board[pos]
        if piece != None and self.is_opponent(piece) or\
                    self.board.is_enpassant(pos):
            moves.append(pos)

        # Normal capture to left
        pos = (my_row + d*1, my_col-1)
        piece = self.board[pos]
        if piece != None and self.is_opponent(piece) or\
                    self.board.is_enpassant(pos):
            moves.append(pos)

        return moves

    def positioningEvaluation(self):
        row, col = self.position
        ac = 0
        if self.is_white():
            if row != 7:
                ac = row*PPAWN
            else:
                ac = MAX
        else:
            if row != 0:
                ac = (7-row)*PPAWN
            else:
                ac = MAX
        return ac

    def materialEvaluation(self):
        return WPAWN

    def evaluations(self):
        return self.positioningEvaluation() +\
                self.materialEvaluation() +\
                self.freedomEvaluation()

    def move_to(self, pos):
        self._has_moved = True
        super(Pawn, self).move_to(pos)



class Rook(Piece):
        
    def __init__(self, board, team, position):
        self.board = board
        self.team = team
        self.position = position
        self.kind = ROOK

    def _col(self, dir_):
        my_row, my_col = self.position
        d = (-1 if dir_ < 0 else 1)
        for col in xrange(1, abs(dir_)):
            yield (my_row, my_col + d*col)

    def _row(self, dir_):
        my_row, my_col = self.position

        d = (-1 if dir_ < 0 else 1)
        for row in xrange(1, abs(dir_)):
            yield (my_row + d*row, my_col)

    def _gen(self, moves, gen, idx):
        for pos in gen(idx):
            piece = self.board[pos]

            if piece is None:
                moves.append(pos)
                continue

            elif piece.team != self.team:
                moves.append(pos)

            break

    def generate(self):
        moves = []

        my_row, my_col = self.position
        self._gen(moves, self._col, 8-my_col) # RIGHT
        self._gen(moves, self._col, -my_col-1) # LEFT
        self._gen(moves, self._row, 8-my_row) # TOP
        self._gen(moves, self._row, -my_row-1) # BOTTOM

        return moves

    def evaluations(self):
        return self.positioningEvaluation() +\
                self.materialEvaluation() +\
                self.freedomEvaluation()

    def positioningEvaluation(self):
        i, j = self.position
        if self.is_white():
            ac = PROOK - i
        else:
            ac = PROOK-(7-i)
        return ac

    def materialEvaluation(self):
        return WROOK

class Bishop(Piece):
    def __init__(self, board, team, position):
        self.board = board
        self.team = team
        self.position = position
        self.kind = BISHOP

    def _gen(self, moves, row_dir, col_dir):        
        my_row, my_col = self.position

        for i in xrange(1, 8):
            row = row_dir*i
            col = col_dir*i
            q_row, q_col = my_row+row, my_col+col

            if not 0 <= q_row <= 7 or not 0 <= q_col <= 7:
                break

            piece = self.board[q_row, q_col]
            if piece is not None:
                if piece.team != self.team:
                    moves.append((q_row, q_col))
                break

            moves.append((q_row, q_col))

    def generate(self):
        moves = []

        self._gen(moves, row_dir=1, col_dir=1) # TOPRIGHT
        self._gen(moves, row_dir=1, col_dir=-1) # TOPLEFT
        self._gen(moves, row_dir=-1, col_dir=-1) # BOTTOMLEFT
        self._gen(moves, row_dir=-1, col_dir=1) # BOTTOMRIGHT

        return moves

    def evaluations(self):
        return self.positioningEvaluation() +\
                self.materialEvaluation() +\
                self.freedomEvaluation()

    def positioningEvaluation(self):
       i, j = self.position
       return PBISHOP[i] + PBISHOP[j]

    def materialEvaluation(self):
        return WBISHOP
