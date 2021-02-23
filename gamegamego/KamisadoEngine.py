"""
This class is respnsible for starting all the information about the current state of a chess game. It will also be
responsible for determining the valid moves at the current state. It will also keep a move log.
"""


class GameState():
    def __init__(self):
        self.board = [
            ["wR", "wR", "wR", "wR", "wR", "wR", "wR", "wR"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["bR", "bR", "bR", "bR", "bR", "bR", "bR", "bR"]
        ]
        self.boardColors = {
            1: "orange",
            2: "blue",
            3: "purple",
            4: "pink",
            5: "yellow",
            6: "red",
            7: "green",
            8: "brown"
        }

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
        self.moveFunctions = {'R': self.getTowerMoves}
        self.blackToMove = True
        self.moveLog = []
        self.gameIsWon = False
        # self.whiteKingLocation == (0,0)
        # self.blackKingLocation == (7,7)

    '''Takes a Move as a prameter and executes it (this will not work for castling, pawn promotin, and en-passant'''

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo it later
        self.blackToMove = not self.blackToMove  # swap players
        self.isWin(move.endRow, move.endCol)
        '''if move.pieceMoved == 'wR':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'wR':
            self.blackKingLocation = (move.endRow, move.endCol)'''

    '''Undo the last move made'''

    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.blackToMove = not self.blackToMove  # switch turns back

    '''All moves considering checks'''

    def getValidMoves(self):
        return self.getAllPossibleMoves()  # for now we will not worry about checks

    '''All moves without considering checks'''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board)):  # number of columns
                turn = self.board[r][c][0]
                if (turn == 'b' and self.blackToMove) or (turn == 'w' and not self.blackToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  #
        return moves



    '''Get all the rook moves for the pawn located at row, col and add these moves to the list'''

    def getTowerMoves(self, r, c, moves):
        # spalte zeile
        __directionsBlack = ((-1, 0), (-1, -1), (-1, 1))
        __directionsWhite = ((1, 0), (1, 1), (1, -1))
        if self.blackToMove:  # white pawn moves
            for d in __directionsBlack:
                for i in range(1, 8):
                    endRow = r + d[0] * i
                    endCol = c + d[1] * i
                    if 0 <= endRow < 8 and 0 <= endCol < 8:
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] != "--":  # not an allypiece (empty or enemypiece )
                            break
                        else:  # friendl piece invalid
                            break
                    else:  # off board
                        break
        else:
            for d in __directionsWhite:
                for i in range(1, 8):
                    endRow = r + d[0] * i
                    endCol = c + d[1] * i
                    if 0 <= endRow < 8 and 0 <= endCol < 8:
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] != "--":  # not an allypiece (empty or enemypiece )
                            break
                        else:  # friendl piece invalid
                            break
                    else:  # off board
                        break

    def isWin(self,r , c):
        if self.blackToMove:
            for i in range(8):
                if self.board[7][i] == self.board[r][c]:
                    self.gameIsWon = True
        else:
            for i in range(8):
                if self.board[0][i] == self.board[r][c]:
                    self.gameIsWon = True



class Move():
    # maps keys to values
    # key :value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

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

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
