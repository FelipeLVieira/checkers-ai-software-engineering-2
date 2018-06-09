import pygame
import Board
from Constants import *
import random
import threading
import copy
import cProfile, pstats, io
from math import ceil

class mockBoard:
    def __init__(self, moveDivision):
        self.moveDivision = moveDivision
        self.selectedPos = None

    def getLegalMoves(self):
        if isinstance(self.moveDivision, list):
            return self.moveDivision
        return []

    def executeMove(self, move):
        self.moveDivision = move

def mockHeuristic(board, playerColor):
    return board.moveDivision



class rngWrapper:
    """Wrapper class to ensure the RNG is properly seeded, and only once."""
    def __init__(self):
        self.seeded = False

    def rand(self):
        if not self.seeded:
            random.seed()
            self.seeded = True
        return random.random()

# Global rngWrapper object for the minimax function
rng = rngWrapper()


def test_simple():
    tree = [
            [
                [2., 3.],
                [2.5]
            ],
            [
                [4.]
            ]
           ]
    board = mockBoard(tree)
    result = []
    minimaxAB(board, 8, RED, result, randomOffset=0, heuristicFunc=mockHeuristic)
    assert result[0] is tree[1]

def test_two():
    tree = [
            [
                [2., 3.],
                [
                    [4., 6.],
                    [1., -1.]
                ]
            ],
            [
                [4.],
                [
                    [-1.],
                    [
                        [10., 5.]
                    ]
                ]
            ]
           ]
    board = mockBoard(tree)
    result = []
    minimaxAB(board, 8, RED, result, randomOffset=0, heuristicFunc=mockHeuristic)
    assert result[0] is tree[0]



def contextColor(color, maximizing):
    '''Gives the minimax context color based on the AI's color.'''
    if maximizing: return color
    if color == RED: return WHITE
    if color == WHITE: return RED
    raise RuntimeError("Graphics.py::contextColor(): invalid color `{}'."
            .format(color))

def heuristic(board, playerColor, endGame):
    """Outputs a number that describes the state of the game.
       In other words, a number that correlates with how well the player
       indicated by playerColor is doing."""

    """Piece count will not be used for heuristic anymore.
    myPieces = 0
    opponentPieces = 0
    myKings = 0
    opponentKings = 0

    for col in range(8):
        for row in range(8):
            if board.matrix[col][row].occupant is not None:
                if board.matrix[col][row].occupant.color == playerColor:
                    if board.matrix[col][row].occupant.king:
                        myKings += 1
                    myPieces += 1
                else: 
                    if board.matrix[col][row].occupant.king:
                        opponentKings += 1
                    opponentPieces += 1
    """

    if endGame:
        if board.playerTurn == playerColor:
            return -100000000000.
        else: 
            return 100000000000.

    opponentColor = contextColor(playerColor, False)
    attenuation = 1.0

    heur = 2 * ((2 * board.kingCache[playerColor]) ** 2 - 
            1.1 * ((2 * board.kingCache[opponentColor]) ** 2))
    for e in board.captureCache[playerColor]:
        heur += 2.1 * (e ** 2) * attenuation
        attenuation *= 0.7
    attenuation = 1.0
    for e in board.captureCache[opponentColor]:
        heur -= 2.4 * (e ** 2) * attenuation
        attenuation *= 0.7
    attenuation = 1.0
    for e in board.kingCaptureCache[playerColor]:
        heur += 2.1 * ((2 * e) ** 2) * attenuation
        attenuation *= 0.7
    attenuation = 1.0
    for e in board.kingCaptureCache[opponentColor]:
        heur -= 2.4 * ((2 * e) ** 2) * attenuation
        attenuation *= 0.7

    return heur

    """
    return (1.2 * sum(map(lambda x: x ** 2, board.captureCache[playerColor])) - 
            0.8 * sum(map(lambda x: x ** 2, board.captureCache[opponentColor])) +
            board.kingCache[playerColor] * 1.2 -
            board.kingCache[opponentColor] * 0.8 +
            sum(map(lambda x: (2 * x) ** 2, board.kingCaptureCache[
                playerColor])) - 1.2 *
            sum(map(lambda x: (2 * x) ** 2, board.kingCaptureCache[
                opponentColor])))
    """

