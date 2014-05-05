""""Board"""
import time
import random
import copy
from base_client import LiacBot
from g10pieces import  *

WHITE = 1
BLACK = -1
NONE = 0

PIECES = {
        'r': Rook,
        'p': Pawn,
        'b': Bishop,
        }

PAWN = 'p'

WIN_VALUE = 100 
LOSE_VALUE = -100
class Board(object):
    def __init__(self, state):
        self.cells = [[None for j in xrange(8)] for i in xrange(8)]
        self.pieces = []
        self.black_pieces = []
        self.white_pieces = []

        
        self.winner = state['winner'] 
        self.draw = state['draw']        
        self.team = state['who_moves']
        self.other_team = WHITE if (self.team == BLACK) else BLACK
        self.who_moves = self.team
        self.enpassant = state['enpassant']


        
        c = state['board']
        i = 0

        self.win_methods = [self.win_pawncapture, self.win_pawnpromotion] 
        for row in xrange(7, -1, -1):
            for col in xrange(0, 8):
                if c[i] != '.':

                    cls = PIECES[c[i].lower()]
                    piece = cls(self, self.team, (row, col))
                    if c[i].lower() == c[i] :
                        self.black_pieces.append(piece) 

                    else:
                        self.white_pieces.append(piece)

                    self.pieces.append(piece)
                    self.cells[row][col] = piece


                i += 1

    def is_valid_move(self, from_pos, to_pos):
        dest_row, dest_col = to_pos

        if not 0 <= dest_row <= 7 or not 0 <= dest_col <= 7:
            return False

        from_piece = self[from_pos]
        if from_piece is None:
            return False

        if from_piece.team != self.who_moves:
            return False

        if not from_piece.is_valid_move(to_pos):
            return False

        return True

    def _verify_win(self):
        for win in self.win_methods:
            r = win()
            if r != NONE:
                self.winner = r
                return


    def raw_move(self, from_pos, to_pos):
        from_piece = self[from_pos]
        to_piece = self[to_pos]

        if to_piece is not None:
            self.remove_piece(to_piece)

        self[to_pos] = from_piece
        self[from_pos] = None
        from_piece.move_to(to_pos)

    def move(self, from_pos, to_pos):
        from_piece = self[from_pos]
        to_piece = self[to_pos]

        # Change bad move state
        self.bad_move = False

        # Verify if it is a valid move
        if not self.is_valid_move(from_pos, to_pos):
            self.bad_move = True
            self._verify_win()
            return

        # Verify if it is an enpassant capture
        if self.enpassant and from_piece.type == PAWN:
            if to_pos[0] == self.enpassant[0] and to_pos[1] == self.enpassant[1]:
                to_piece = self.enpassant_piece

        # Verify if it is a capture (to remove from lists)
        if to_piece is not None:
            self.remove_piece(to_piece)

        # Clear enpassant state
        self.enpassant = None
        self.enpassant_piece = None

        # Change enpassant state, if possible
        if from_piece.type == PAWN:
            d = abs(from_pos[0]-to_pos[0])
            left = self[to_pos[0], to_pos[1]-1]
            right = self[to_pos[0], to_pos[1]+1]

            has_left_pawn = (left is not None and left.type == PAWN)
            has_right_pawn = (right is not None and right.type == PAWN)

            if d == 2 and (has_left_pawn or has_right_pawn):
                row = (to_pos[0]+from_pos[0])//2
                col = to_pos[1]
                self.enpassant = (row, col)
                self.enpassant_piece = from_piece

        # Change s state
        if self.who_moves == WHITE:
            self.who_moves = BLACK
        else: self.who_moves = WHITE

        # Change positions
        self[to_pos] = from_piece
        self[from_pos] = None
        from_piece.move_to(to_pos)#position = to_pos


        # Verify winning
        self._verify_win()
    
    def set_board(self, c):
        i = 0
        for row in xrange(7, -1, -1):
            for col in xrange(0, 8):
                if c[i] != '.':
                    self.new_piece(c[i], (row, col))

                i += 1

    def new_piece(self, type_, pos):
        cls = PIECES[type_.lower()]
        piece = cls(self, team, pos)
        self._cells[pos[0]][pos[1]] = piece
        self.pieces.append(piece)
        if type_.lower() == type_:
            self.black_pieces.append(piece)
        else:
            self.white_pieces.append(piece)

    def __getitem__(self, pos):
        if not 0 <= pos[0] <= 7 or not 0 <= pos[1] <= 7:
            return None

        return self.cells[pos[0]][pos[1]]

    def __setitem__(self, pos, value):
        self.cells[pos[0]][pos[1]] = value

    def is_empty(self, pos):
        return self[pos] is None


    def generate(self):
        moves = []
        my_pieces = self.black_pieces if self.who_moves == BLACK else self.white_pieces   
        for piece in my_pieces:
            ms = piece.generate()
            ms = [(piece.position, m) for m in ms]
            moves.extend(ms)

        return moves

    def remove_piece(self, piece):
        pos = piece.position
        self[pos] = None

        self.pieces.remove(piece)
        if piece.team == BLACK:
            self.black_pieces.remove(piece)
        else:
            self.white_pieces.remove(piece)

    def win_pawncapture(self):
        has_black_pawn = any([p.type == PAWN for p in self.black_pieces])
        has_white_pawn = any([p.type == PAWN for p in self.white_pieces])

        if not has_black_pawn:
            return WHITE

        if not has_white_pawn:
            return BLACK

        return NONE

    def win_pawnpromotion(self):
        for p in self.white_pieces:
            if p.type == PAWN and p.position[0] == 7:
                return WHITE

        for p in self.black_pieces:
            if p.type == PAWN and p.position[0] == 0:
                return BLACK

        return NONE

    def is_enpassant(self, pos):
        enp = self.enpassant
        return enp and enp[0] == pos[0] and enp[1] == pos[1]

    def __copy__(self):
        return copy.deepcopy(self)

    def makeMove(self, movement):
        next_state = self.__copy__()
        next_state.move(movement[0], movement[1])
        return next_state

    
    def heuristic(self):
        ac = 0
        for	piece in self.white_pieces:
            ac += piece.evaluations()
        for piece in self.black_pieces:
            ac -= piece.evaluations()
        if self.team == WHITE:
            return ac
        else:
            return -ac