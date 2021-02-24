import random

'''Picks and returns a random move'''


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


'''Find the best move based on material alone.'''


def findBestMove():
    return
