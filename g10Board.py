""""Board"""
import time
import random
import copy
from base_client import LiacBot
from g10pieces import (Piece, Pawn, Rook, Bishop)
from g10color import (white, black, complemento)

PIECES = {
        'r': Rook,
        'p': Pawn,
        'b': Bishop,
        }


def sizeW(board):
    return len(board.white_pieces)
def sizeB(board):
    return len(board.black_pieces)
 
def linear_to_map(x):
    s = x/8
    return (7 - s, s - x)

def out_of_world(position):
    i, j = position
    return not (0 <= i <= 7 and 0 <= j <= 7)

class Board(object):
    def __init__(self, state):
        self.cells = [[None for j in xrange(8)] for i in xrange(8)]
        self.white_pieces = []
        self.black_pieces = []

        self.error = state['bad_move']
        self.enpassant = state['enpassant']
        self.who_moves = state['who_moves']
        self.set_board(state['board'])

    def set_board(self, c):
        i = 0
        for row in xrange(7, -1, -1):
            for col in xrange(0, 8):
                if c[i] != '.':
                    self.new_piece(c[i], (row, col))
                i += 1

    def new_piece(self, type_, pos):
        team = white() if type_.isupper() else black()
        cls = PIECES[type_.lower()]
        piece = cls(self, team, pos)
        self.cells[pos[0]][pos[1]] = piece
        if team == black():
            self.black_pieces.append(piece)
        else:
            self.white_pieces.append(piece)

    def makeMove(self, movement):
        next_state = self.__copy__()
        next_state.move(movement[0], movement[1])
        return next_state

    def move(self, from_pos, to_pos):
        self.who_moves = complemento(self.who_moves)
        from_piece = self[from_pos]
        to_piece = self[to_pos]

        if to_piece is not None:
            self.kill_piece(to_piece)

        self.remove_piece(from_piece)
        self[to_pos] = from_piece
        from_piece.move_to(to_pos)

    def remove_piece(self, piece):
        pos = piece.position
        self[pos] = None

    def __copy__(self):
        return copy.deepcopy(self)

    def __getitem__(self, pos): # It won't receive invalid positions.
        if out_of_world(pos):
            return None
        i, j = pos
        return self.cells[i][j]

    def __setitem__(self, pos, value):
        if not out_of_world(pos):
            i, j = pos
            self.cells[i][j] = value

    def is_empty(self, pos):
        return self[pos] is None

    def my_pieces(self):
        iswhite = self.who_moves == white()
        return  self.white_pieces if iswhite else self.black_pieces


    def generate(self):
        moves = []
        for piece in self.my_pieces():
            destinies = piece.generate()
            piece_moves = [(piece.position, m) for m in destinies]
            moves.extend(piece_moves)
        return moves


    def kill_piece(self, piece):
        self.remove_piece(piece)
        if piece.team == black():
            self.black_pieces.remove(piece)
        else:
            self.white_pieces.remove(piece)

    def heuristic(self):
        ac = 0
        for piece in self.white_pieces:
            ac += piece.evaluations()
        for piece in self.black_pieces:
            ac -= piece.evaluations()
        if self.who_moves == black():
            ac = -ac
        return ac

    def is_enpassant(self, pos):
        enp = self.enpassant
        return enp and enp[0] == pos[0] and enp[1] == pos[1]


