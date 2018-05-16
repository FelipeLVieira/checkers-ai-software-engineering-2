import pygame
import copy
from Constants import *


class Board:
    def __init__(self, board=None):
        # This allows us to make a copy of the board for the AI to safely
        # recurse on.
        if board is Board:
            self.matrix = board.matrix
        self.matrix = self.newBoard()

        self.pieceBestMoves = []
        self.selectedLegalMoves = None
        self.selectedPieceCoordinate = None
        self.mouseClick = None
        self.playerTurn = None

    """-------------------+
    |  Board Initializer  |
    +-------------------"""

    def newBoard(self):

        # Initialize squares and place them in matrix

        matrix = [[None] * 8 for i in range(8)]

        for x in range(8):
            for y in range(8):
                if (x % 2 != 0) and (y % 2 == 0):
                    matrix[x][y] = Square(BLACK)
                elif (x % 2 != 0) and (y % 2 != 0):
                    matrix[x][y] = Square(WHITE)
                elif (x % 2 == 0) and (y % 2 != 0):
                    matrix[x][y] = Square(BLACK)
                elif (x % 2 == 0) and (y % 2 == 0):
                    matrix[x][y] = Square(WHITE)

        # initialize the pieces and put them in the appropriate squares
        for x in range(8):
            for y in range(3):
                if matrix[x][y].color == BLACK:
                    matrix[x][y].occupant = Piece(RED, True)
            for y in range(5, 8):
                if matrix[x][y].color == BLACK:
                    matrix[x][y].occupant = Piece(WHITE, True)

        return matrix

    def boardString(self, board):
        """
        Takes a board and returns a matrix of the board space colors. Used for testing new_board()
        """

        boardString = [[None] * 8 for i in range(8)]

        for x in range(0, 8):
            for y in range(0, 8):
                if board[x][y].color is BLACK:
                    if board[x][y].occupant is None:
                        boardString[x][y] = "B"
                        continue
                    elif board[x][y].occupant.color is WHITE:
                        boardString[x][y] = "WHITE"
                        continue
                    elif board[x][y].occupant.color is RED:
                        boardString[x][y] = "RED"
                        continue
                else:
                    boardString[x][y] = "W"
                    continue

        return boardString

    def nextCoordinate(self, dir, coordinate):
        """
        Returns the coordinates one square in a different direction to (x,y).
        """
        if dir == NORTHWEST:
            return Coordinate(coordinate.x - 1, coordinate.y - 1)
        elif dir == NORTHEAST:
            return Coordinate(coordinate.x + 1, coordinate.y - 1)
        elif dir == SOUTHWEST:
            return Coordinate(coordinate.x - 1, coordinate.y + 1)
        elif dir == SOUTHEAST:
            return Coordinate(coordinate.x + 1, coordinate.y + 1)
        else:
            return 0

    def afterNextCoordinate(self, dir, coordinate):
        """
        Returns the coordinates one square in a different direction to (x,y).
        """
        if dir == NORTHWEST:
            return Coordinate(coordinate.x - 2, coordinate.y - 2)
        elif dir == NORTHEAST:
            return Coordinate(coordinate.x + 2, coordinate.y - 2)
        elif dir == SOUTHWEST:
            return Coordinate(coordinate.x - 2, coordinate.y + 2)
        elif dir == SOUTHEAST:
            return Coordinate(coordinate.x + 2, coordinate.y + 2)
        else:
            return 0

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

    def canMoveDirection(self, DIRECTION, currentCoordinate):
        if self.onBoard(self.nextCoordinate(DIRECTION, currentCoordinate)):
            if self.location(self.nextCoordinate(DIRECTION, currentCoordinate)).occupant is None:
                return True
            else:
                return False

    def canJumpDirection(self, DIRECTION, legalMove):
        """
            Given a coordinate, color, direction and a list of moves, checks if there's another available jump
        """
        currentPosition = legalMove[-1]
        previous = None
        if len(legalMove) > 1:
            previous = legalMove[-2]

        if self.onBoard(self.nextCoordinate(DIRECTION, currentPosition)) \
                and self.onBoard(self.afterNextCoordinate(DIRECTION, currentPosition)) \
                and self.location(
            self.nextCoordinate(DIRECTION, currentPosition)).occupant is not None \
                and self.location(self.afterNextCoordinate(DIRECTION, currentPosition)).occupant is None \
                and self.nextCoordinate(DIRECTION, currentPosition) is not previous \
                and self.afterNextCoordinate(DIRECTION,currentPosition) is not previous \
                and not self.moveContainsCoordinate(self.afterNextCoordinate(DIRECTION, currentPosition), legalMove) \
                and self.playerTurn is not self.location(self.nextCoordinate(DIRECTION, currentPosition)).occupant.color:
            return True

        return False

    def kingInitialLegalMove(self, currentCoordinate, auxCoordinateList, playerTurn, DIRECTION):
        print("auxCoordinateList", auxCoordinateList)
        if self.canMoveDirection(DIRECTION, currentCoordinate):
            auxCoordinateList = [currentCoordinate]
            nextCoord = currentCoordinate
            while self.canMoveDirection(DIRECTION, auxCoordinateList[-1]):
                auxCoordinateList += [self.nextCoordinate(DIRECTION, nextCoord)]
                if not self.canMoveDirection(DIRECTION, auxCoordinateList[-1]):
                    break
                else:
                    nextCoord = self.nextCoordinate(DIRECTION, nextCoord)

                # Checks if didn't enter inside while (it can't move except for jump pieces
                if not auxCoordinateList[0] == nextCoord:
                    # Can still jump after few cells move?
                    if self.canJumpDirection(DIRECTION, auxCoordinateList):
                        # Add the jump coordinates
                        auxCoordinateList += [self.nextCoordinate(DIRECTION, auxCoordinateList[-1])]
                        auxCoordinateList += [self.afterNextCoordinate(DIRECTION, currentCoordinate)]

        # After verify if the variable nextCoord didn't get new moves, verify if it can jump an adjacent
        if not auxCoordinateList and self.canJumpDirection(DIRECTION, currentCoordinate):
            auxCoordinateList = [currentCoordinate]
            auxCoordinateList += [self.nextCoordinate(DIRECTION, currentCoordinate)]
            auxCoordinateList += [self.afterNextCoordinate(DIRECTION, currentCoordinate)]

        return auxCoordinateList

    def getPieceJumps(self, moveSet, king):

        if len(moveSet) == 1:
            return

        copied = False
        moveQueue = []
        if self.canJumpDirection(NORTHWEST, moveSet):
            refPiece = moveSet[-1]
            moveSetCopy = copy.deepcopy(moveSet)
            moveSetCopy += self.nextCoordinate(NORTHWEST, refPiece)
            moveSetCopy += self.afterNextCoordinate(NORTHWEST, refPiece)
            moveQueue.append(moveSetCopy)

        if self.canJumpDirection(NORTHEAST, moveSet):
            refPiece = moveSet[-1]
            moveSetCopy = copy.deepcopy(moveSet)
            moveSetCopy += self.nextCoordinate(NORTHEAST, refPiece)
            moveSetCopy += self.afterNextCoordinate(NORTHEAST, refPiece)
            moveQueue.append(moveSetCopy)

        if self.canJumpDirection(SOUTHWEST, moveSet):
            refPiece = moveSet[-1]
            moveSetCopy = copy.deepcopy(moveSet)
            moveSetCopy += self.nextCoordinate(SOUTHWEST, refPiece)
            moveSetCopy += self.afterNextCoordinate(SOUTHWEST, refPiece)
            moveQueue.append(moveSetCopy)

        if self.canJumpDirection(SOUTHEAST, moveSet):
            refPiece = moveSet[-1]
            moveSetCopy = copy.deepcopy(moveSet)
            moveSetCopy += self.nextCoordinate(SOUTHEAST, refPiece)
            moveSetCopy += self.afterNextCoordinate(SOUTHEAST, refPiece)
            moveQueue.append(moveSetCopy)

        return moveQueue

    """-------------------------------+
    |  Player all pieces Moves Logic  |
    +-------------------------------"""

    def getLegalMoves(self):

        # Get a list of all legal moves
        legalMoveSet = []
        for x in range(8):
            for y in range(8):
                coordinate = Coordinate(x, y)
                if self.matrix[x][y].occupant is not None \
                        and self.matrix[x][y].occupant.color is self.playerTurn:
                    for move in self.legalMovesByPiece(coordinate, self.location(coordinate).occupant.king):
                        if move and move not in legalMoveSet:
                            legalMoveSet.append(move)

        print("before get best moves - ", legalMoveSet)

        legalMoveSet = self.getBestMoves(legalMoveSet, self.playerTurn)

        print("getLegalMoves - legalMoveSet", legalMoveSet)

        return legalMoveSet

    """--------------------------+
    |  Single Piece Moves Logic  |
    +--------------------------"""

    def legalMovesByPiece(self, pieceCoordinate, king=False):
        """
        Look for all possible movements recursively and return a list of possible moves
        """
        legalMove = []
        legalMoves = []

        print("pieceCoordinate", pieceCoordinate)

        if (self.playerTurn is WHITE or king) and self.canMoveDirection(NORTHWEST, pieceCoordinate):
            legalMove.append(copy.deepcopy(pieceCoordinate))
            legalMove.append(self.nextCoordinate(NORTHWEST, legalMove[0]))

            print("legalMove", legalMove)
            if king:
                aux = legalMove[0]
                while self.canMoveDirection(NORTHWEST, self.nextCoordinate(NORTHWEST, aux)):
                    legalMove.append(self.nextCoordinate(NORTHWEST, aux))
                    aux = self.nextCoordinate(NORTHWEST, aux)

                if self.canJumpDirection(NORTHWEST, legalMove):
                    legalMove.append(self.nextCoordinate(NORTHWEST, pieceCoordinate))
                    legalMove.append(self.afterNextCoordinate(NORTHWEST, pieceCoordinate))
                    # Jumped first piece
                    # Get subsequent king jumps
                    # moveSets = self.getPieceJumps(legalMove, king)
                # else:
                    # Get subsequent simple jumps
                    # moveSets = self.getPieceJumps(legalMove, king)

                # legalMoves.append(moveSets)
                legalMoves.append(legalMove)
                legalMove = []

        if (self.playerTurn is WHITE or king) and self.canMoveDirection(NORTHEAST, pieceCoordinate):
            legalMove.append(copy.deepcopy(pieceCoordinate))
            legalMove.append(self.nextCoordinate(NORTHEAST, legalMove[0]))

            print("legalMove", legalMove)
            if king:
                aux = legalMove[0]
                while self.canMoveDirection(NORTHEAST, self.nextCoordinate(NORTHEAST, aux)):
                    legalMove.append(self.nextCoordinate(NORTHEAST, aux))
                    aux = self.nextCoordinate(NORTHEAST, aux)

                if self.canJumpDirection(NORTHEAST, legalMove):
                    legalMove.append(self.nextCoordinate(NORTHEAST, pieceCoordinate))
                    legalMove.append(self.afterNextCoordinate(NORTHEAST, pieceCoordinate))
                    # Jumped first piece
                    # Get subsequent king jumps
                    # moveSets = self.getPieceJumps(legalMove, king)
                # else:
                    # Get subsequent simple jumps
                    # moveSets = self.getPieceJumps(legalMove, king)

                # legalMoves.append(moveSets)
                legalMoves.append(legalMove)
                legalMove = []

        print("legalMoves final", legalMoves)

        return legalMoves

    def getBestMoves(self, legalMoves, playerTurn):

        self.pieceBestMoves = []

        print("legalMoves", legalMoves)

        for move in legalMoves:
            if self.location(move[0]) == self.location(self.selectedPieceCoordinate):
                self.pieceBestMoves.append(move)

        aux = 0
        jumpRef = 0
        auxMoves = []

        for move in self.pieceBestMoves:
            for coord in move:
                if self.location(coord).occupant:
                    if self.location(coord).occupant.color is not playerTurn:
                        aux += 1
            aux = 0
            if aux > jumpRef:
                jumpRef = aux

        for move in self.pieceBestMoves:
            for coord in move:
                if self.location(coord).occupant:
                    if self.location(coord).occupant.color is not playerTurn:
                        aux += 1
            aux = 0
            if aux == jumpRef:
                auxMoves.append(move)

        if jumpRef > 0:
            self.pieceBestMoves = auxMoves

        return self.pieceBestMoves

    def filterMoves(self, moves):

        if not moves:
            return []

        moves = [x for x in moves if x]

        for move in moves:
            if None in move:
                move.pop()

        return moves

    def exists(self):
        return self is not None

    def removePiecesByMove(self, move, player):
        """
        Removes enemy pieces from a move (x,y).
        """
        for coordinate in move:
            if self.location(coordinate).occupant:
                if self.location(coordinate).occupant.color is not player:
                    self.matrix[coordinate.x][coordinate.y].occupant = None

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
            self.matrix[endCoordinate.x][endCoordinate.y].occupant = self.matrix[startCoordinate.x][
                startCoordinate.y].occupant
            self.removePiece(startCoordinate)
        self.king(endCoordinate)

    def executeMove(self, playerTurn):
        print("executeMove")
        print(self.pieceBestMoves)
        for move in self.pieceBestMoves:
            for coord in move:
                if self.location(coord) == self.location(self.mouseClick):
                    self.movePiece(self.selectedPieceCoordinate, self.mouseClick)
                    self.removePiecesByMove(move, playerTurn)
                    return True
        return False


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
            if (self.location(coordinate).occupant.color == WHITE and coordinate.y == 0) or (
                    self.location(coordinate).occupant.color == RED and coordinate.y == 7):
                self.location(coordinate).occupant.king = True

    def drawBoardSquares(self, graphics):
        """
            Takes a board object and draws all of its squares to the display
            """
        for x in range(8):
            for y in range(8):
                pygame.draw.rect(graphics.screen, self.matrix[x][y].color,
                                 (x * graphics.squareSize, y * graphics.squareSize, graphics.squareSize,
                                  graphics.squareSize), )

    def drawBoardPieces(self, screen, redPiece, whitePiece):
        for x in range(8):
            for y in range(8):
                if self.matrix[x][y].occupant is not None and self.matrix[x][y].color is BLACK and self.matrix[x][
                    y].occupant.color is RED:
                    screen.blit(redPiece, (x * 90, y * 90))

                if self.matrix[x][y].occupant is not None and self.matrix[x][y].color is BLACK and self.matrix[x][
                    y].occupant.color is WHITE:
                    screen.blit(whitePiece, (x * 90, y * 90))

    def drawBoardKings(self, screen, kingPiece):
        for x in range(8):
            for y in range(8):
                if self.matrix[x][y].occupant is not None and self.matrix[x][y].occupant.king:
                    screen.blit(kingPiece, (x * 90, y * 90))

    def highlightLegalMoves(self, legalMoves, selectedPiece, screen, goldPiece):
        if selectedPiece is not None and legalMoves is not None:

            for movePath in legalMoves:
                for coordinate in movePath:
                    if coordinate is not None and not self.location(coordinate).occupant:
                        screen.blit(goldPiece, (coordinate.x * 90, coordinate.y * 90))

    def pixelCoords(self, coordinate, squareSize, pieceSize):
        """
            Takes in a tuple of board coordinates (x,y)
            and returns the pixel coordinates of the center of the square at that location.
        """
        return (
            coordinate.x * squareSize + pieceSize, coordinate.y * squareSize + pieceSize)

    def boardCoords(self, pixelCoordinate, squareSize):
        """
           Does the reverse of pixel_coords(). Takes in a tuple of of pixel coordinates and returns what square they are in.
        """
        return Coordinate(int(pixelCoordinate[0] / squareSize), int(pixelCoordinate[1] / squareSize))

    def pixelToSquarePosition(self, pixelCoordinate, squareSize):
        """
            Does the reverse of pixel_coords(). Takes in a tuple of of pixel coordinates and returns what square they are in.
        """
        return Coordinate(pixelCoordinate.x / squareSize, pixelCoordinate.y / squareSize)

    def piecePositionToPixel(self, boardPiece):
        return True


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Piece:
    def __init__(self, color, king=False):
        self.color = color
        self.king = king

    def getPlayerColor(self):
        return WHITE

    def getEnemyColor(self):
        return RED


class Square:
    def __init__(self, color, occupant=None):
        self.color = color  # color is either BLACK or WHITE
        self.occupant = occupant  # occupant is a Square object


class Direction:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
