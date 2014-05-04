

__all__ = ['Pawn', 'Rook', 'Bishop']

PAWN = 'p'
ROOK = 'r'
BISHOP = 'b'

class Piece(object):
    def __init__(self):
        self.board = None
        self.team = None
        self.position = None
	self.type = None

    def is_valid_move(self, pos):
        pass

    def move_to(self, pos):
        self.position = pos

    def generate(self):
        pass

    def is_opponent(self, piece):
        return piece is not None and piece.team != self.team

class Pawn(Piece):
    def __init__(self, board, team, position):
        self.board = board
        self.team = team
        self.position = position
	self.type = PAWN
        self._has_moved = False
        
    def generate(self):
        moves = []
        my_row, my_col = self.position
        
	# Movement to 1 forward
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
        if self.is_opponent(piece) or self.board.is_enpassant(pos):
            moves.append(pos)

        # Normal capture to left
        pos = (my_row + d*1, my_col-1)
        piece = self.board[pos]
        if self.is_opponent(piece) or self.board.is_enpassant(pos):
            moves.append(pos)

        return moves

    def move_to(self, pos):
        self._has_moved = True
        super(Pawn, self).move_to(pos)

    def is_valid_move(self, pos):
        query_row, query_col = pos
        my_row, my_col = self.position
        
        piece = self.board[pos]

        # multiply to self.team in order to ignore the direction
        d_row = self.team*(query_row - my_row)
        d_col = (query_col - my_col)

        # some conditions to verify if is a valid movement
        capture_move = abs(d_col) == 1 and d_row == 1
        valid_enpassant = self.board.enpassant is not None and \
                          pos[0] == self.board.enpassant[0] and \
                          pos[1] == self.board.enpassant[1]  
        opponent_piece = piece is not None and piece.team != self.team

        movement = (d_col == 0) and (piece is None) and \
                   (d_row == 1 or (d_row == 2 and not self._has_moved))
        capture = capture_move and (valid_enpassant or opponent_piece)
        # ------------------------------------------------

        # print 'capture_move', capture_move
        # print 'valid_enpassant', valid_enpassant
        # print 'opponent_piece', opponent_piece
        # print 'movement', movement
        # print 'capture', capture
        if movement or capture:
            return True

        return False




class Rook(Piece):
        
    def __init__(self, board, team, position):
        self.board = board
        self.team = team
        self.position = position
	self.type = ROOK
    def _col(self, dir_):
        my_row, my_col = self.position
        d = -1 if dir_ < 0 else 1
        for col in xrange(1, abs(dir_)):
            yield (my_row, my_col + d*col)

    def _row(self, dir_):
        my_row, my_col = self.position

        d = -1 if dir_ < 0 else 1
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
        
    def is_valid_move(self, pos):
        query_row, query_col = pos
        my_row, my_col = self.position
        
        d_row = (query_row - my_row)
        d_col = (query_col - my_col)

        piece = self.board[pos]

        if d_row and d_col:
            return False

        if not(d_row or d_col):
            return False

        if piece is not None and piece.team == self.team:
            return False

        row_direction = -1 if d_row < 0 else 1
        for row in xrange(1, abs(d_row)):
            piece = self.board[(my_row+row_direction*row, my_col)]
            if piece is not None:
                return False

        col_direction = -1 if d_col < 0 else 1
        for col in xrange(1, abs(d_col)):
            piece = self.board[(my_row, my_col+col_direction*col)]
            if piece is not None:
                return False

        return True

class Bishop(Piece):
    def __init__(self, board, team, position):
        self.board = board
        self.team = team
        self.position = position
        self.type = BISHOP

        
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

    def is_valid_move(self, pos):
        query_row, query_col = pos
        my_row, my_col = self.position

        d_row = (query_row - my_row)
        d_col = (query_col - my_col)

        piece = self.board[pos]

        if abs(d_row) != abs(d_col):
            return False

        if not(d_row or d_col):
            return False

        if piece is not None and piece.team == self.team:
            return False

        vertical_direction = 1 if d_row > 0 else -1
        horizontal_direction = 1 if d_col > 0 else -1
        for i in xrange(1, abs(d_row)):
            row = vertical_direction*i
            col = horizontal_direction*i

            piece = self.board[(my_row+row, my_col+col)]
            if piece is not None:
                return False

        return True
        



