import pygame
import copy
from Constants import *


def lookup(matrix, index):
    """Looks up an index, defined by a tuple, in a multidimensional array."""
    result = matrix
    for i in index:
        result = result[i]
    return result


class Board:
    def __init__(self, board=None):
        # This allows us to make a copy of the board for the AI to safely
        # recurse on.
        # Load the board matrix
        if isinstance(board, Board):
            self.matrix = copy.deepcopy(board.matrix)
        elif isinstance(board, list):
            self.matrix = self.boardFromStrings(board)
        else:
            self.matrix = self.newBoard()

        # Cache of list of legal moves for the board in this turn;
        # Must be set to None at the end of a turn.
        self.legalMoveSet = None

        # Indicates which player is currently playing.
        self.playerTurn = WHITE

        # Cache of moves list from selected piece
        self.selectedPieceMoves = None
        # Cache of selected piece
        self.selectedPieceCoordinate = None
        # Cache of mouse click
        self.mouseClick = None

        self.isPlayerRedLost = False
        self.isPlayerWhiteLost = False
        self.isDraw = False
        self.kingRedCounterAux = 0
        self.kingRedCounter = 0
        self.redCounterAux = 12
        self.redCounter = 0
        self.kingWhiteCounterAux = 0
        self.kingWhiteCounter = 0
        self.whiteCounterAux = 12
        self.whiteCounter = 0
        self.numberOfPlays = 0
        self.numberOfPlays2 = 0

    def newBoard(self):
        """Creates a matrix containing a new board."""
        matrix = []
        for x in range(8):
            row = []
            for y in range(8):
                square = Square((x & 1) ^ (y & 1))
                if y < 3 and square.black:
                    square.occupant = Piece(RED, False)
                elif y > 4 and square.black:
                    square.occupant = Piece(WHITE, False)
                row.append(square)
            matrix.append(row)
        return matrix

    def nextCoordinate(self, direction, coordinate):
        """
        Returns the coordinates one square in a different direction to (x,y).
        """
        if direction == NORTHWEST:
            return Coordinate(coordinate.x - 1, coordinate.y - 1)
        elif direction == NORTHEAST:
            return Coordinate(coordinate.x + 1, coordinate.y - 1)
        elif direction == SOUTHWEST:
            return Coordinate(coordinate.x - 1, coordinate.y + 1)
        elif direction == SOUTHEAST:
            return Coordinate(coordinate.x + 1, coordinate.y + 1)
        else:
            return 0

    def afterNextCoordinate(self, direction, coordinate):
        """
        Returns the coordinates one square in a different direction to (x,y).
        """
        if direction == NORTHWEST:
            return Coordinate(coordinate.x - 2, coordinate.y - 2)
        elif direction == NORTHEAST:
            return Coordinate(coordinate.x + 2, coordinate.y - 2)
        elif direction == SOUTHWEST:
            return Coordinate(coordinate.x - 2, coordinate.y + 2)
        elif direction == SOUTHEAST:
            return Coordinate(coordinate.x + 2, coordinate.y + 2)
        else:
            return 0

    def canJumpAdjacent(self, coordinate):
        """
        Returns a list of squares locations that are adjacent (on a diagonal) to (x,y).
        """

        return self.canJumpDirection(NORTHWEST, self.nextCoordinate(NORTHWEST,
                                                                    coordinate)) \
               or self.canJumpDirection(NORTHEAST,
                                        self.nextCoordinate(NORTHEAST,
                                                            coordinate)) \
               or self.canJumpDirection(SOUTHWEST,
                                        self.nextCoordinate(SOUTHWEST,
                                                            coordinate)) \
               or self.canJumpDirection(SOUTHEAST,
                                        self.nextCoordinate(SOUTHEAST,
                                                            coordinate))

    def canMoveAdjacent(self, coordinate):
        """
        Returns a list of squares locations that are adjacent (on a diagonal) to (x,y).
        """

        return self.canMoveDirection(NORTHWEST, self.nextCoordinate(NORTHWEST,
                                                                    coordinate)) \
               or self.canMoveDirection(NORTHEAST,
                                        self.nextCoordinate(NORTHEAST,
                                                            coordinate)) \
               or self.canMoveDirection(SOUTHWEST,
                                        self.nextCoordinate(SOUTHWEST,
                                                            coordinate)) \
               or self.canMoveDirection(SOUTHEAST,
                                        self.nextCoordinate(SOUTHEAST,
                                                            coordinate))

    def adjacent(self, coordinate):
        """
        Returns a list of squares locations that are adjacent (on a diagonal) to (x,y).
        """

        return [self.nextCoordinate(NORTHWEST, coordinate),
                self.nextCoordinate(NORTHEAST, coordinate),
                self.nextCoordinate(SOUTHWEST, coordinate),
                self.nextCoordinate(SOUTHEAST, coordinate)]

    def location(self, coordinate):
        """
        Takes a set of coordinates as arguments and returns self.matrix[x][y]
        This can be faster than writing something like self.matrix[coords[0]][coords[1]]
        """
        if not coordinate:
            return
        return self.matrix[coordinate.x][coordinate.y]

    def moveContainsCoordinate(self, coordinate, move):
        """
        Check if the coordinate already exists in the move coordinate list
        """
        for m in move:
            if m.x == coordinate.x and m.y == coordinate.y:
                return True
        return False

    def canMoveDirection(self, direction, currentCoordinate):
        if self.onBoard(self.nextCoordinate(direction, currentCoordinate)):
            if self.location(self.nextCoordinate(direction,
                                                 currentCoordinate)).occupant is None:
                return True
            else:
                return False

    def canJumpDirection(self, direction, coordinate):
        """
            Given a coordinate, color, direction and a list of moves, checks if there's another available jump
        """

        if not coordinate:
            return

        nextSquare = self.nextCoordinate(direction, coordinate)
        afterNextSquare = self.afterNextCoordinate(direction, coordinate)

        if self.onBoard(nextSquare) \
                and self.onBoard(afterNextSquare) \
                and self.location(nextSquare).occupant is not None \
                and self.location(afterNextSquare).occupant is None \
                and self.playerTurn is not self.location(
            nextSquare).occupant.color:
            return True

        return False

    def getDirection(self, previous, refSquare):
        aux = self.nextCoordinate(NORTHWEST, previous)
        if aux.x == refSquare.x and aux.y == refSquare.y:
            return NORTHWEST
        aux = self.nextCoordinate(NORTHEAST, previous)
        if aux.x == refSquare.x and aux.y == refSquare.y:
            return NORTHEAST
        aux = self.nextCoordinate(SOUTHWEST, previous)
        if aux.x == refSquare.x and aux.y == refSquare.y:
            return SOUTHWEST
        aux = self.nextCoordinate(SOUTHEAST, previous)
        if aux.x == refSquare.x and aux.y == refSquare.y:
            return SOUTHEAST

    def getDirectionByJump(self, previous, refSquare):
        aux = self.afterNextCoordinate(NORTHWEST, previous)
        if aux.x == refSquare.x and aux.y == refSquare.y:
            return NORTHWEST
        aux = self.afterNextCoordinate(NORTHEAST, previous)
        if aux.x == refSquare.x and aux.y == refSquare.y:
            return NORTHEAST
        aux = self.afterNextCoordinate(SOUTHWEST, previous)
        if aux.x == refSquare.x and aux.y == refSquare.y:
            return SOUTHWEST
        aux = self.afterNextCoordinate(SOUTHEAST, previous)
        if aux.x == refSquare.x and aux.y == refSquare.y:
            return SOUTHEAST

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
                if (self.matrix[x][y].occupant is not None
                        and self.matrix[x][
                            y].occupant.color is self.playerTurn):
                    # print((x, y))
                    for move in self.theoreticalLegalMoves((x, y)):
                        if move not in self.legalMoveSet:
                            self.legalMoveSet.append(move)

                            rank = self.moveRank(move)
                            if highestMoveRank < rank: highestMoveRank = rank

        # Filter out moves that aren't the highest rank, to enforce the
        # longest captures

        # print("BoardLogic.py::Board:getAllLegalMoves: Unfiltered legal moves:")
        # for move in self.legalMoveSet: print(move)

        # print("BoardLogic.py::Board:getAllLegalMoves: Highest move rank is {}".format(highestMoveRank))

        illegalMoves = []
        for move in self.legalMoveSet:
            if self.moveRank(move) < highestMoveRank:
                # print("BoardLogic.py::Board:getAllLegalMoves: Move {} has rank {} < {}, dropping.".format(move, self.moveRank(move), highestMoveRank))
                illegalMoves.append(move)

        for move in illegalMoves: self.legalMoveSet.remove(move)

        # For debugging only... comment this later
        # print("BoardLogic.py::Board:getAllLegalMoves: Legal moves:")
        # for move in self.legalMoveSet: print(move)

        print ("return self.legalMoveSet from getAllLegalMoves", self.legalMoveSet)
        return self.legalMoveSet

    """-----------------------------------------+
    |  AUXILIARY MOVEMENT EVALUATION FUNCTIONS  |
    +-----------------------------------------"""

    def moveRank(self, move):
        """Calculates the rank for a move.
        A move's rank is given by its number of captured pieces."""
        rank = 0
        start = derefer(self.matrix, move[0]).occupant
        for coord in move:
            # If there's a piece in that coordinate
            square = derefer(self.matrix, coord).occupant
            # print(coord, square)
            if square and square.color is not start.color:
                # print(square.color, start.color)
                rank += 1
        return rank

    """--------------------------------------------------------------------"""

    def theoreticalLegalMoves(self, pieceCoords):
        """Returns the possible moves for a piece if there were no
        higher-ranked moves possible."""
        # Dereference the coordinates to get the square object
        square = derefer(self.matrix, pieceCoords)

        if square.occupant.king:
            return self.theoreticalKingLegalMoves(pieceCoords)
        moveList = []

        deltaDict = {WHITE: [(-1, -1), (1, -1)], RED: [(-1, 1), (1, 1)]}

        for delta in deltaDict[square.occupant.color]:
            # print("BoardLogic.py::Board:theoreticalLegalMoves: Evaluating delta {}".format(delta))
            deltaCoord = tplsum(pieceCoords, delta)
            # Verify that the value is in bounds
            if not bounded(deltaCoord, 0, 7): continue

            deltaSquare = derefer(self.matrix, deltaCoord)
            # Check if the delta square is occupied
            if deltaSquare.occupant:
                # If the piece in the delta square is the same color,
                # the move is impossible.
                if deltaSquare.occupant.color is square.occupant.color: continue

                # Otherwise, it's possibly a capture move. Deal with it.
                for move in self.possibleCaptures(square.occupant.color,
                                                  pieceCoords, delta,
                                                  pieceCoords):
                    moveList.append(move)
                    # print("Evaluated capture move {} for delta {}.".format(move, delta))

            else:
                # It's a valid movement.
                moveList.append([pieceCoords, deltaCoord])
        # print("Theoretical legal moves for {}:".format(pieceCoords))
        # for move in moveList: print(move)
        return moveList

    """--------------------------------------------------------------------"""

    def theoreticalKingLegalMoves(self, pieceCoords):
        """Returns the possible moves for a king if there were no
        higher-ranked moves possible."""
        # Dereference the coordinates to get the square object
        square = derefer(self.matrix, pieceCoords)
        moveList = []

        deltas = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        newPieceCoords = pieceCoords
        for delta in deltas:
            deltaCoord = tplsum(pieceCoords, delta)
            # Check all possible chain positions in bounds
            currentMove = [pieceCoords]
            while bounded(deltaCoord, 0, 7):
                deltaSquare = derefer(self.matrix, deltaCoord)
                # Check if the delta square is occupied
                if deltaSquare.occupant:
                    # If the piece in the delta square is the same color,
                    # the move is impossible. Break the chain.
                    if deltaSquare.occupant.color is square.occupant.color: break

                    # Otherwise, it's possibly a capture move. Deal with it.
                    for move in self.possibleCaptures(square.occupant.color,
                                                      newPieceCoords, delta,
                                                      pieceCoords):
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

        # print("Theoretical legal moves for {}:".format(pieceCoords))
        # for move in moveList: print(move)
        return moveList

    """--------------------------------------------------------------------"""

    def possibleCaptures(self, pieceColor, pieceCoords, delta, startPosition,
                         capturedPieces=None):
        """Recursively evaluates a capture and searches for capture chains."""
        deltaCoord = tplsum(pieceCoords, delta)
        landingCoord = tplsum(deltaCoord, delta)
        # print("BoardLogic.py::Board:possibleCaptures: New call at {} ({} -> {} - > {} with capturedPieces = {})".format(pieceCoords, pieceCoords, deltaCoord, landingCoord, capturedPieces))

        # Check if the delta and landing squares are in bounds
        if not bounded(deltaCoord, 0, 7) or not bounded(landingCoord, 0, 7):
            return []

        deltaSquare = derefer(self.matrix, deltaCoord)
        landingSquare = derefer(self.matrix, landingCoord)

        # Check if there is a piece that can be captured
        if ((not deltaSquare.occupant) or
                (deltaSquare.occupant.color is pieceColor)): return []

        # Check whether the landing square is clear
        if landingSquare.occupant and landingCoord != startPosition:
            # print("BoardLogic.py::Board:possibleCaptures: Landing square is not clear", landingCoord, startPosition)
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
                                                   newdelta, startPosition,
                                                   copy.deepcopy(
                                                       capturedPieces)):
                # print(extraMove)
                baseMove = [pieceCoords, deltaCoord]
                baseMove.extend(extraMove)
                # print("BoardLogic.py::Board:possibleCaptures: recursing into {} ({} -> {}) got {}".format(delta, landingCoord, tplsum(landingCoord, delta), baseMove))
                captureList.append(baseMove)

        return captureList

    """-------------------------------+
    |        UTILITY FUNCTIONS        |
    +-------------------------------"""

    def getBestMovesByPiece(self, pieceCoordinate, legalMoveSet):
        if not legalMoveSet:
            return

        jumpCounter = 0
        mostJumps = 0

        for move in legalMoveSet:
            for coord in move:
                if self.location(coord).occupant:
                    if self.location(
                            coord).occupant.color is not self.playerTurn:
                        jumpCounter += 1
            if jumpCounter > mostJumps:
                mostJumps = jumpCounter
            jumpCounter = 0

        bestMoves = []
        if mostJumps is not 0:
            auxBestMoves = []
            for move in legalMoveSet:
                for coord in move:
                    if self.location(coord).occupant:
                        if self.location(
                                coord).occupant.color is not self.playerTurn:
                            jumpCounter += 1
                if jumpCounter is mostJumps:
                    auxBestMoves.append(move)
                jumpCounter = 0

            for move in auxBestMoves:
                if move[0].x is pieceCoordinate.x and move[
                    0].y is pieceCoordinate.y:
                    bestMoves.append(move)
        else:
            for move in legalMoveSet:
                if move[0].x is pieceCoordinate.x and move[
                    0].y is pieceCoordinate.y:
                    bestMoves.append(move)

    def coordToTuple(coordinate):
        tup = (coordinate.x, coordinate.y)
        return tup

    def tupleToCoord(tup):
        coord = Coordinate(tup[0], tup[1])
        return coord

    def filterNoneOrEmptyMoves(self, movesSet):

        if not movesSet:
            return []

        movesSet = [x for x in movesSet if x]

        for move in movesSet:
            if None in move or [] in move:
                move.pop()

        return movesSet

    def exists(self):
        return self is not None

    def removePiecesByMove(self, move):
        """
        Removes enemy pieces from a move (x,y).
        """
        auxCopy = copy.deepcopy(move)
        auxCoordinate = auxCopy.pop(0)
        while auxCoordinate:
            if self.location(auxCoordinate) is self.location(self.mouseClick):
                break
            if self.location(auxCoordinate).occupant:
                if self.location(
                        auxCoordinate).occupant.color is not self.playerTurn:
                    self.matrix[auxCoordinate.x][
                        auxCoordinate.y].occupant = None
            auxCoordinate = auxCopy.pop(0)

    def removePiece(self, coordinate):
        """
        Removes a piece from the board at position (x,y).
        """
        self.matrix[coordinate.x][coordinate.y].occupant = None

    def movePiece(self, startCoordinate, endCoordinate):
        """
        Move a piece from (start_x, start_y) to (end_x, end_y).
        """
        if self.onBoard(startCoordinate) and self.onBoard(endCoordinate):
            self.matrix[endCoordinate.x][endCoordinate.y].occupant = \
                self.matrix[startCoordinate.x][
                    startCoordinate.y].occupant
            self.removePiece(startCoordinate)
        self.king(endCoordinate)
        self.verifyDrawCondition()

    def showCoordinates(self):
        if self.selectedPieceMoves is not None:
            for move in self.selectedPieceMoves:
                print("\n")
                for coord in move:
                    print("(", coord.x, coord.y, ") ")

    def executeMove(self):
        self.showCoordinates()
        if self.selectedPieceMoves is None:
            return False

        if self.location(self.selectedPieceCoordinate).occupant.king == False:
            longestMove = 0
            for move in self.selectedPieceMoves:
                if len(move) > longestMove:
                    longestMove = len(move)

            for move in self.selectedPieceMoves:
                if len(move) == longestMove:
                    contador = 0
                    for coord in move:
                        contador = contador + 1
                        if self.location(coord) == self.location(
                                self.mouseClick) and \
                                contador == longestMove:
                            self.movePiece(self.selectedPieceCoordinate,
                                           self.mouseClick)
                            self.removePiecesByMove(move)
                            return True
        else:
            for move in self.selectedPieceMoves:
                for coord in move:
                    if self.location(coord) == self.location(self.mouseClick):
                        self.movePiece(self.selectedPieceCoordinate,
                                       self.mouseClick)
                        self.removePiecesByMove(move)
                        return True

        return False

    def verifyWinCondition(self):
        self.isPlayerRedLost = True
        self.isPlayerWhiteLost = True
        for x in range(8):
            for y in range(8):
                if self.matrix[x][y].occupant is not None and self.matrix[x][
                    y].occupant.color is RED:
                    self.isPlayerRedLost = False
                elif self.matrix[x][y].occupant is not None and self.matrix[x][
                    y].occupant.color is WHITE:
                    self.isPlayerWhiteLost = False
                if self.isPlayerRedLost is False and self.isPlayerWhiteLost is False:
                    break;

    def getPlayerWhiteLostInformation(self):
        return self.isPlayerWhiteLost

    def getPlayerRedLostInformation(self):
        return self.isPlayerRedLost

    def verifyDrawCondition(self):
        self.whiteCounter = 0
        self.kingWhiteCounter = 0
        self.redCounter = 0
        self.kingRedCounter = 0
        for x in range(8):
            for y in range(8):
                if self.matrix[x][y].occupant is not None and self.matrix[x][
                    y].occupant.king \
                        and self.matrix[x][y].occupant.color is WHITE:
                    if self.kingWhiteCounterAux == 0:
                        self.kingWhiteCounterAux = 1
                    self.kingWhiteCounter = self.kingWhiteCounter + 1
                elif self.matrix[x][y].occupant is not None and self.matrix[x][
                    y].occupant.king \
                        and self.matrix[x][y].occupant.color is RED:
                    if self.kingRedCounterAux == 0:
                        self.kingRedCounterAux = 1
                    self.kingRedCounter = self.kingRedCounter + 1
                elif self.matrix[x][y].occupant is not None and self.matrix[x][
                    y].occupant.color is WHITE:
                    self.whiteCounter = self.whiteCounter + 1
                elif self.matrix[x][y].occupant is not None and self.matrix[x][
                    y].occupant.color is RED:
                    self.redCounter = self.redCounter + 1

        'Draw conditions'

        if (
                self.kingWhiteCounterAux != self.kingWhiteCounter or self.kingRedCounterAux != self.kingRedCounter) and \
                self.whiteCounterAux == self.whiteCounter and self.redCounterAux == self.redCounter:
            self.numberOfPlays = self.numberOfPlays + 1
        else:
            self.numberOfPlays = 0

        if (self.kingWhiteCounterAux == self.kingWhiteCounter and
                (self.kingWhiteCounter == 2 or self.kingWhiteCounter == 1) and
                self.kingRedCounterAux == self.kingRedCounter and
                (self.kingRedCounter == 2 or self.kingRedCounter == 1) and
                self.whiteCounterAux == 0 and self.redCounterAux == 0):
            self.numberOfPlays2 = self.numberOfPlays2 + 1
        elif (
                self.kingWhiteCounterAux == self.kingWhiteCounter and self.kingWhiteCounter == 2 and
                self.kingRedCounterAux == self.kingRedCounter and self.kingRedCounter == 1 and
                self.redCounterAux == self.redCounter and self.redCounter == 1 and self.whiteCounterAux == 0) or \
                (
                        self.kingRedCounterAux == self.kingRedCounter and self.kingRedCounterAux == 2 and
                        self.kingWhiteCounterAux == self.kingWhiteCounter and self.kingWhiteCounter == 1 and
                        self.whiteCounterAux == self.whiteCounter and self.whiteCounter == 1 and self.redCounterAux == 0) or \
                (
                        self.kingWhiteCounterAux == self.kingWhiteCounter and self.kingWhiteCounter == 1 and
                        self.kingRedCounterAux == self.kingRedCounter and self.kingRedCounter == 1 and
                        self.redCounterAux == self.redCounter and self.redCounter == 1 and self.whiteCounterAux == 0) or \
                (
                        self.kingRedCounterAux == self.kingRedCounter and self.kingRedCounterAux == 1 and
                        self.kingWhiteCounterAux == self.kingWhiteCounter and self.kingWhiteCounter == 1 and
                        self.whiteCounterAux == self.whiteCounter and self.whiteCounter == 1 and self.redCounterAux == 0):
            self.numberOfPlays2 = self.numberOfPlays2 + 1
        else:
            self.numberOfPlays2 = 0
        print(str(self.numberOfPlays) + ', ' + str(self.numberOfPlays2))
        self.kingWhiteCounterAux = self.kingWhiteCounter
        self.kingRedCounterAux = self.kingRedCounter
        self.whiteCounterAux = self.whiteCounter
        self.redCounterAux = self.redCounter

        'DEIXAR numberOfPlays IGUAL A 4 POIS ASSIM CONTABILIZA 5 MOVES'
        if self.numberOfPlays == 20 or self.numberOfPlays2 == 4:
            self.isDraw = True

    def getDrawInformation(self):
        return self.isDraw

    def isEndSquare(self, coordinate):
        """
        Is passed a coordinate tuple (x,y), and returns true or
        false depending on if that square on the board is an end square.
        """

        if coordinate.x == 0 or coordinate.x == 7:
            return True
        else:
            return False

    def onBoard(self, coordinate):
        """
        Checks to see if the given square (x,y) lies on the board.
        If it does, then on_board() return True. Otherwise it returns false.
        """

        if coordinate.x < 0 or coordinate.y < 0 or coordinate.x > 7 or coordinate.y > 7:
            return False
        else:
            return True

    def king(self, coordinate):
        """
        Takes in (x,y), the coordinates of square to be considered for kinging.
        If it meets the criteria, then king() kings the piece in that square and kings it.
        """
        if self.location(coordinate).occupant is not None:
            if (self.location(
                    coordinate).occupant.color == WHITE and coordinate.y == 0) or (
                    self.location(
                        coordinate).occupant.color == RED and coordinate.y == 7):
                self.location(coordinate).occupant.king = True

    def drawBoardSquares(self, graphics):
        """
            Takes a board object and draws all of its squares to the display
            """
        for x in range(8):
            for y in range(8):
                pygame.draw.rect(graphics.screen,
                                 self.matrix[x][y].occupant.color,
                                 (x * graphics.squareSize,
                                  y * graphics.squareSize, graphics.squareSize,
                                  graphics.squareSize), )

    def drawBoardPieces(self, screen, redPiece, whitePiece):
        for x in range(8):
            for y in range(8):
                if self.matrix[x][y].occupant is not None and self.matrix[x][
                    y].occupant.color is RED:
                    screen.blit(redPiece, (x * 90, y * 90))

                if self.matrix[x][y].occupant is not None and self.matrix[x][
                    y].occupant.color is WHITE:
                    screen.blit(whitePiece, (x * 90, y * 90))

    def drawBoardKings(self, screen, kingPiece):
        for x in range(8):
            for y in range(8):
                if self.matrix[x][y].occupant is not None and self.matrix[x][
                    y].occupant.king:
                    screen.blit(kingPiece, (x * 90, y * 90))

    def highlightLegalMoves(self, screen, goldPiece):
        if self.selectedPieceCoordinate is not None and self.selectedPieceMoves is not None:

            for movePath in self.selectedPieceMoves:
                for coordinate in movePath:
                    if coordinate is not None and not self.location(
                            coordinate).occupant:
                        screen.blit(goldPiece,
                                    (coordinate.x * 90, coordinate.y * 90))

    def pixelCoords(self, coordinate, squareSize, pieceSize):
        """
            Takes in a tuple of board coordinates (x,y)
            and returns the pixel coordinates of the center of the square at that location.
        """
        return (
            coordinate.x * squareSize + pieceSize,
            coordinate.y * squareSize + pieceSize)

    def boardCoords(self, pixelCoordinate, squareSize):
        """
           Does the reverse of pixel_coords(). Takes in a tuple of of pixel coordinates and returns what square they are in.
        """
        return (int(pixelCoordinate[0] / squareSize),
                          int(pixelCoordinate[1] / squareSize))

    def pixelToSquarePosition(self, pixelCoordinate, squareSize):
        """
            Does the reverse of pixel_coords(). Takes in a tuple of of pixel coordinates and returns what square they are in.
        """
        return Coordinate(pixelCoordinate.x / squareSize,
                          pixelCoordinate.y / squareSize)

    def piecePositionToPixel(self, boardPiece):
        return True

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
            "r": (RED, False),
            "R": (RED, True)
        }

        for x in range(8):
            for y in range(8):
                if (x & 1) ^ (y & 1):
                    boardMatrix[x][y].black = True
                    if boardDescription[y][x] in parseDict.keys():
                        boardMatrix[x][y].occupant = (
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
                    if self.matrix[x][y].occupant is None:
                        row.append(" ")
                    elif (self.matrix[x][y].occupant.color is WHITE and
                          self.matrix[x][y].occupant.king):
                        row.append("W")
                    elif (self.matrix[x][y].occupant.color is RED and
                          self.matrix[x][y].occupant.king):
                        row.append("R")
                    elif self.matrix[x][y].occupant.color is WHITE:
                        row.append("w")
                    elif self.matrix[x][y].occupant.color is RED:
                        row.append("r")
                else:
                    row.append("#")
            boardString.append(''.join(row))

        return boardString


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

    def __init__(self, black, occupant=None):
        self.black = bool(black)
        self.occupant = occupant


class Piece:
    def __init__(self, color, king=False):
        self.color = color
        self.king = king

    def getPlayerColor(self):
        return WHITE

    def getEnemyColor(self):
        return RED


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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
