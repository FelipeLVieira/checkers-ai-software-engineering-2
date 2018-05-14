import pygame

from Constants import *


class Board:
    def __init__(self, board=None):
        # This allows us to make a copy of the board for the AI to safely
        # recurse on.
        if board is Board:
            self.matrix = board.matrix
        self.matrix = self.newBoard()

        self.selectedLegalMoves = None
        self.selectedPieceCoordinate = None
        self.turn = None

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

        return [self.nextCoordinate(NORTHWEST, (coordinate.x, coordinate.y)),
                self.nextCoordinate(NORTHEAST, (coordinate.x, coordinate.y)),
                self.nextCoordinate(SOUTHWEST, (coordinate.x, coordinate.y)),
                self.nextCoordinate(SOUTHEAST, (coordinate.x, coordinate.y))]

    def location(self, coordinate):
        """
        Takes a set of coordinates as arguments and returns self.matrix[x][y]
        This can be faster than writing something like self.matrix[coords[0]][coords[1]]
        """
        if coordinate is None:
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

    def canMoveOrJumpCount(self, playerTurn, currentCoordinate, jump, previous, move, king):
        """
        Count the number of adjacent possible movements
        """

        possibleJumpsCount = 0

        if move is None:
            return 0

        # Checks for all directions if a piece can jump an enemy given a coordinate
        if self.onBoard(self.nextCoordinate(NORTHWEST, currentCoordinate)) \
                and self.onBoard(self.afterNextCoordinate(NORTHWEST, currentCoordinate)) \
                and self.location(self.nextCoordinate(NORTHWEST, currentCoordinate)).occupant is not None \
                and self.location(self.afterNextCoordinate(NORTHWEST, currentCoordinate)).occupant is None \
                and self.afterNextCoordinate(NORTHWEST, currentCoordinate) is not previous \
                and not self.moveContainsCoordinate(self.afterNextCoordinate(NORTHWEST, currentCoordinate), move) \
                and playerTurn is not self.location(
            self.nextCoordinate(NORTHWEST, currentCoordinate)).occupant.color:
            possibleJumpsCount += 1

        if self.onBoard(self.nextCoordinate(NORTHEAST, currentCoordinate)) \
                and self.onBoard(self.afterNextCoordinate(NORTHEAST, currentCoordinate)) \
                and self.location(self.nextCoordinate(NORTHEAST, currentCoordinate)).occupant is not None \
                and self.location(self.afterNextCoordinate(NORTHEAST, currentCoordinate)).occupant is None \
                and self.afterNextCoordinate(NORTHEAST, currentCoordinate) is not previous \
                and not self.moveContainsCoordinate(self.afterNextCoordinate(NORTHEAST, currentCoordinate), move) \
                and playerTurn is not self.location(
            self.nextCoordinate(NORTHEAST, currentCoordinate)).occupant.color:
            possibleJumpsCount += 1

        if self.onBoard(self.nextCoordinate(SOUTHWEST, currentCoordinate)) \
                and self.onBoard(self.afterNextCoordinate(SOUTHWEST, currentCoordinate)) \
                and self.location(self.nextCoordinate(SOUTHWEST, currentCoordinate)).occupant is not None \
                and self.location(self.afterNextCoordinate(SOUTHWEST, currentCoordinate)).occupant is None \
                and self.afterNextCoordinate(SOUTHWEST, currentCoordinate) is not previous \
                and not self.moveContainsCoordinate(self.afterNextCoordinate(SOUTHWEST, currentCoordinate), move) \
                and playerTurn is not self.location(
            self.nextCoordinate(SOUTHWEST, currentCoordinate)).occupant.color:
            possibleJumpsCount += 1

        if self.onBoard(self.nextCoordinate(SOUTHEAST, currentCoordinate)) \
                and self.onBoard(self.afterNextCoordinate(SOUTHEAST, currentCoordinate)) \
                and self.location(self.nextCoordinate(SOUTHEAST, currentCoordinate)).occupant is not None \
                and self.location(self.afterNextCoordinate(SOUTHEAST, currentCoordinate)).occupant is None \
                and self.afterNextCoordinate(SOUTHEAST, currentCoordinate) is not previous \
                and not self.moveContainsCoordinate(self.afterNextCoordinate(SOUTHEAST, currentCoordinate), move) \
                and playerTurn is not self.location(
            self.nextCoordinate(SOUTHEAST, currentCoordinate)).occupant.color:
            possibleJumpsCount += 1

        # Check if the piece never jumped before
        if not jump and possibleJumpsCount == 0:
            if playerTurn is WHITE or king:
                # Check if there is a empty square to move forward
                if self.onBoard(self.nextCoordinate(NORTHWEST, currentCoordinate)):
                    if self.location(self.nextCoordinate(NORTHWEST, currentCoordinate)).occupant is None:
                        possibleJumpsCount += 1
                if self.onBoard(self.nextCoordinate(NORTHEAST, currentCoordinate)):
                    if self.location(self.nextCoordinate(NORTHEAST, currentCoordinate)).occupant is None:
                        possibleJumpsCount += 1
            if playerTurn is RED or king:
                if self.onBoard(self.nextCoordinate(SOUTHWEST, currentCoordinate)):
                    if self.location(self.nextCoordinate(SOUTHWEST, currentCoordinate)).occupant is None:
                        possibleJumpsCount += 1
                if self.onBoard(self.nextCoordinate(SOUTHEAST, currentCoordinate)):
                    if self.location(self.nextCoordinate(SOUTHEAST, currentCoordinate)).occupant is None:
                        possibleJumpsCount += 1

        return possibleJumpsCount

    def canMoveDirection(self, currentCoordinate, DIRECTION):
        if self.onBoard(self.nextCoordinate(DIRECTION, currentCoordinate)):
            if self.location(self.nextCoordinate(DIRECTION, currentCoordinate)).occupant is None:
                return True
            else:
                return False

    def canJumpDirection(self, coordinate, playerTurn, DIRECTION, previous, move):
        """
            Given a coordinate, color, direction and a list of moves, checks if there's another available jump
        """

        if self.onBoard(self.nextCoordinate(DIRECTION, coordinate)) \
                and self.onBoard(self.afterNextCoordinate(DIRECTION, coordinate)) \
                and self.location(self.nextCoordinate(DIRECTION, coordinate)).occupant is not None \
                and self.location(self.afterNextCoordinate(DIRECTION, coordinate)).occupant is None \
                and self.afterNextCoordinate(DIRECTION, coordinate) is not previous \
                and not self.moveContainsCoordinate(self.afterNextCoordinate(DIRECTION, coordinate), move) \
                and playerTurn is not self.location(self.nextCoordinate(DIRECTION, coordinate)).occupant.color:
            return True
            # If after a repeated coordinate there still exists an enemy piece to jump over
        elif self.onBoard(self.nextCoordinate(DIRECTION, coordinate)) \
                and self.onBoard(self.afterNextCoordinate(DIRECTION, coordinate)) \
                and self.location(self.nextCoordinate(DIRECTION, coordinate)).occupant is not None \
                and self.location(self.afterNextCoordinate(DIRECTION, coordinate)).occupant is None \
                and self.afterNextCoordinate(DIRECTION, coordinate) is not previous \
                and not self.moveContainsCoordinate(self.afterNextCoordinate(DIRECTION, coordinate), move) \
                and playerTurn is not self.location(self.nextCoordinate(DIRECTION, coordinate)).occupant.color \
                and self.onBoard(self.nextCoordinate(DIRECTION, self.afterNextCoordinate(DIRECTION, coordinate))) \
                and self.location(
            self.nextCoordinate(DIRECTION, self.afterNextCoordinate(DIRECTION, coordinate))).occupant is not None \
                and self.onBoard(
            self.afterNextCoordinate(DIRECTION, self.afterNextCoordinate(DIRECTION, coordinate))) \
                and playerTurn is not self.location(
            self.nextCoordinate(DIRECTION, self.afterNextCoordinate(DIRECTION, coordinate))).occupant.color:
            return True

        return False

    def kingInitialLegalMove(self, currentCoordinate, auxCoordinateList, playerTurn, DIRECTION):
        if auxCoordinateList:
            auxCoordinateList = [currentCoordinate]
            nextCoord = currentCoordinate
            while self.canMoveDirection(auxCoordinateList[-1], DIRECTION):
                auxCoordinateList += [self.nextCoordinate(DIRECTION, nextCoord)]
                if not self.canMoveDirection(auxCoordinateList[-1], DIRECTION):
                    break
                else:
                    nextCoord = self.nextCoordinate(DIRECTION, nextCoord)

                # Checks if didn't enter inside while (it can't move except for jump pieces
                if not auxCoordinateList[0] == nextCoord:
                    # Can still jump after few cells move?
                    if self.canJumpDirection(auxCoordinateList[-1], playerTurn, DIRECTION, None,
                                             auxCoordinateList):
                        # Add the jump coordinates
                        auxCoordinateList += [self.nextCoordinate(DIRECTION, auxCoordinateList[-1])]
                        auxCoordinateList += [self.afterNextCoordinate(DIRECTION, currentCoordinate)]

        # After verify if the variable nextCoord didn't get new moves, verify if it can jump an adjacent piece
        if not auxCoordinateList and self.canJumpDirection(currentCoordinate, playerTurn, DIRECTION, None,
                                                           auxCoordinateList):
            auxCoordinateList = [self.nextCoordinate(DIRECTION, currentCoordinate)]
            auxCoordinateList += [self.afterNextCoordinate(DIRECTION, currentCoordinate)]

        return auxCoordinateList

    """-------------------+
    |  Piece Moves Logic  |
    +-------------------"""

    def legalMoves(self, playerTurn, currentCoordinate, jump=False,
                   previous=None, move=[], king=False):
        """
        Look for all possible movements recursively and return a list of possible moves
        """

        legalMoves = []

        if not jump:

            """---------------+
            |   First Call    |
            +---------------"""

            auxNorthwestmove = []
            auxNortheastmove = []
            auxSouthwestmove = []
            auxSoutheastmove = []

            if playerTurn is WHITE or king:
                # Check if there is a empty square to move forward
                if self.canMoveDirection(currentCoordinate, NORTHWEST):
                    if king:
                        auxNorthwestmove = [self.nextCoordinate(NORTHWEST, currentCoordinate)]
                    else:
                        legalMoves.append([self.nextCoordinate(NORTHWEST, currentCoordinate)])

                if self.canMoveDirection(currentCoordinate, NORTHEAST):
                    if king:
                        auxNortheastmove = [self.nextCoordinate(NORTHEAST, currentCoordinate)]
                    else:
                        legalMoves.append([self.nextCoordinate(NORTHEAST, currentCoordinate)])

            if playerTurn is RED or king:

                if self.canMoveDirection(currentCoordinate, SOUTHWEST):
                    if king:
                        auxSouthwestmove = [self.nextCoordinate(SOUTHWEST, currentCoordinate)]
                    else:
                        legalMoves.append([self.nextCoordinate(SOUTHWEST, currentCoordinate)])

                if self.canMoveDirection(currentCoordinate, SOUTHEAST):
                    if king:
                        auxSoutheastmove = [self.nextCoordinate(SOUTHEAST, currentCoordinate)]
                    else:
                        legalMoves.append([self.nextCoordinate(SOUTHEAST, currentCoordinate)])

            # Build kings path and also checks if king can jump
            if king:

                """ ---------------------------
                |   King initial legal move   |
                ----------------------------"""
                # NW

                # Checks if the path is free to move and will stop at the first piece or end of board
                auxNorthwestmove = self.kingInitialLegalMove(currentCoordinate, auxNorthwestmove, playerTurn, NORTHWEST)

                # Call recursivity to check for more jumps
                if auxNorthwestmove:
                    legalMoves.append(self.legalMoves(playerTurn, auxNorthwestmove[-1],
                                                      True, auxNorthwestmove[-1], auxNorthwestmove, king))

                """---------------------------------------------------------------------------------"""

                # NE

                auxNortheastmove = self.kingInitialLegalMove(currentCoordinate, auxNortheastmove, playerTurn, NORTHEAST)

                if auxNortheastmove:
                    legalMoves.append(self.legalMoves(playerTurn, auxNortheastmove[-1],
                                                      True, auxNortheastmove[-1], auxNortheastmove, king))

                """---------------------------------------------------------------------------------"""

                # SW

                auxSouthwestmove = self.kingInitialLegalMove(currentCoordinate, auxSouthwestmove, playerTurn, SOUTHWEST)

                if auxSouthwestmove:
                    legalMoves.append(self.legalMoves(playerTurn, auxSouthwestmove[-1],
                                                      True, auxSouthwestmove[-1], auxSouthwestmove, king))

                """---------------------------------------------------------------------------------"""

                # SE

                auxSoutheastmove = self.kingInitialLegalMove(currentCoordinate, auxSoutheastmove, playerTurn, SOUTHEAST)

                if auxSoutheastmove:
                    legalMoves.append(self.legalMoves(playerTurn, auxSoutheastmove[-1],
                                                      True, auxSoutheastmove[-1], auxSoutheastmove, king))

            if not king:
                # Check where to jump over and call recursive for that direction

                # NW
                if self.canJumpDirection(currentCoordinate, playerTurn, NORTHWEST, previous, move):
                    move = [self.nextCoordinate(NORTHWEST, currentCoordinate)]
                    move += [self.afterNextCoordinate(NORTHWEST, currentCoordinate)]
                    legalMoves.append(
                        self.legalMoves(playerTurn, self.afterNextCoordinate(NORTHWEST, currentCoordinate),
                                        True, currentCoordinate, move, king))

                # NE
                if self.canJumpDirection(currentCoordinate, playerTurn, NORTHEAST, previous, move):
                    move = [self.nextCoordinate(NORTHEAST, currentCoordinate)]
                    move += [self.afterNextCoordinate(NORTHEAST, currentCoordinate)]
                    legalMoves.append(
                        self.legalMoves(playerTurn, self.afterNextCoordinate(NORTHEAST, currentCoordinate),
                                        True, currentCoordinate, move, king))

                # SW
                if self.canJumpDirection(currentCoordinate, playerTurn, SOUTHWEST, previous, move):
                    move = [self.nextCoordinate(SOUTHWEST, currentCoordinate)]
                    move += [self.afterNextCoordinate(SOUTHWEST, currentCoordinate)]
                    legalMoves.append(
                        self.legalMoves(playerTurn, self.afterNextCoordinate(SOUTHWEST, currentCoordinate),
                                        True, currentCoordinate, move, king))

                # SE
                if self.canJumpDirection(currentCoordinate, playerTurn, SOUTHEAST, previous, move):
                    move = [self.nextCoordinate(SOUTHEAST, currentCoordinate)]
                    move += [self.afterNextCoordinate(SOUTHEAST, currentCoordinate)]
                    legalMoves.append(
                        self.legalMoves(playerTurn, self.afterNextCoordinate(SOUTHEAST, currentCoordinate),
                                        True, currentCoordinate, move, king))

        # Jumped at least once already
        # LegalMoves is temporally a simple array when enters here
        if jump:

            auxNorthwestmove = []
            auxNortheastmove = []
            auxSouthwestmove = []
            auxSoutheastmove = []

            if self.canJumpDirection(currentCoordinate, playerTurn, NORTHWEST, previous, move):
                auxNorthwestmove = move
                auxNorthwestmove += [self.nextCoordinate(NORTHWEST, currentCoordinate)]
                auxNorthwestmove += [self.afterNextCoordinate(NORTHWEST, currentCoordinate)]
                auxNorthwestmove = self.legalMoves(playerTurn, self.afterNextCoordinate(NORTHWEST, currentCoordinate),
                                                   True, currentCoordinate, auxNorthwestmove, king)
                print("aux NORTHWEST", auxNorthwestmove)

            if self.canJumpDirection(currentCoordinate, playerTurn, NORTHEAST, previous, move):
                auxNortheastmove = move
                auxNortheastmove += [self.nextCoordinate(NORTHEAST, currentCoordinate)]
                auxNortheastmove += [self.afterNextCoordinate(NORTHEAST, currentCoordinate)]
                auxNortheastmove = self.legalMoves(playerTurn, self.afterNextCoordinate(NORTHEAST, currentCoordinate),
                                                   True, currentCoordinate, auxNortheastmove, king)
                print("aux NORTHEAST", auxNortheastmove)

            if self.canJumpDirection(currentCoordinate, playerTurn, SOUTHWEST, previous, move):
                auxSouthwestmove = move
                auxSouthwestmove += [self.nextCoordinate(SOUTHWEST, currentCoordinate)]
                auxSouthwestmove += [self.afterNextCoordinate(SOUTHWEST, currentCoordinate)]
                auxSouthwestmove = self.legalMoves(playerTurn, self.afterNextCoordinate(SOUTHWEST, currentCoordinate),
                                                   True, currentCoordinate, auxSouthwestmove, king)
                print("aux SOUTHWEST", auxSouthwestmove)

            if self.canJumpDirection(currentCoordinate, playerTurn, SOUTHEAST, previous, move):
                auxSoutheastmove = move
                auxSoutheastmove += [self.nextCoordinate(SOUTHEAST, currentCoordinate)]
                auxSoutheastmove += [self.afterNextCoordinate(SOUTHEAST, currentCoordinate)]
                auxSoutheastmove = self.legalMoves(playerTurn, self.afterNextCoordinate(SOUTHEAST, currentCoordinate),
                                                   True, currentCoordinate, auxSoutheastmove, king)
                print("aux SOUTHEAST", auxSoutheastmove)

        print("legalMoves ", legalMoves)

        legalMoves = self.filterMoves(legalMoves)

        if not legalMoves:
            return move
        else:
            return legalMoves

    def getLongestMoves(self, legalMoves, king):

        """
        Given a list of possible moves, filter the largest.
        If draw, return all with the same size of the first largest move found
        """

        longestMoves = []

        if legalMoves is None:
            return

        longest = []
        for move in legalMoves:
            if len(move) > len(longest):
                longest = move

        longestLegalMoves = []

        for move in legalMoves:
            if len(longest) == len(move):
                longestLegalMoves.append(move)

        return longestLegalMoves

    def filterMoves(self, moves):

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

    def executeMove(self, selectedSquareCoordinate):
        for movepath in self.selectedLegalMoves:
            for idx, coordinate in enumerate(movepath):
                if coordinate is not None:
                    # Check if the selected position is the position that jumps over all possible pieces
                    if coordinate.x == selectedSquareCoordinate.x and coordinate.y == selectedSquareCoordinate.y and coordinate is \
                            movepath[-1]:
                        self.movePiece(self.selectedPieceCoordinate, selectedSquareCoordinate)
                        self.removePiecesByMove(movepath, self.turn)

                    # If the piece jump in a position smaller the farest square of the move
                    elif coordinate.x == selectedSquareCoordinate.x and coordinate.y == selectedSquareCoordinate.y and coordinate is not \
                            movepath[-1] and self.location(
                        self.selectedPieceCoordinate).occupant.king:
                        auxMove = movepath[:idx]
                        self.movePiece(self.selectedPieceCoordinate, selectedSquareCoordinate)
                        self.removePiecesByMove(auxMove, self.turn)

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
