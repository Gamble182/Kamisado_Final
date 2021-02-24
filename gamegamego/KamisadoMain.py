import pygame as p
from Kamisado_Final.gamegamego import KamisadoEngine

'''
The main driver four our code. This will handle user input and updating the graphics
'''

WIDTH = 512
HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main 
'''


def loadImages():
    pieces = ["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "w1", "w2", "w3", "w4", "w5", "w6", "w7", "w8", ]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


'''
The main driver for our code. This will handle user input and updating the graphics
'''


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("black"))
    gs = KamisadoEngine.GameState()
    validMoves = gs.getValidMoves(0, [0])
    moveMade = False  # flag variable for when a move is made
    loadImages()
    running = True
    sqSelected = ()  # no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = []  # keep track of player clicks (two tuples: [(6, 4), (4,4)])
    running = True
    gameOver = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()  # (x,y) location of mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col):  # the user clicked the same square twice
                        sqSelected = (row, col)
                        playerClicks = []  # clear player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # append for both 1st and 2nd clicks
                    if len(playerClicks) == 2:  # after 2nd click
                        move = KamisadoEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        if move in validMoves:
                            moveMade = True
                            gs.makeMove(move)
                            sqSelected = ()  # reset user clicks
                            playerClicks = []  #
                        else:
                            playerClicks = [sqSelected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                if e.key == p.K_r:  # reset the board when 'r' is pressed
                    gs = KamisadoEngine.GameState()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
        if moveMade:
            # animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves(move.getRows(), gs.board)
            moveMade = False

        drawGameState(screen, gs, validMoves, sqSelected)
        if gs.gameIsWon:
            gameOver = True
            if gs.blackToMove:
                drawText(screen, "White wins!")
            else:
                drawText(screen, 'Black wins!')

        clock.tick(MAX_FPS)
        p.display.flip()


'''Highlight square selected and moves for piece selected'''

def highlightSquare(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('b' if gs.blackToMove else 'w'):  # sqSelected is a piece that chan be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transperancy value -> 0 transparent; 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


'''
Responsible for all the graphics within ta curent game state
'''

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)  # draw squares on the board
    highlightSquare(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

'''
Draw the suwares on the board.
'''

def drawBoard(screen):
    intDimension = int(DIMENSION)

    colors = {
        "orange": p.Color("#FF6A00"),
        "blue": p.Color("#0026FF"),
        "purple": p.Color("#9300FF"),
        "pink": p.Color("#FF00DC"),
        "yellow": p.Color("#FFE400"),
        "red": p.Color("#FF0000"),
        "green": p.Color("#4CB200"),
        "brown": p.Color("#7F3300")
    }

    # Oragne Field
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            if row == column:  # spalte , zeile
                p.draw.rect(screen, colors["orange"], p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # blue field
    p.draw.rect(screen, colors["blue"], p.Rect((2 - 1) * SQ_SIZE, (1 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["blue"], p.Rect((5 - 1) * SQ_SIZE, (2 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["blue"], p.Rect((8 - 1) * SQ_SIZE, (3 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["blue"], p.Rect((3 - 1) * SQ_SIZE, (4 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["blue"], p.Rect((6 - 1) * SQ_SIZE, (5 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["blue"], p.Rect((1 - 1) * SQ_SIZE, (6 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["blue"], p.Rect((4 - 1) * SQ_SIZE, (7 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["blue"], p.Rect((7 - 1) * SQ_SIZE, (8 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # purple field
    p.draw.rect(screen, colors["purple"], p.Rect((3 - 1) * SQ_SIZE, (1 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["purple"], p.Rect((8 - 1) * SQ_SIZE, (2 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["purple"], p.Rect((5 - 1) * SQ_SIZE, (3 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["purple"], p.Rect((2 - 1) * SQ_SIZE, (4 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["purple"], p.Rect((7 - 1) * SQ_SIZE, (5 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["purple"], p.Rect((4 - 1) * SQ_SIZE, (6 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["purple"], p.Rect((1 - 1) * SQ_SIZE, (7 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["purple"], p.Rect((6 - 1) * SQ_SIZE, (8 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # pink field
    pinkCount = 3
    pinkCount2 = 7
    for row in range(intDimension // 2):
        for column in range(1):
            p.draw.rect(screen, colors["pink"], p.Rect(pinkCount * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            pinkCount -= 1

    for row in range(intDimension // 2, intDimension):
        for column in range(1):
            p.draw.rect(screen, colors["pink"], p.Rect(pinkCount2 * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            pinkCount2 -= 1

    # yellow field
    yellowCount = 4
    yellowCount2 = 0
    for row in range(intDimension // 2):
        for column in range(1):
            p.draw.rect(screen, colors["yellow"], p.Rect(yellowCount * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            yellowCount += 1

    for row in range(intDimension // 2, intDimension):
        for column in range(1):
            p.draw.rect(screen, colors["yellow"], p.Rect(yellowCount2 * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            yellowCount2 += 1

    # red field
    p.draw.rect(screen, colors["red"], p.Rect((6 - 1) * SQ_SIZE, (1 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["red"], p.Rect((1 - 1) * SQ_SIZE, (2 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["red"], p.Rect((4 - 1) * SQ_SIZE, (3 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["red"], p.Rect((7 - 1) * SQ_SIZE, (4 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["red"], p.Rect((2 - 1) * SQ_SIZE, (5 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["red"], p.Rect((5 - 1) * SQ_SIZE, (6 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["red"], p.Rect((8 - 1) * SQ_SIZE, (7 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["red"], p.Rect((3 - 1) * SQ_SIZE, (8 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # green field
    p.draw.rect(screen, colors["green"], p.Rect((7 - 1) * SQ_SIZE, (1 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["green"], p.Rect((4 - 1) * SQ_SIZE, (2 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["green"], p.Rect((1 - 1) * SQ_SIZE, (3 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["green"], p.Rect((6 - 1) * SQ_SIZE, (4 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["green"], p.Rect((3 - 1) * SQ_SIZE, (5 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["green"], p.Rect((8 - 1) * SQ_SIZE, (6 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["green"], p.Rect((5 - 1) * SQ_SIZE, (7 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colors["green"], p.Rect((2 - 1) * SQ_SIZE, (8 - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # brwon field
    brownCount = 7
    for row in range(DIMENSION):
        for column in range(1):
            p.draw.rect(screen, colors["brown"], p.Rect(brownCount * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            brownCount -= 1


'''
Draw the pieces on the board using the current Gamestate.board
'''


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''Animating a move'''

'''def animateMove(move, screen, board, clock):
    global colors
    coords = []  # list of coords that the animation will move through
    dR = move.endRow - move.startRow
    dC = move.endCol = move.startCol
    framesPerSquare = 10  # frames to move on square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect[(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)]
        p.draw.rect(screen, color, endSquare)
        # draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
'''


def drawText(screen, text):
    font = p.font.SysFont("Arial", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2,
                                                    HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))


if __name__ == "__main__":
    main()
