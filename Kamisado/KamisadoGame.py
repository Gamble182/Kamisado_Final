from __future__ import print_function
import sys

sys.path.append('../..')
from Game import Game
from .KamisadoLogic import Board
import numpy as np

"""
This class specifies the base Game class. To define your own game, subclass
this class and implement the functions below. This works when the game is
two-player, adversarial and turn-based.

Use 1 for player1 and -1 for player2.

See othello/OthelloGame.py for an example implementation.
"""

# black= 1 white= -1
class KamisadoGame():

    square_content_pieces = {
        -1: "w1",
        -2: "w2",
        -3: "w3",
        -4: "w4",
        -5: "w5",
        -6: "w6",
        -7: "w7",
        -8: "w8",
        +0: "--",
        +1: "b1",
        +2: "b2",
        +3: "b3",
        +4: "b4",
        +5: "b5",
        +6: "b6",
        +7: "b7",
        +8: "b8"
    }

    @staticmethod
    def getSquarePiece(piece):
        return KamisadoGame.square_content_pieces[piece]

    def __init__(self, n):
        self.n = n

    def getInitBoard(self):
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        return (self.n, self.n)

    # 8 * 3 * 8 + 1 Anzahl der möglichen Züge
    def getActionSize(self):
        return self.n * 3 * self.n + 1

    def getNextState(self, board, player, action):
        if action == self.n* self.n:
            return (board, -player)
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = (int(action / self.n), action % self.n)
        b.execute_move(move, player)
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        valids = [0] * self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves = b.get_legal_moves(player)
        if len(legalMoves) == 0:
            valids[-1] = 1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n * x + y] = 1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = np.copy(board)
        if b.has_legal_moves(player):
            return 0
        if b.has_legal_moves(-player):
            return 0
        return 0 # TODO return 1 / -1 if won

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        pass

    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        pass

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        pass

    @staticmethod
    def display(board):
        n = board.shape[0]
        print("   ", end="")
        for y in range(n):
            print(y, end=" ")
        print("")
        print("-----------------------")
        for y in range(n):
            print(y, "|", end="")  # row
            for x in range(n):
                piece = board[y][x]  # piece
                print(KamisadoGame.square_content_pieces[piece], end=" ")
            print("|")

        print("-----------------------")
