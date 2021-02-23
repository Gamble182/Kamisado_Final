'''
Author: Eric P. Nichols
Date: Feb 8, 2008.
Board class.
Board data:
  1=white, -1=black, 0=empty
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.
'''

def get_player(color):
    if color > 0:
        return 1
    elif color < 0:
        return -1
    else:
        return 0



class Board():
    # list of all 8 directions on the board, as (x,y) offsets
    # brauchen nur eine direction, da das board gespiegelt wird
    __directionsBlack = [(0, -1), (-1, -1), (1, -1)]

    __directionsWhite = [(0, 1), (1, 1), (-1, 1)]

    def __init__(self, n):
        "Set up initial board configuration."

        self.n = n
        # Create the empty board array.
        self.pieces = [None] * self.n
        for i in range(self.n):
            self.pieces[i] = [0] * self.n

        # Set up the initial white pieces
        self.pieces[int(self.n - 8)][int(self.n - 8)] = -1
        self.pieces[int(self.n - 8)][int(self.n - 7)] = -2
        self.pieces[int(self.n - 8)][int(self.n - 6)] = -3
        self.pieces[int(self.n - 8)][int(self.n - 5)] = -4
        self.pieces[int(self.n - 8)][int(self.n - 4)] = -5
        self.pieces[int(self.n - 8)][int(self.n - 3)] = -6
        self.pieces[int(self.n - 8)][int(self.n - 2)] = -7
        self.pieces[int(self.n - 8)][int(self.n - 1)] = -8
        # Set up the initial black pieces
        self.pieces[int(self.n - 1)][int(self.n - 8)] = 8
        self.pieces[int(self.n - 1)][int(self.n - 7)] = 7
        self.pieces[int(self.n - 1)][int(self.n - 6)] = 6
        self.pieces[int(self.n - 1)][int(self.n - 5)] = 5
        self.pieces[int(self.n - 1)][int(self.n - 4)] = 4
        self.pieces[int(self.n - 1)][int(self.n - 3)] = 3
        self.pieces[int(self.n - 1)][int(self.n - 2)] = 2
        self.pieces[int(self.n - 1)][int(self.n - 1)] = 1
        # add [][] indexer syntax to the Board

    def __getitem__(self, index):
        return self.pieces[index]

    def get_legal_moves(self, color):  # color des spielers wird erwartet (aktiver spieler)
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = set()  # stores the legal moves.

        # Get all the squares with pieces of the given color.
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == color:
                  #  piece = ColorBoard.Board[x][y]
                   # if piece == 1: # TODO get field-color of last move
                    newmoves = self.get_moves_for_square((x, y))
                    moves.update(newmoves)
        return list(moves)

    def has_legal_moves(self, color):
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == color:
                    newmoves = self.get_moves_for_square((x, y))
                    if len(newmoves) > 0:
                        return True
        return False

    def get_moves_for_square(self, square):
        """Returns all the legal moves that use the given square as a base.
        That is, if the given square is (3,4) and it contains a black piece,
        and (3,5) and (3,6) contain white pieces, and (3,7) is empty, one
        of the returned moves is (3,7) because everything from there to (3,4)
        is flipped.
        """
        (x, y) = square

        # determine the color of the piece.
        player = self[x][y]

            # search all possible directions.
        moves = []
        # search all possible directions.
        for d in self.__directionsBlack:
            for i in range(1, 8):
                endRow = x + d[0] * i
                endCol = y + d[1] * i
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.pieces[endRow][endCol]
                if endPiece == 0:
                    moves.append(endPiece)
                else:
                    break
        return moves

    def execute_move(self, move, color):
        """Perform the given move on the board;
        color gives the color pf the piece to play (1=white,-1=black)
        """

        # Much like move generation, start at the new piece's square and

        # Add the piece to the empty square.
        # print(move)
        pass


class ColorBoard():
    Board = [
        [1, 2, 3, 4, 5, 6, 7, 8],
        [6, 1, 4, 7, 2, 5, 8, 3],
        [7, 4, 1, 6, 3, 8, 5, 2],
        [4, 3, 2, 1, 8, 7, 6, 5],
        [5, 6, 7, 8, 1, 2, 3, 4],
        [2, 5, 8, 3, 6, 1, 4, 7],
        [3, 8, 5, 2, 7, 4, 1, 6],
        [8, 7, 6, 5, 4, 3, 2, 1]
    ]
