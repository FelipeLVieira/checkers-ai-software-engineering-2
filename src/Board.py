import pygame
import pygame
import copy
from Constants import *


class Board:
    def __init__(self, board=None):
        # This allows us to make a copy of the board for the AI to safely
        # recurse on.
        if board is Board:
            self.matrix = copy.deepcopy(board.matrix)
        self.matrix = self.newBoard()

        self.selectedPieceMoves = None
        self.playerLegalMoves = None
        self.selectedPieceCoordinate = None
        self.mouseClick = None
        self.playerTurn = None

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

    def canJumpAdjacent(self, coordinate):
        """
        Returns a list of squares locations that are adjacent (on a diagonal) to (x,y).
        """

        return self.canJumpDirection(NORTHWEST, self.nextCoordinate(NORTHWEST, coordinate)) \
            or self.canJumpDirection(NORTHEAST, self.nextCoordinate(NORTHEAST, coordinate)) \
            or self.canJumpDirection(SOUTHWEST, self.nextCoordinate(SOUTHWEST, coordinate)) \
            or self.canJumpDirection(SOUTHEAST, self.nextCoordinate(SOUTHEAST, coordinate))

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

    def canJumpDirection(self, DIRECTION, coordinate):
        """
            Given a coordinate, color, direction and a list of moves, checks if there's another available jump
        """

        if not coordinate:
            return

        nextSquare = self.nextCoordinate(DIRECTION, coordinate)
        afterNextSquare = self.afterNextCoordinate(DIRECTION, coordinate)

        if self.onBoard(nextSquare) \
                and self.onBoard(afterNextSquare) \
                and self.location(nextSquare).occupant is not None \
                and self.location(afterNextSquare).occupant is None \
                and self.playerTurn is not self.location(nextSquare).occupant.color:
            return True

        return False

    def getRegularMovesByPiece(self, pieceCoordinate, king):
        if not pieceCoordinate:
            return

        move = []
        moveSet = []

        if not king and self.playerTurn is WHITE:
            if self.canMoveDirection(NORTHWEST, pieceCoordinate):
                move.append(pieceCoordinate)
                move.append(self.nextCoordinate(NORTHWEST, pieceCoordinate))
                moveSet.append(move)
                move = []

            if self.canMoveDirection(NORTHEAST, pieceCoordinate):
                move.append(pieceCoordinate)
                move.append(self.nextCoordinate(NORTHEAST, pieceCoordinate))
                moveSet.append(move)
                move = []

        if not king and self.playerTurn is RED:
            if self.canMoveDirection(SOUTHWEST, pieceCoordinate):
                move.append(pieceCoordinate)
                move.append(self.nextCoordinate(SOUTHWEST, pieceCoordinate))
                moveSet.append(move)
                move = []

            if self.canMoveDirection(SOUTHEAST, pieceCoordinate):
                move.append(pieceCoordinate)
                move.append(self.nextCoordinate(SOUTHEAST, pieceCoordinate))
                moveSet.append(move)
                move = []

        if king:
            move.append(pieceCoordinate)
            aux = copy.deepcopy(pieceCoordinate)
            while self.canMoveDirection(NORTHWEST, aux):
                aux = self.nextCoordinate(NORTHWEST, aux)
                move.append(aux)
            moveSet.append(move)
            move = []

            move.append(pieceCoordinate)
            aux = copy.deepcopy(pieceCoordinate)
            while self.canMoveDirection(NORTHEAST, aux):
                aux = self.nextCoordinate(NORTHEAST, aux)
                move.append(aux)
            moveSet.append(move)
            move = []

            move.append(pieceCoordinate)
            aux = copy.deepcopy(pieceCoordinate)
            while self.canMoveDirection(SOUTHWEST, aux):
                aux = self.nextCoordinate(SOUTHWEST, aux)
                move.append(aux)
            moveSet.append(move)
            move = []

            move.append(pieceCoordinate)
            aux = copy.deepcopy(pieceCoordinate)
            while self.canMoveDirection(SOUTHEAST, aux):
                aux = self.nextCoordinate(SOUTHEAST, aux)
                move.append(aux)
            moveSet.append(move)
            move = []

        return moveSet

    def getJumpsByPiece(self, move, previous, king):
        if not move:
            return

        refSquare = move[-1]
        moveQueue = []
        finalMoveSet = []

        if previous[0].x == refSquare.x and previous[0].y == refSquare.y:#Primeiro caso, quando não existe anterior
            if self.canJumpDirection(NORTHWEST, refSquare):
                moveCopy = copy.deepcopy(move)
                moveCopy.append(self.nextCoordinate(NORTHWEST, refSquare))
                moveCopy.append(self.afterNextCoordinate(NORTHWEST, refSquare))
                #finalMoveSet.append(moveCopy)
                moveQueue.append(moveCopy)
            elif not self.canJumpDirection(NORTHWEST, refSquare):
                finalMoveSet.append(move)

            if self.canJumpDirection(NORTHEAST, refSquare):
                moveCopy = copy.deepcopy(move)
                moveCopy.append(self.nextCoordinate(NORTHEAST, refSquare))
                moveCopy.append(self.afterNextCoordinate(NORTHEAST, refSquare))
                # finalMoveSet.append(moveCopy)
                moveQueue.append(moveCopy)
            elif not self.canJumpDirection(NORTHWEST, refSquare):
                finalMoveSet.append(move)

            if self.canJumpDirection(SOUTHWEST, refSquare):
                moveCopy = copy.deepcopy(move)
                moveCopy.append(self.nextCoordinate(SOUTHWEST, refSquare))
                moveCopy.append(self.afterNextCoordinate(SOUTHWEST, refSquare))
                # finalMoveSet.append(moveCopy)
                moveQueue.append(moveCopy)
            elif not self.canJumpDirection(NORTHWEST, refSquare):
                finalMoveSet.append(move)

            if self.canJumpDirection(SOUTHEAST, refSquare):
                moveCopy = copy.deepcopy(move)
                moveCopy.append(self.nextCoordinate(SOUTHEAST, refSquare))
                moveCopy.append(self.afterNextCoordinate(SOUTHEAST, refSquare))
                # finalMoveSet.append(moveCopy)
                moveQueue.append(moveCopy)
            elif not self.canJumpDirection(NORTHWEST, refSquare):
                finalMoveSet.append(move)

        elif previous[0].x > refSquare.x:
            if previous[0].y > refSquare.y:
                if self.canJumpDirection(NORTHWEST, refSquare):
                    moveCopy = copy.deepcopy(move)
                    moveCopy.append(self.nextCoordinate(NORTHWEST, refSquare))
                    moveCopy.append(self.afterNextCoordinate(NORTHWEST, refSquare))
                    # finalMoveSet.append(moveCopy)
                    moveQueue.append(moveCopy)
                    """elif not self.canJumpDirection(NORTHWEST, refSquare):"""
                else:
                    finalMoveSet.append(move)

            else:
                if self.canJumpDirection(SOUTHWEST, refSquare):
                    moveCopy = copy.deepcopy(move)
                    moveCopy.append(self.nextCoordinate(SOUTHWEST, refSquare))
                    moveCopy.append(self.afterNextCoordinate(SOUTHWEST, refSquare))
                    # finalMoveSet.append(moveCopy)
                    moveQueue.append(moveCopy)
                    """elif not self.canJumpDirection(NORTHWEST, refSquare):"""
                else:
                    finalMoveSet.append(move)

        else:
            if previous[0].y > refSquare.y:
                if self.canJumpDirection(NORTHEAST, refSquare):
                    moveCopy = copy.deepcopy(move)
                    moveCopy.append(self.nextCoordinate(NORTHEAST, refSquare))
                    moveCopy.append(self.afterNextCoordinate(NORTHEAST, refSquare))
                    # finalMoveSet.append(moveCopy)
                    moveQueue.append(moveCopy)
                    """elif not self.canJumpDirection(NORTHWEST, refSquare):"""
                else:
                    finalMoveSet.append(move)

            else:
                if self.canJumpDirection(SOUTHEAST, refSquare):
                    moveCopy = copy.deepcopy(move)
                    moveCopy.append(self.nextCoordinate(SOUTHEAST, refSquare))
                    moveCopy.append(self.afterNextCoordinate(SOUTHEAST, refSquare))
                    # finalMoveSet.append(moveCopy)
                    moveQueue.append(moveCopy)
                    """elif not self.canJumpDirection(NORTHWEST, refSquare):"""
                else:
                    finalMoveSet.append(move)


        """if self.canJumpDirection(NORTHWEST, refSquare):
            moveCopy = copy.deepcopy(move)
            moveCopy.append(self.nextCoordinate(NORTHWEST, refSquare))
            moveCopy.append(self.afterNextCoordinate(NORTHWEST, refSquare))
            #finalMoveSet.append(moveCopy)
            moveQueue.append(moveCopy)
        elif not self.canJumpDirection(NORTHWEST, refSquare):
            finalMoveSet.append(move)

        if self.canJumpDirection(NORTHEAST, refSquare):
            moveCopy = copy.deepcopy(move)
            moveCopy.append(self.nextCoordinate(NORTHEAST, refSquare))
            moveCopy.append(self.afterNextCoordinate(NORTHEAST, refSquare))
            # finalMoveSet.append(moveCopy)
            moveQueue.append(moveCopy)
        elif not self.canJumpDirection(NORTHWEST, refSquare):
            finalMoveSet.append(move)

        if self.canJumpDirection(SOUTHWEST, refSquare):
            moveCopy = copy.deepcopy(move)
            moveCopy.append(self.nextCoordinate(SOUTHWEST, refSquare))
            moveCopy.append(self.afterNextCoordinate(SOUTHWEST, refSquare))
            # finalMoveSet.append(moveCopy)
            moveQueue.append(moveCopy)
        elif not self.canJumpDirection(NORTHWEST, refSquare):
            finalMoveSet.append(move)

        if self.canJumpDirection(SOUTHEAST, refSquare):
            moveCopy = copy.deepcopy(move)
            moveCopy.append(self.nextCoordinate(SOUTHEAST, refSquare))
            moveCopy.append(self.afterNextCoordinate(SOUTHEAST, refSquare))
            # finalMoveSet.append(moveCopy)
            moveQueue.append(moveCopy)
        elif not self.canJumpDirection(NORTHWEST, refSquare):
            finalMoveSet.append(move)"""


        while moveQueue:
            print("\n\nTINHA QUE COMER")
            move = moveQueue.pop()
            refSquare = move[-1]
            print("\n\n",refSquare.x, refSquare.y)
            previous = move[-2]
            print("\n\n",previous.x, previous.y)
            next = refSquare
            DIRECTION = self.getDirection(previous, refSquare)
            print("\n\n"+DIRECTION+"\n\n")
            expanded = False
            # while self.canMoveDirection(DIRECTION, refSquare):

            if self.canJumpDirection(DIRECTION, refSquare):
                expanded = True
                auxCopy = copy.deepcopy(move)
                auxCopy += [self.nextCoordinate(DIRECTION, refSquare)]
                auxCopy += [self.afterNextCoordinate(DIRECTION, refSquare)]
                if self.canJumpAdjacent(auxCopy[-1]):
                    moveQueue.append(auxCopy)
                else:
                    finalMoveSet.append(auxCopy)

            if not expanded:
                finalMoveSet.append(move)

        return finalMoveSet


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
        """print("previous", previous,"refSquare", refSquare)
        aux = self.nextCoordinate(NORTHWEST, refSquare)
        print("aux", aux)
        if aux.x == previous.x and aux.y == previous.y:
            return NORTHWEST
        aux = self.nextCoordinate(NORTHEAST, refSquare)
        if aux.x == previous.x and aux.y == previous.y:
            return NORTHEAST
        aux = self.nextCoordinate(SOUTHWEST, refSquare)
        if aux.x == previous.x and aux.y == previous.y:
            return SOUTHWEST
        aux = self.nextCoordinate(SOUTHEAST, refSquare)
        if aux.x == previous.x and aux.y == previous.y:
            return SOUTHEAST"""

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
                    for move in self.getLegalMovesByPiece(coordinate, self.location(coordinate).occupant.king):
                        if move and move not in legalMoveSet:
                            legalMoveSet.append(move)

        print("getLegalMoves - legalMoveSet ", legalMoveSet)
        return legalMoveSet

    """--------------------------+
    |  Single Piece Moves Logic  |
    +--------------------------"""

    def getLegalMovesByPiece(self, pieceCoordinate, king=False):
        """
        Look for all possible movements recursively and return a list of possible moves
        """
        pieceFinalLegalMoves = []

        # Get piece moves without jump
        legalMoveSet = self.getRegularMovesByPiece(pieceCoordinate, king)

        # Extend jumps
        c = -1
        previous = legalMoveSet[0]
        for pieceMove in legalMoveSet:
            if c > -1:
                previous = legalMoveSet[c]
            c = c + 1
            returnMoves = self.getJumpsByPiece(pieceMove, previous, king)
            print("returnMoves", returnMoves)
            for returnMove in returnMoves:
                if returnMove not in pieceFinalLegalMoves:
                    pieceFinalLegalMoves.append(returnMove)

        print("pieceFinalLegalMoves", pieceFinalLegalMoves)

        return pieceFinalLegalMoves

    def getBestMoves(self, legalMoveSet, king):

        copyLegalMoves = copy.deepcopy(legalMoveSet)
        legalMoveSet = []

        for move in copyLegalMoves:
            if self.moveContainsCoordinate(self.selectedPieceCoordinate, move) and move not in legalMoveSet:
                legalMoveSet.append(move)

        return legalMoveSet

    def filterNoneOrEmptyMoves(self, moves):

        if not moves:
            return []

        moves = [x for x in moves if x]

        for move in moves:
            if None in move or [] in move:
                move.pop()

        return moves

    def exists(self):
        return self is not None

    def removePiecesByMove(self, move):
        """
        Removes enemy pieces from a move (x,y).
        """
        for coordinate in move:
            if self.location(coordinate).occupant:
                if self.location(coordinate).occupant.color is not self.playerTurn:
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
        self.verifyDrawCondition()

    def executeMove(self):
        print("self.selectedPieceMoves", self.selectedPieceMoves)
        if self.selectedPieceMoves is None:
            return False
        for move in self.selectedPieceMoves:
            for coord in move:
                if self.location(coord) == self.location(self.mouseClick):
                    self.movePiece(self.selectedPieceCoordinate, self.mouseClick)
                    self.removePiecesByMove(move)
                    return True
        return False

    def verifyWinCondition(self):
        self.isPlayerRedLost = True
        self.isPlayerWhiteLost = True
        for x in range(8):
            for y in range(8):
                if self.matrix[x][y].occupant is not None and self.matrix[x][y].occupant.color is RED:
                   self.isPlayerRedLost = False
                elif self.matrix[x][y].occupant is not None and self.matrix[x][y].occupant.color is WHITE:
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
                if self.matrix[x][y].occupant is not None and self.matrix[x][y].occupant.king \
                        and self.matrix[x][y].occupant.color is WHITE:
                    if self.kingWhiteCounterAux == 0:
                        self.kingWhiteCounterAux = 1
                    self.kingWhiteCounter = self.kingWhiteCounter + 1
                elif self.matrix[x][y].occupant is not None and self.matrix[x][y].occupant.king \
                        and self.matrix[x][y].occupant.color is RED:
                    if self.kingRedCounterAux == 0:
                        self.kingRedCounterAux = 1
                    self.kingRedCounter = self.kingRedCounter + 1
                elif self.matrix[x][y].occupant is not None and self.matrix[x][y].occupant.color is WHITE:
                    self.whiteCounter = self.whiteCounter + 1
                elif self.matrix[x][y].occupant is not None and self.matrix[x][y].occupant.color is RED:
                    self.redCounter = self.redCounter + 1

        'Draw conditions'

        if (self.kingWhiteCounterAux != self.kingWhiteCounter or self.kingRedCounterAux != self.kingRedCounter) and \
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
        elif (self.kingWhiteCounterAux == self.kingWhiteCounter and self.kingWhiteCounter == 2 and
                self.kingRedCounterAux == self.kingRedCounter and self.kingRedCounter == 1 and
                self.redCounterAux == self.redCounter and self.redCounter == 1 and self.whiteCounterAux == 0) or \
            (self.kingRedCounterAux == self.kingRedCounter and self.kingRedCounterAux == 2 and
                self.kingWhiteCounterAux == self.kingWhiteCounter and self.kingWhiteCounter == 1 and
                self.whiteCounterAux == self.whiteCounter and self.whiteCounter == 1 and self.redCounterAux == 0) or \
            (self.kingWhiteCounterAux == self.kingWhiteCounter and self.kingWhiteCounter == 1 and
                self.kingRedCounterAux == self.kingRedCounter and self.kingRedCounter == 1 and
                self.redCounterAux == self.redCounter and self.redCounter == 1 and self.whiteCounterAux == 0) or \
            (self.kingRedCounterAux == self.kingRedCounter and self.kingRedCounterAux == 1 and
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

    def highlightLegalMoves(self, screen, goldPiece):
        if self.selectedPieceCoordinate is not None and self.selectedPieceMoves is not None:

            for movePath in self.selectedPieceMoves:
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
