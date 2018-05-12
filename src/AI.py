import pygame
import Board
from Constants import *

def minimax_ab(board, depth, AIColor, maximizing=True, alpha=float("-inf"), 
               beta=float("+inf")):
    # Get a list of all legal moves
    legalMoveSet = []
    for x in range(8):
        for y in range(8):
            if(board.matrix[x][y].occupant is Board.Piece
                    and board.matrix[x][y].occupant.color == AIColor):
                for move in board.legalMoves(AIColor, Coordinate(x, y)):
                    if move is not in legalMoveSet:
                        legalMoveSet.append(move)

    # If we're at the limit of our tree, use the heuristic to guess
    if depth == 0 or len(legalMoveSet) == 0:
        return heuristic(board)

    if maximizing:
        bestValue = float("-inf")
        for move in legalMoveSet:
            childBoard = Board.Board(board)
            executeMove(move, childBoard)
            # Recurse to the minimizing step
            bestValue = max(bestValue, minimax_ab(childBoard, depth - 1,
                    playerColor, maximizing=False, alpha, beta))
            alpha = max(alpha, bestValue)
            # Prune the tree
            if beta <= alpha: break
        return bestValue

    else:
        worstValue = float("+inf")
        for move in legalMoveSet:
            childBoard = Board.Board(board)
            executeMove(move, childBoard)
            # Recurse to the maximizing step
            worstValue = min(bestValue, minimax_ab(childBoard, depth - 1,
                    playerColor, maximizing=True, alpha, beta))
            beta = min(beta, worstValue)
            # Prune the tree
            if beta <= alpha: break
        return bestValue

def heuristic(board, playerColor):
    raise NotImplementedError()