def minimaxAB(board, depth, AIColor, returnPointer, maximizing=True,
        alpha=float("-inf"), beta=float("+inf"), parentCall=True,
        stubbornnessTable=None, randomOffset=0.05, heuristicFunc=heuristic, 
        rng=rng, prof=None, treeCutFactor=2.):
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
    # Profiling code
    if parentCall:
        board = copy.deepcopy(board)
        board.clearMovementStats()
       
    # If we're at the limit of our tree, use the heuristic to guess
    if depth == 0:
        return heuristicFunc(board, AIColor, False)
    
    # Blind the AI randomly
    if (not parentCall
            and (isinstance(stubbornnessTable, list)
                    or isinstance(stubbornnessTable, tuple))):
        if rng.rand() < stubbornnessTable[depth]:
            return heuristicFunc(board, AIColor, False)
            
    # Get a list of all legal moves
    legalMoveSet = board.getAllLegalMoves()
    if len(legalMoveSet) == 0:
        return heuristicFunc(board, AIColor, True)

    nodeIndex = -1
    chosenNode = None
    chosenNodeHeuristic = None
    
    nodes = []
    # For all possible moves, execute them and grab the resulting heuristic
    # assessment.
    for move in legalMoveSet:
        childBoard = Board.Board(board)
        childBoard.executeMove(move, blind=True)
        if depth > 3:
            heuristic = minimaxAB(Board.Board(childBoard), 1, AIColor, None,
                        maximizing=not maximizing, alpha=alpha, beta=beta, 
                        parentCall=False, 
                        stubbornnessTable=stubbornnessTable, 
                        randomOffset=randomOffset,
                        heuristicFunc=heuristicFunc, prof=prof,
                        treeCutFactor=treeCutFactor)
        else: 
            heuristic = (heuristicFunc(childBoard, AIColor, False) 
                    + rng.rand() * randomOffset)
        childBoard.playerTurn = contextColor(AIColor, not maximizing)
        nodes.append((childBoard, heuristic))
    
    # Case 1: maximizing step
    if maximizing:
        bestValue = float("-inf")
        # Debug
        #values = []
        nodes = sorted(nodes, key=lambda x: x[1])
        for node in nodes:
            nodeIndex += 1
            # Cut the tree in half if an admissible heuristic has been found
            if (len(nodes) > 2 and nodeIndex >= ceil(len(nodes) / treeCutFactor)
                    and bestValue >= -0.2): break

            # This makes the AI randomly "not see" a move based on its
            # stubbornness. But only if it has seen at least one move on the
            # parent call.
            
            # Simulate move in an imaginary board
            childBoard = node[0]
            #print("AI.py::minimaxAB: d{}, recursing into {}".format(depth, move))
            #for l in board.boardToStrings():
            #    print(l)
            #print()

            # Recurse to the minimizing step.
            # randomOffset is used here to give the AI some unpredictability.
            # (and make it randomly choose between equally-valued moves)
            #print("AI.py::minimaxAB: d{}, recursing into {}".format(depth, move))
            childValue = (minimaxAB(childBoard, depth - 1, AIColor, None, 
                            maximizing=False, alpha=alpha, beta=beta, 
                            parentCall=False, 
                            stubbornnessTable=stubbornnessTable, 
                            randomOffset=randomOffset,
                            heuristicFunc=heuristicFunc, prof=prof,
                            treeCutFactor=treeCutFactor)
                    + rng.rand() * randomOffset)
            #print("AI.py::minimaxAB: d{}, got {} from {}".format(depth, childValue, move))

            #values.append(childValue)
            if ((childValue > bestValue - 0.15 and (chosenNodeHeuristic is None
                                    or node[1] > chosenNodeHeuristic))
                    or childValue > bestValue + 0.45):
                bestValue = childValue
                chosenNode = nodeIndex
                chosenNodeHeuristic = node[1]

            alpha = max(alpha, bestValue)

            # Prune the tree
            if beta + 0.49 <= alpha: 
                #print("AI.py::minimaxAB: (d{}) beta={}, alpha={}, pruning".format(depth, beta, alpha))
                break
        #print("AI.py::minimaxAB: (d{}) values={}, maximizing={}".format(depth, values, maximizing))
        if not parentCall: return bestValue
        print("AI.py::minimaxAB: (parent) Best value is {}".format(bestValue))


    # Case 2: minimizing step
    else:
        worstValue = float("+inf")
        # Debug
        #values = []
        nodes = sorted(nodes, key=lambda x: -x[1])
        for node in nodes:
            nodeIndex += 1
            # Cut the tree in half if an admissible heuristic has been found
            if (len(nodes) > 2 and nodeIndex >= ceil(len(nodes) / treeCutFactor) 
                    and worstValue <= 0.2): break

            # This makes the AI randomly "not see" a move based on its
            # stubbornness. But on the parent call, it only skips if it has
            # already seen at least one move.

            # Execute move in our imaginary board
            childBoard = node[0]
            # Recurse to the maximizing step.
            # randomOffset is used here to give the AI some unpredictability.
            # (and make it randomly choose between equally-valued moves)
            #print("AI.py::minimaxAB: d{}, recursing into {}".format(depth, move))
            childValue = (minimaxAB(childBoard, depth - 1, AIColor, None,
                                    maximizing=True, alpha=alpha, beta=beta, 
                            parentCall=False, 
                            stubbornnessTable=stubbornnessTable, 
                            randomOffset=randomOffset,
                            heuristicFunc=heuristicFunc, prof=prof,
                            treeCutFactor=treeCutFactor)
                    + rng.rand() * randomOffset)

            #values.append(childValue)
            if ((childValue < worstValue + 0.15 and (chosenNodeHeuristic is None
                                    or node[1] < chosenNodeHeuristic))
                    or childValue < worstValue - 0.45):
                worstValue = childValue
                chosenNode = nodeIndex
                chosenNodeHeuristic = node[1]

            beta = min(beta, worstValue)

            # Prune the tree
            if beta + 0.49 <= alpha: 
                #print("AI.py::minimaxAB: (d{}) beta={}, alpha={}, pruning".format(depth, beta, alpha))
                break
        #print("AI.py::minimaxAB: (d{}) values={}, maximizing={}".format(depth, values, maximizing))
        if not parentCall: return worstValue
    returnPointer.append(legalMoveSet[chosenNode])


