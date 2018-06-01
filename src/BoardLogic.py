import pygame
import copy
from Constants import *

class Board:
    
    def __init__(self, board=None):
        
        # Load the board matrix
        if isinstance(board, Board):
            self.matrix = copy.deepcopy(board.matrix)
        elif isinstance(board, list):
            self.matrix = self.boardFromStrings(board)
        else: self.matrix = self.newBoard()
        
        # Indicates which player is currently playing.
        self.playerTurn = WHITE
        
        # Cache of list of legal moves for the board in this turn;
        # Must be set to None at the end of a turn.
        self.legalMoveSet = None
    
    def newBoard(self):
        """Creates a matrix containing a new board."""
        matrix = []
        for x in range(8):
            row = []
            for y in range(8):
                square = Square((x & 1) ^ (y & 1))
                if y < 3 and square.black: square.occp = Piece(RED, False)
                elif y > 4 and square.black: square.occp = Piece(WHITE, False)
                row.append(square)
            matrix.append(row)
        return matrix
    
    """---------------------------------------------+
    |               TESTING FUNCTIONS               |
    +---------------------------------------------"""
    
    def boardFromStrings(self, boardDescription):
        """
        Takes a board string description and returns a matrix containing the 
        corresponding board pieces. Used for unit tests.
        """
        boardMatrix = []
        for x in range(8):
            col = []
            for y in range(8):
                col.append(Square(False))
            boardMatrix.append(col)
        
        parseDict = {
                "w": (WHITE, False),
                "W": (WHITE, True),
                "r": (RED,   False),
                "R": (RED,   True)
                }
        
        for x in range(8):
            for y in range(8):
                if (x & 1) ^ (y & 1):
                    boardMatrix[x][y].black = True
                    if boardDescription[y][x] in parseDict.keys():
                        boardMatrix[x][y].occp = (
                                Piece(parseDict[boardDescription[y][x]][0],
                                        parseDict[boardDescription[y][x]][1]))
        
        return boardMatrix
    
    """--------------------------------------------------------------------"""
    
    def boardToStrings(self):
        """
        Takes a board and returns a matrix of the board space colors.
        Used for unit tests.
        """

        boardString = []
        
        for y in range(0, 8):
            row = []
            for x in range(0, 8):
                if self.matrix[x][y].black:
                    if self.matrix[x][y].occp is None:
                        row.append(" ")
                    elif (self.matrix[x][y].occp.color is WHITE and
                            self.matrix[x][y].occp.king):
                        row.append("W")
                    elif (self.matrix[x][y].occp.color is RED and
                            self.matrix[x][y].occp.king):
                        row.append("R")
                    elif self.matrix[x][y].occp.color is WHITE:
                        row.append("w")
                    elif self.matrix[x][y].occp.color is RED:
                        row.append("r")
                else:
                    row.append("#")
            boardString.append(''.join(row))

        return boardString

    """-------------------------------------------------+
    |         MAIN MOVEMENT EVALUATION FUNCTIONS        |
    +-------------------------------------------------"""

    def getLegalMoves(self, coordinate):
        """Returns the legal moves for a piece."""
        # Calculate legal move set if it hasn't been calculated yet
        if self.legalMoveSet is None: self.getAllLegalMoves()

        # Select in the legal move set, where the first coordinate is the
        # desired piece's coordinate
        return list(filter(lambda m: m[0] == coordinate, self.legalMoveSet))

    """--------------------------------------------------------------------"""

    def getAllLegalMoves(self):
        """Computes legal moves for all of the player's pieces on the 
        board."""
        self.legalMoveSet = []
        # The highest move rank encountered.
        # The rank of a move is given by the number of captures it makes.
        highestMoveRank = -1
        
        # Go through the matrix and get the theoretical legal moves for each
        # piece.
        for x in range(8):
            for y in range(8):
                if (self.matrix[x][y].occp is not None 
                        and self.matrix[x][y].occp.color is self.playerTurn):
                    #print((x, y))
                    for move in self.theoreticalLegalMoves((x, y)):
                        if move not in self.legalMoveSet:
                            self.legalMoveSet.append(move)
                            
                            rank = self.moveRank(move)
                            if highestMoveRank < rank: highestMoveRank = rank
        
        # Filter out moves that aren't the highest rank, to enforce the
        # longest captures
        
        #print("BoardLogic.py::Board:getAllLegalMoves: Unfiltered legal moves:")
        #for move in self.legalMoveSet: print(move)
        
        #print("BoardLogic.py::Board:getAllLegalMoves: Highest move rank is {}".format(highestMoveRank))
        
        illegalMoves = []
        for move in self.legalMoveSet:
            if self.moveRank(move) < highestMoveRank:
                #print("BoardLogic.py::Board:getAllLegalMoves: Move {} has rank {} < {}, dropping.".format(move, self.moveRank(move), highestMoveRank))
                illegalMoves.append(move)
        
        for move in illegalMoves: self.legalMoveSet.remove(move)
        
        # For debugging only... comment this later
        #print("BoardLogic.py::Board:getAllLegalMoves: Legal moves:")
        #for move in self.legalMoveSet: print(move)
        
        return self.legalMoveSet
    
    """-----------------------------------------+
    |  AUXILIARY MOVEMENT EVALUATION FUNCTIONS  |
    +-----------------------------------------"""
    
    def moveRank(self, move):
        """Calculates the rank for a move.
        A move's rank is given by its number of captured pieces."""
        rank = 0
        start = derefer(self.matrix, move[0]).occp
        for coord in move:
            # If there's a piece in that coordinate
            square = derefer(self.matrix, coord).occp
            #print(coord, square)
            if square and square.color is not start.color:
                #print(square.color, start.color)
                rank += 1
        return rank
    
    """--------------------------------------------------------------------"""
    
    def theoreticalLegalMoves(self, pieceCoords):
        """Returns the possible moves for a piece if there were no
        higher-ranked moves possible."""
        # Dereference the coordinates to get the square object
        square = derefer(self.matrix, pieceCoords)
        
        if square.occp.king:
            return self.theoreticalKingLegalMoves(pieceCoords)
        moveList = []
        
        deltaDict = {WHITE: [(-1, -1), (1, -1)], RED: [(-1, 1), (1, 1)]}
        allDeltas = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        
        for delta in allDeltas:
            #print("BoardLogic.py::Board:theoreticalLegalMoves: Evaluating delta {}".format(delta))
            deltaCoord = tplsum(pieceCoords, delta)
            # Verify that the value is in bounds
            if not bounded(deltaCoord, 0, 7): continue
            
            deltaSquare = derefer(self.matrix, deltaCoord)
            # Check if the delta square is occupied
            if deltaSquare.occp:
                # If the piece in the delta square is the same color,
                # the move is impossible.
                if deltaSquare.occp.color is square.occp.color: continue
                
                # Otherwise, it's possibly a capture move. Deal with it.
                for move in self.possibleCaptures(square.occp.color, 
                        pieceCoords, delta, pieceCoords):
                    moveList.append(move)
                    #print("Evaluated capture move {} for delta {}.".format(move, delta))
            
            elif delta in deltaDict[square.occp.color]:
                # Given the square is free and is in "front" of the piece,
                # it's a valid movement.
                moveList.append([pieceCoords, deltaCoord])
        #print("Theoretical legal moves for {}:".format(pieceCoords))
        #for move in moveList: print(move)
        return moveList
    
    """--------------------------------------------------------------------"""
    
    def theoreticalKingLegalMoves(self, pieceCoords):
        """Returns the possible moves for a king if there were no
        higher-ranked moves possible."""
        # Dereference the coordinates to get the square object
        square = derefer(self.matrix, pieceCoords)
        moveList = []
        
        deltas = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for delta in deltas:
            newPieceCoords = pieceCoords
            deltaCoord = tplsum(pieceCoords, delta)
            # Check all possible chain positions in bounds
            currentMove = [pieceCoords]
            while bounded(deltaCoord, 0, 7):
                deltaSquare = derefer(self.matrix, deltaCoord)
                # Check if the delta square is occupied
                if deltaSquare.occp is not None:
                    # If the piece in the delta square is the same color,
                    # the move is impossible. Break the chain.
                    if deltaSquare.occp.color is square.occp.color: break
                    
                    # Otherwise, it's possibly a capture move. Deal with it.
                    for move in self.possibleCaptures(square.occp.color, 
                            newPieceCoords, delta, pieceCoords):
                        fullMove = copy.deepcopy(currentMove)[:-1]
                        fullMove.extend(move)
                        moveList.append(fullMove)
                    # A capture move ends the chain.
                    break
                else:
                    # It's a valid movement.
                    currentMove.append(deltaCoord)
                    currentMoveCopy = copy.deepcopy(currentMove)
                    moveList.append(currentMoveCopy)
                newPieceCoords = deltaCoord
                deltaCoord = tplsum(deltaCoord, delta)
        
        #print("Theoretical legal moves for {}:".format(pieceCoords))
        #for move in moveList: print(move)
        return moveList
    
    """--------------------------------------------------------------------"""
    
    def possibleCaptures(self, pieceColor, pieceCoords, delta, startPosition, 
            capturedPieces=None):
        """Recursively evaluates a capture and searches for capture chains."""
        deltaCoord = tplsum(pieceCoords, delta)
        landingCoord = tplsum(deltaCoord, delta)
        #print("BoardLogic.py::Board:possibleCaptures: New call at {} ({} -> {} - > {} with capturedPieces = {})".format(pieceCoords, pieceCoords, deltaCoord, landingCoord, capturedPieces))
        
        # Check if the delta and landing squares are in bounds
        if not bounded(deltaCoord, 0, 7) or not bounded(landingCoord, 0, 7):
            return []
        
        deltaSquare = derefer(self.matrix, deltaCoord)
        landingSquare = derefer(self.matrix, landingCoord)
        
        # Check if there is a piece that can be captured
        if ((not deltaSquare.occp) or
                (deltaSquare.occp.color is pieceColor)): return []
        
        # Check whether the landing square is clear
        if landingSquare.occp and landingCoord != startPosition: 
            #print("BoardLogic.py::Board:possibleCaptures: Landing square is not clear", landingCoord, startPosition)
            return []

        if capturedPieces is None: capturedPieces = []
        
        # Check whether the piece hasn't already been captured before
        if deltaCoord in capturedPieces: return []
        
        captureList = []
        captureList.append([pieceCoords, deltaCoord, landingCoord])
        
        # Flag the delta square as captured
        capturedPieces.append(deltaCoord)
        
        deltas = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        # Recurse into every possible delta
        for newdelta in deltas:
            for extraMove in self.possibleCaptures(pieceColor, landingCoord, 
                    newdelta, startPosition, copy.deepcopy(capturedPieces)):
                #print(extraMove)
                baseMove = [pieceCoords, deltaCoord]
                baseMove.extend(extraMove)
                #print("BoardLogic.py::Board:possibleCaptures: recursing into {} ({} -> {}) got {}".format(delta, landingCoord, tplsum(landingCoord, delta), baseMove))
                captureList.append(baseMove)
        
        return captureList

    """--------------------------------------------------------------------"""

