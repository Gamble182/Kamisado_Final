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
        self.moveFunctions = {'R': self.getRookMoves}
        self.blackToMove = True
        self.moveLog = []
        self.checkmate = False
        # self.whiteKingLocation == (0,0)
        # self.blackKingLocation == (7,7)

    '''Takes a Move as a prameter and executes it (this will not work for castling, pawn promotin, and en-passant'''

    def makeMove(self, move):
        print("makeMove")
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo it later
        self.blackToMove = not self.blackToMove  # swap players
        '''if move.pieceMoved == 'wR':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'wR':
            self.blackKingLocation = (move.endRow, move.endCol)'''

    # def makeMove(self, move):

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

    '''Get all the pawn moves for the pawn located at row, col and add these moves to the list'''

    def getPawnMoves(self, r, c, moves):
        if self.blackToMove:  # white pawn moves
            if self.board[r - 1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == "b":  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # captures to the right
                if self.board[r - 1][c + 1][0] == "b":  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:  # black pawn moves
            if self.board[r + 1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2, c), self.board))
            # captures
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == "w":  # enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                if c + 1 <= 7:  # captures to the right
                    if self.board[r + 1][c + 1][0] == "w":  # enemy piece to capture
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))

    '''Get all the rook moves for the pawn located at row, col and add these moves to the list'''

    def getRookMoves(self, r, c, moves):
        # spalte zeile
        __directionsBlack = ((-1, 0), (-1, -1), (-1, 1))
        __directionsWhite = ((1, 0), (1, 1), (1, -1))
        if self.blackToMove:  # white pawn moves
            for d in __directionsBlack:
                for i in range(1, 8):
                    print("black to move")
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
                    print("white to move")
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

    '''Get all the Knight moves for the pawn located at row, col and add these moves to the list'''

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.blackToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an allypiece (empty or enemypiece )
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    '''Get all the bishop moves for the pawn located at row, col and add these moves to the list'''

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # up, left, down, right
        enemyColor = "b" if self.blackToMove else "w"
        for d in directions:
            for i in range(1, 8):
                print("ChessEngine schleife1")
                endRow = r + d[0] * i
                endCol = c + d[0] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    print("ChessEngine schleife2")
                    endPiece = self.board[endRow][endCol]  # empty space valid
                    if endPiece == "--":  # empty space valid
                        print("ChessEngine schleife3")
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        print("ChessEngine schleife4")
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        print("ChessEngine schleife5")
                        break
                else:  # off board
                    print("ChessEngine schleife6")
                    break


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