minimaxHyperParameters = [
        {"heuristicFunc": heuristic, "depth": 2, "stubbornnessTable": [0, 0.4, 0],
            "randomOffset": 0.1, "treeCutFactor": 1.},
        {"heuristicFunc": heuristic, "depth": 3, "stubbornnessTable": None,
            "randomOffset": 0.05, "treeCutFactor": 1.},
        {"heuristicFunc": heuristic, "depth": 4,
            "stubbornnessTable": None,
            "randomOffset": 0.02, "treeCutFactor": 1},
        ]

class AIPlayer:
    # The Board object the AI is playing in.
    board = None

    # The minimum time in seconds to delay when the AI is
    # going to play.
    # This avoids it from playing too quickly on fast computers.
    waitTime = None

    # The counter for waitTime.
    waitTimer = None
    
    # The AI color; usually RED, but who knows.
    color = None

    # The pointer to the minimax thread that's initiated when the AI is going
    # to play.
    minimaxThread = None

    # Result of the minimaxThread
    minimaxResult = None

    # +--- Difficulty parameters: ---+
    # Heuristic function:
    heuristicFunc = None

    # Search depth:
    depth = None

    # Stubbornness:
    stubbornnessTable = None

    # Random judgement offset:
    randomOffset = None

    # +------------------------------+
    
    def __init__(self, board, color=RED, difficulty=2, waitTime=1.0):
        self.board = board
        self.color = color
        self.waitTime = waitTime
        self.waitTimer = 0.
        self.heuristicFunc = minimaxHyperParameters[difficulty]\
                ["heuristicFunc"]
        self.depth = minimaxHyperParameters[difficulty]\
                ["depth"]
        self.stubbornnessTable = minimaxHyperParameters[difficulty]\
                ["stubbornnessTable"]
        self.randomOffset = minimaxHyperParameters[difficulty]\
                ["randomOffset"]
        self.treeCutFactor = minimaxHyperParameters[difficulty]\
                ["treeCutFactor"]

        self.minimaxThread = None
        self.minimaxResult = []


    def isThinking(self):
        return (self.minimaxThread is not None and
                self.minimaxThread.is_alive())


    def play(self):
        if self.isThinking():
            raise RuntimeError("AI.py::AIPlayer:play(): An attempt to call the AI function was made while it is already running.")
        self.waitTimer = self.waitTime
        self.minimaxResult = []
        self.minimaxThread = threading.Thread(
                target=minimaxAB, args=(self.board, self.depth, self.color, 
                        self.minimaxResult),
                kwargs={"heuristicFunc": self.heuristicFunc,
                        "stubbornnessTable": self.stubbornnessTable,
                        "randomOffset": self.randomOffset,
                        "treeCutFactor": self.treeCutFactor})
        self.minimaxThread.start()
    

    def updateAndCheckCompletion(self, timeDelta):
        self.waitTimer -= timeDelta
        if not (self.waitTimer > 0 or self.isThinking()):
            print("AI.py::AIPlayer.updateAndCheckCompletion: waitTimer={}, minimaxThread={}, isAlive={}, minimaxResult={}, returning".format(self.waitTimer, self.minimaxThread, self.minimaxThread.is_alive(), self.minimaxResult))
            return self.minimaxResult[0]
        return False