"""----------------------------------------------------+
|      AUXILIARY STRUCTURE MANIPULATION FUNCTIONS      |
+----------------------------------------------------"""


def bounded(tpl, minm, maxm):
    """Checks if the values in a tuple are within given bounds."""
    bound = list(map(lambda val: val >= minm and val <= maxm, tpl))
    return bound[0] and bound[1]


def tplsum(t1, t2):
    """Returns the sum of two tuples."""
    return tuple(map(lambda x, y: x + y, t1, t2))

def derefer(matrix, coords):
    """Dereferences into a matrix using a tuple or list as coordinates."""
    ref = matrix
    for c in coords:
        ref = ref[c]
    return ref


"""-----------------------------------+
|      AUXILIARY DATA STRUCTURES      |
+-----------------------------------"""

class Square:
    
    def __init__(self, black, occp=None):
        self.black = bool(black)
        self.occp = occp

class Piece:
    def __init__(self, color, king):
        self.color = color
        self.king = king


"""------------------+
|     UNIT TESTS     |
+------------------"""

def test_simple():
    boardStart = [
            "#r#r#r#r",
            "r#r#r#r#",
            "#r#r#r#r",
            " # # # #",
            "# # # # ",
            "w#w#w#w#",
            "#w#w#w#w",
            "w#w#w#w#"
            ]
    selectedPiece = (2, 5)
    movement = [[(2, 5), (1, 4)], [(2, 5), (3, 4)]]
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement

