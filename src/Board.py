from Constants import *


class Board:
    def __init__(self):
        self.matrix = self.newBoard()

    def newBoard(self):

        # initialize squares and place them in matrix

        matrix = [[None] * 8 for i in range(8)]

        # The following code block has been adapted from
        # http://itgirl.dreamhosters.com/itgirlgames/games/Program%20Leaders/ClareR/Checkers/checkers.py
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
                    matrix[x][y].occupant = Piece(RED)
            for y in range(5, 8):
                if matrix[x][y].color == BLACK:
                    matrix[x][y].occupant = Piece(WHITE)

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

    def rel(self, dir, coordinate):
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

    def adjacent(self, coordinate):
        """
        Returns a list of squares locations that are adjacent (on a diagonal) to (x,y).
        """

        return [self.rel(NORTHWEST, (coordinate.x, coordinate.y)), self.rel(NORTHEAST, (coordinate.x, coordinate.y)),
                self.rel(SOUTHWEST, (coordinate.x, coordinate.y)),
                self.rel(SOUTHEAST, (coordinate.x, coordinate.y))]

    def location(self, coordinate):
        """
        Takes a set of coordinates as arguments and returns self.matrix[x][y]
        This can be faster than writing something like self.matrix[coords[0]][coords[1]]
        """
        if coordinate is None:
            return

        return self.matrix[coordinate.x][coordinate.y]

    def blindLegalMoves(self, coordinate):
        """
        Returns a list of blind legal move locations from a set of coordinates (x,y) on the board.
        If that location is empty, then blind_legal_moves() return an empty list.
        """

        blindLegalMoves = []

        if self.matrix[coordinate.x][coordinate.y].occupant is not None:

            if self.matrix[coordinate.x][coordinate.y].occupant.king is False \
                    and self.matrix[coordinate.x][coordinate.y].occupant.color is WHITE:
                if self.onBoard(self.rel(NORTHWEST, coordinate)):
                    blindLegalMoves.append(self.rel(NORTHWEST, coordinate))
                if self.onBoard( self.rel(NORTHEAST, coordinate)):
                    blindLegalMoves.append( self.rel(NORTHEAST, coordinate))

            elif self.matrix[coordinate.x][coordinate.y].occupant.king is False \
                    and self.matrix[coordinate.x][coordinate.y].occupant.color == RED:
                if self.onBoard(self.rel(SOUTHWEST, coordinate)):
                    blindLegalMoves.append(self.rel(SOUTHWEST, coordinate))
                if self.onBoard(self.rel(SOUTHEAST, coordinate)):
                    blindLegalMoves.append(self.rel(SOUTHEAST, coordinate))

            else:
                if self.onBoard(self.rel(NORTHWEST, coordinate)):
                    blindLegalMoves.append(self.rel(NORTHWEST, coordinate))
                if self.onBoard( self.rel(NORTHEAST, coordinate)):
                    blindLegalMoves.append( self.rel(NORTHEAST, coordinate))
                if self.onBoard(self.rel(SOUTHWEST, coordinate)):
                    blindLegalMoves.append(self.rel(SOUTHWEST, coordinate))
                if self.onBoard(self.rel(SOUTHEAST, coordinate)):
                    blindLegalMoves.append(self.rel(SOUTHEAST, coordinate))

        else:
            blindLegalMoves = []

        return blindLegalMoves

    def legalMoves(self, playerTurn, coordinate):
        """
        Returns a list of legal move locations from a given set of coordinates (x,y) on the board.
        If that location is empty, then legal_moves() returns an empty list.
        """

        blindLegalMoves = self.blindLegalMoves(coordinate)
        legalMoves = []

        if self.location(coordinate).occupant.king is False:
            for moveCoordinate in blindLegalMoves:
                if playerTurn is WHITE:
                    # Check if the two next squares are occupied
                    if self.location(moveCoordinate).occupant is not None \
                            and self.location(self.rel(NORTHWEST, moveCoordinate)).occupant is not None \
                            and self.location(self.rel(NORTHEAST, moveCoordinate)).occupant is not None:
                        # There's nowhere to jump or move
                        continue
                # RED turn
                else:
                    # Check if the two next squares are occupied
                    if self.location(moveCoordinate).occupant is not None \
                            and self.location(self.rel(SOUTHWEST, moveCoordinate)).occupant is not None \
                            and self.location(self.rel(SOUTHEAST, moveCoordinate)).occupant is not None:
                        # There's nowhere to jump or move
                        continue

            # There are spots to go
            legalMoves = self.checkNextLegalMove(playerTurn, [coordinate])
        else:
            # TODO king actions
            return legalMoves

        return legalMoves

    def checkNextLegalMove(self, playerTurn, moveCoordinates):

        blindMoves = self.blindLegalMoves(moveCoordinates[-1])
        legalMoves = []

        # Player WHITE
        if playerTurn is WHITE:
            for move in blindMoves:
                # Next square is empty, add move
                if self.location(move).occupant is None:
                    legalMoves.append([move])
                    continue
                # Next northwest square is occupied but after this one is empty
                if self.location(move).occupant is not None and \
                        self.location(self.rel(NORTHWEST, move)).occupant is None:
                    aux = [move, self.rel(NORTHWEST, move)]
                    legalMoves.append(aux)
                    continue
                # Next northeast square is occupied but after this one is empty
                if self.location(move).occupant is not None and \
                        self.location(self.rel(NORTHEAST, move)).occupant is None:
                    aux = [move, self.rel(NORTHEAST, move)]
                    legalMoves.append(aux)
                    continue
            # Call recursivity
            # self.checkNextLegalMove(playerTurn, moveCoordinates)
        else:
            for move in blindMoves:
                # Next square is empty, add move
                if self.location(move).occupant is None:
                    legalMoves.append([move])
                    continue
                # Next northwest square is occupied but after this one is empty
                if self.location(move).occupant is not None and \
                        self.location(self.rel(SOUTHWEST, move)).occupant is None:
                    aux = [move, self.rel(SOUTHWEST, move)]
                    legalMoves.append(aux)
                    continue
                # Next northeast square is occupied but after this one is empty
                if self.location(move).occupant is not None and \
                        self.location(self.rel(SOUTHEAST, move)).occupant is None:
                    aux = [move, self.rel(SOUTHEAST, move)]
                    legalMoves.append(aux)
                    continue
            # Call recursivity
            # self.checkNextLegalMove(playerTurn, moveCoordinates)
        return legalMoves

    def removePiece(self, coordinate):
        """
        Removes a piece from the board at position (x,y).
        """
        self.matrix[coordinate.x][coordinate.y].occupant = None

    def movePiece(self, startCoordinate, endCoordinate):
        """
        Move a piece from (start_x, start_y) to (end_x, end_y).
        """

        self.matrix[endCoordinate.x][endCoordinate.y].occupant = self.matrix[startCoordinate.x][
            startCoordinate.y].occupant
        self.removePiece(startCoordinate)

        # self.king(endCoordinate)

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
        if self.location(coordinate.x, coordinate.y).occupant != None:
            if (self.location(coordinate.x, coordinate.y).occupant.color == BLUE and coordinate.y == 0) or (
                    self.location(coordinate.x, coordinate.y).occupant.color == RED and coordinate.y == 7):
                self.location(coordinate.x, coordinate.y).occupant.king = True


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
