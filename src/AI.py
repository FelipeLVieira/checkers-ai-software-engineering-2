import pygame
import Board
from Constants import *
import random


class rngWrapper
    """Wrapper class to ensure the RNG is properly seeded, and only once."""
    def __init__(self):
        seeded = False

    def rand(self):
        if not seeded:
            random.seed()
            seeded = True
        return random.random()

# Global rngWrapper object for the minimax function
rng = rngWrapper()



def contextColor(color, maximizing):
    '''Gives the minimax context color based on the AI's color.'''
    if maximizing: return color
    if color == RED: return WHITE
    if color == WHITE: return RED
    raise RuntimeError("Graphics.py::contextColor(): invalid color `{}'."
            .format(color))

def minimaxAB(board, depth, AIColor, maximizing=True, alpha=float("-inf"), 
               beta=float("+inf"), parentCall=True, stubbornnessTable=None,
               randomOffset=0.05, heuristicFunc=heuristic):
    """Implements the minimax algorithm.
       The below variables are tuning knobs:
       - depth controls how far into the future the algorithm looks.
       - stubbornnessTable is a list containing the probability of the AI
       skipping a move for each value of `depth'.
       - randomOffset is the magnitude of a small random offset applied to the
       computed moves' values, to make the AI unpredictable.
       - heuristicFun is a pointer to the heuristic function. It takes a Board
       object and the AI's color, and returns a value expressing the state of
       the game; a higher value means the AI is in a better position."""
    global rng
    # Get a list of all legal moves
    legalMoveSet = []
    for x in range(8):
        for y in range(8):
            if(board.matrix[x][y].occupant is Board.Piece
                    and board.matrix[x][y].occupant.color == 
                    contextColor(AIColor)):
                for move in board.legalMoves(contextColor(AIColor),
                        Coordinate(x, y)):
                    if move is not in legalMoveSet:
                        legalMoveSet.append(move)

    # If we're at the limit of our tree, use the heuristic to guess
    if depth == 0 or len(legalMoveSet) == 0:
        return heuristic(board, AIColor)

    nodeIndex = -1
    chosenNode = None
    
    # Case 1: maximizing step
    if maximizing:
        bestValue = float("-inf")
        for move in legalMoveSet:
            nodeIndex += 1

            # This makes the AI randomly "not see" a move based on its
            # stubbornness. But only if it has seen at least one move on the
            # parent call.
            if (not (parentCall and not bestvalue > float("-inf"))
                    and (stubbornnessTable is list
                        or stubbornnessTable is tuple)
                    and depth < len(stubbornnessTable)):
                if rng.rand() < stubbornnessTable[depth]: continue
            
            # Simulate move in an imaginary board
            childBoard = Board.Board(board)
            executeMove(move, childBoard)

            # Recurse to the minimizing step.
            # randomOffset is used here to give the AI some unpredictability.
            # (and make it randomly choose between equally-valued moves)
            childValue = minimaxAB(childBoard, depth - 1, AIColor, False, alpha,
                            beta, false, stubbornnessTable, randomOffset,
                            heuristicFunc)
                    + rng.rand() * randomOffset)

            if childValue > bestValue:
                bestValue = childValue
                chosenNode = nodeIndex

            alpha = max(alpha, bestValue)

            # Prune the tree
            if beta <= alpha: break
        if not parentCall: return bestValue


    # Case 2: minimizing step
    else:
        worstValue = float("+inf")
        for move in legalMoveSet:
            nodeIndex += 1

            # This makes the AI randomly "not see" a move based on its
            # stubbornness. But on the parent call, it only skips if it has
            # already seen at least one move.
            if (not (parentCall and not worstValue < float("+inf"))
                    and (stubbornnessTable is list
                        or stubbornnessTable is tuple)
                    and depth < len(stubbornnessTable)):
                if rng.rand() < stubbornnessTable[depth]: continue

            # Execute move in our imaginary board
            childBoard = Board.Board(board)
            executeMove(move, childBoard)

            # Recurse to the maximizing step.
            # randomOffset is used here to give the AI some unpredictability.
            # (and make it randomly choose between equally-valued moves)
            childValue = minimaxAB(childBoard, depth - 1, AIColor, True, alpha,
                            beta, False, stubbornnessTable, randomOffset,
                            heuristicFunc)
                    + rng.rand() * randomOffset)

            if childValue < worstValue:
                worstValue = childValue
                chosenNode = nodeIndex

            beta = min(beta, worstValue)

            # Prune the tree
            if beta <= alpha: break
        if not parentCall: return worstValue

    return legalMoveSet(chosenNode)


def heuristic(board, playerColor):
    raise NotImplementedError()