def test_capture_simple():
    boardStart = [
            "#r#r#r#r",
            "r#r#r#r#",
            "#r#r# #r",
            " # #r# #",
            "# #w# # ",
            "w# #w#w#",
            "#w#w#w#w",
            "w#w#w#w#"
            ]
    selectedPiece = (3, 4)
    movement = [[(3, 4), (4, 3), (5, 2)]]
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement

def test_capture_enforce():
    boardStart = [
            "#r#r#r#r",
            "r#r#r#r#",
            "#r#r# #r",
            " # #r# #",
            "# #w# # ",
            "w# #w#w#",
            "#w#w#w#w",
            "w#w#w#w#"
            ]
    selectedPiece = (4, 5)
    movement = []
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement

def test_capture_multiple():
    boardStart = [
            "#r#r#r# ",
            "r#r#r#r#",
            "#r#r# #r",
            " # #r# #",
            "# #w# # ",
            "w# #w#w#",
            "#w#w#w#w",
            "w#w#w#w#"
            ]
    selectedPiece = (3, 4)
    movement = [[(3, 4), (4, 3), (5, 2), (6, 1), (7, 0)]]
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement

def test_capture_multiple_enforce():
    boardStart = [
            "#r#r#r# ",
            "r#r#r#r#",
            "# #r# #r",
            " #r#r# #",
            "# #w# # ",
            "w# #w#w#",
            "#w#w#w#w",
            "w#w#w#w#"
            ]
    selectedPiece = (3, 4)
    movement = [[(3, 4), (4, 3), (5, 2), (6, 1), (7, 0)]]
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement

