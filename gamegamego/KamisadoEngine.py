"""
This class is respnsible for starting all the information about the current state of a chess game. It will also be
responsible for determining the valid moves at the current state. It will also keep a move log.
"""


class GameState():
    def __init__(self):

        self.board = [
            ["w1", "w2", "w3", "w4", "w5", "w6", "w7", "w8"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["b8", "b7", "b6", "b5", "b4", "b3", "b2", "b1"]
        ]

        self.boardColorValues = [
            [1, 2, 3, 4, 5, 6, 7, 8],
            [6, 1, 4, 7, 2, 5, 8, 3],
            [7, 4, 1, 6, 3, 8, 5, 2],
            [4, 3, 2, 1, 8, 7, 6, 5],
            [5, 6, 7, 8, 1, 2, 3, 4],
            [2, 5, 8, 3, 6, 1, 4, 7],
            [3, 8, 5, 2, 7, 4, 1, 6],
            [8, 7, 6, 5, 4, 3, 2, 1]
        ]

        self.__directionsBlack = ((-1, 0), (-1, -1), (-1, 1))
        self.__directionsWhite = ((1, 0), (1, 1), (1, -1))

        self.blackToMove = True
        self.moveLog = []
        self.gameIsWon = False
        self.fieldColor = 0

    '''Takes a Move as a prameter and executes it.'''

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo it later
        self.blackToMove = not self.blackToMove  # swap players
        self.isWin(move.endRow, move.endCol)

    '''Undo the last move made'''

    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.blackToMove = not self.blackToMove  # switch turns back

    '''All moves considering checks'''

    def getValidMoves(self, endSq, board):
        if endSq == 0:
            pass
        else:
            row = endSq[0]
            column = endSq[1]
            self.fieldColor = board[row][column]
            for i in range(len(self.board)):
                print(self.board[i])
            print(" ")
        return self.getAllPossibleMoves()  #

    '''All moves without considering checks'''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board)):  # number of columns
                turn = self.board[r][c][0]
                if (turn == 'b' and self.blackToMove) or (turn == 'w' and not self.blackToMove):
                    piece = self.board[r][c][1]
                    if self.fieldColor == 0:
                        self.getTowerMoves(r, c, moves)
                    elif self.fieldColor == 1 and piece == '1':
                        self.getTowerMoves(r, c, moves)
                    elif self.fieldColor == 2 and piece == '2':
                        self.getTowerMoves(r, c, moves)
                    elif self.fieldColor == 3 and piece == '3':
                        self.getTowerMoves(r, c, moves)
                    elif self.fieldColor == 4 and piece == '4':
                        self.getTowerMoves(r, c, moves)
                    elif self.fieldColor == 5 and piece == '5':
                        self.getTowerMoves(r, c, moves)
                    elif self.fieldColor == 6 and piece == '6':
                        self.getTowerMoves(r, c, moves)
                    elif self.fieldColor == 7 and piece == '7':
                        self.getTowerMoves(r, c, moves)
                    elif self.fieldColor == 8 and piece == '8':
                        self.getTowerMoves(r, c, moves)

        return moves

    '''Get all the tower moves for the tower located at row, col and add these moves to the list'''

    def getTowerMoves(self, r, c, moves):
        # spalte zeile
        if self.blackToMove:  # black player move
            for d in self.__directionsBlack:
                for i in range(1, 8):
                    endRow = r + d[0] * i
                    endCol = c + d[1] * i
                    if 0 <= endRow < 8 and 0 <= endCol < 8:
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] != "--":  # not an allypiece (empty or enemypiece )
                            break
                        else:  # friendly piece invalid
                            break
                    else:  # off board
                        break
        else:
            for d in self.__directionsWhite:
                for i in range(1, 8):
                    endRow = r + d[0] * i
                    endCol = c + d[1] * i
                    if 0 <= endRow < 8 and 0 <= endCol < 8:
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))

                        elif endPiece[0] != "--":  # not an allypiece (empty or enemypiece )
                            break
                        else:  # friendly piece invalid
                            break
                    else:  # off board
                        break

    def isWin(self, r, c):
        if self.blackToMove:
            for i in range(8):
                if self.board[7][i] == self.board[r][c]:
                    self.gameIsWon = True
        else:
            for i in range(8):
                if self.board[0][i] == self.board[r][c]:
                    self.gameIsWon = True


class Move():
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''Overriding the equals method'''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getRows(self):
        return (self.endRow, self.endCol)