def test_capture_multiple_crosspaths():
    boardStart = [
            "#r# #r# ",
            "r#r#r#r#",
            "# #r# #r",
            " #r#r# #",
            "# #w# # ",
            "w# #w#w#",
            "#w#w#w#w",
            "w#w#w#w#"
            ]
    selectedPiece = (3, 4)
    movement = [
            [(3, 4), (4, 3), (5, 2), (4, 1), 
                    (3, 0), (2, 1), (1, 2), (2, 3), (3, 4)], 
            [(3, 4), (2, 3), (1, 2), (2, 1), 
                    (3, 0), (4, 1), (5, 2), (4, 3), (3, 4)],
            [(3, 4), (2, 3), (1, 2), (2, 1), 
                    (3, 0), (4, 1), (5, 2), (6, 1), (7, 0)]        
            ]
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement

def test_king_move():
    boardStart = [
            "# # # #r",
            " # # # #",
            "# # # # ",
            " # # # #",
            "# #W# # ",
            " # # # #",
            "#w# # # ",
            " # # # #"
            ]
    selectedPiece = (3, 4)
    movement = [
            [(3, 4), (2, 5)], 
            [(3, 4), (4, 5)],
            [(3, 4), (4, 5), (5, 6)],
            [(3, 4), (4, 5), (5, 6), (6, 7)],
            [(3, 4), (2, 3)],
            [(3, 4), (2, 3), (1, 2)],
            [(3, 4), (2, 3), (1, 2), (0, 1)],
            [(3, 4), (4, 3)],
            [(3, 4), (4, 3), (5, 2)],
            [(3, 4), (4, 3), (5, 2), (6, 1)]
            ]
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement

def test_king_capture():
    boardStart = [
            "#R#R#R# ",
            " # # # #",
            "# # #R# ",
            " # # # #",
            "# #W#W# ",
            " # # # #",
            "# # # # ",
            " # #W#W#"
            ]
    selectedPiece = (3, 4)
    movement = [[(3, 4), (4, 3), (5, 2), (6, 1)]]
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement

def test_backcapture():
    boardStart = [
            "#r#r#r#r",
            "r#r#r#r#",
            "#r#r# #w",
            " # # #r#",
            "# # # # ",
            "w#w#w# #",
            "#w#w#w#w",
            "w#w#w#w#"
            ]
    selectedPiece = (7, 2)
    movement = [[(7, 2), (6, 3), (5, 4)]]
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement

def test_kingedgecase1():
    boardStart = [
            "# # # # ",
            " # # # #",
            "# # #R# ",
            " # #W# #",
            "# # # # ",
            " # # # #",
            "# # # # ",
            "W# # #W#"
            ]
    selectedPiece = (4, 3)
    movement = [[(4, 3), (5, 2), (6, 1)]]
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement


