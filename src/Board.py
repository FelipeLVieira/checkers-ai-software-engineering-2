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

    def relIncrement(self, dir, coordinate):
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

    def canMoveOrJumpCount(self, playerTurn, selectedSquareCoordinate, jump, king):

        canMoveorJump = 0

        # Otherwise, any piece can be checked if it's able to jump an enemy
        if self.onBoard(self.rel(NORTHWEST, selectedSquareCoordinate)) \
                and self.onBoard(self.relIncrement(NORTHWEST, selectedSquareCoordinate)) \
                and self.location(self.rel(NORTHWEST, selectedSquareCoordinate)).occupant is not None \
                and self.location(self.relIncrement(NORTHWEST, selectedSquareCoordinate)).occupant is None \
                and playerTurn is not self.location(self.rel(NORTHWEST, selectedSquareCoordinate)).occupant.color:
            canMoveorJump += 1

        if self.onBoard(self.rel(NORTHEAST, selectedSquareCoordinate)) \
                and self.onBoard(self.relIncrement(NORTHEAST, selectedSquareCoordinate)) \
                and self.location(self.rel(NORTHEAST, selectedSquareCoordinate)).occupant is not None \
                and self.location(self.relIncrement(NORTHEAST, selectedSquareCoordinate)).occupant is None \
                and playerTurn is not self.location(self.rel(NORTHEAST, selectedSquareCoordinate)).occupant.color:
            canMoveorJump += 1

        if self.onBoard(self.rel(SOUTHWEST, selectedSquareCoordinate)) \
                and self.onBoard(self.relIncrement(SOUTHWEST, selectedSquareCoordinate)) \
                and self.location(self.rel(SOUTHWEST, selectedSquareCoordinate)).occupant is not None \
                and self.location(self.relIncrement(SOUTHWEST, selectedSquareCoordinate)).occupant is None \
                and playerTurn is not self.location(self.rel(SOUTHWEST, selectedSquareCoordinate)).occupant.color:
            canMoveorJump += 1

        if self.onBoard(self.rel(SOUTHEAST, selectedSquareCoordinate)) \
                and self.onBoard(self.relIncrement(SOUTHEAST, selectedSquareCoordinate)) \
                and self.location(self.rel(SOUTHEAST, selectedSquareCoordinate)).occupant is not None \
                and self.location(self.relIncrement(SOUTHEAST, selectedSquareCoordinate)).occupant is None \
                and playerTurn is not self.location(self.rel(SOUTHEAST, selectedSquareCoordinate)).occupant.color:
            canMoveorJump += 1

        # Check if the piece never jumped before
        if not jump and canMoveorJump == 0:
            if playerTurn is WHITE or king is True:
                # Check if there is a empty square to move forward
                if self.onBoard(self.rel(NORTHWEST, selectedSquareCoordinate)):
                    if self.location(self.rel(NORTHWEST, selectedSquareCoordinate)).occupant is None:
                        canMoveorJump += 1
                if self.onBoard(self.rel(NORTHEAST, selectedSquareCoordinate)):
                    if self.location(self.rel(NORTHEAST, selectedSquareCoordinate)).occupant is None:
                        canMoveorJump += 1
            elif playerTurn is RED or king is True:
                if self.onBoard(self.rel(SOUTHWEST, selectedSquareCoordinate)):
                    if self.location(self.rel(SOUTHWEST, selectedSquareCoordinate)).occupant is None:
                        canMoveorJump += 1
                if self.onBoard(self.rel(SOUTHEAST, selectedSquareCoordinate)):
                    if self.location(self.rel(SOUTHEAST, selectedSquareCoordinate)).occupant is None:
                        canMoveorJump += 1

        return canMoveorJump

    def canJumpDirection(self, coordinate, playerTurn, DIRECTION):
        return self.onBoard(self.rel(DIRECTION, coordinate)) \
               and self.onBoard(self.relIncrement(DIRECTION, coordinate)) \
               and self.location(self.rel(DIRECTION, coordinate)).occupant is not None \
               and self.location(self.relIncrement(DIRECTION, coordinate)).occupant is None \
               and playerTurn is not self.location(self.rel(DIRECTION, coordinate)).occupant.color

    def legalMoves(self, playerTurn, selectedSquareCoordinate, jump, king, alreadyVisited):

        legalMoves = []
        legalMoves = alreadyVisited

        if alreadyVisited is not None:
            if self.relIncrement(NORTHWEST, selectedSquareCoordinate) in alreadyVisited \
                    or self.relIncrement(NORTHEAST, selectedSquareCoordinate) in alreadyVisited \
                    or self.relIncrement(SOUTHWEST, selectedSquareCoordinate) in alreadyVisited \
                    or self.relIncrement(SOUTHEAST, selectedSquareCoordinate) in alreadyVisited:
                return

        canMoveOrJumpCount = self.canMoveOrJumpCount(playerTurn, selectedSquareCoordinate, jump, king)
        print("canMoveOrJump = ", canMoveOrJumpCount)
        if canMoveOrJumpCount == 0:
            return

        if not jump:
            if playerTurn is WHITE or king is True:
                # Check if there is a empty square to move forward
                if self.onBoard(self.rel(NORTHWEST, selectedSquareCoordinate)):
                    if self.location(self.rel(NORTHWEST, selectedSquareCoordinate)).occupant is None:
                        legalMoves.append([self.rel(NORTHWEST, selectedSquareCoordinate)])
                if self.onBoard(self.rel(NORTHEAST, selectedSquareCoordinate)):
                    if self.location(self.rel(NORTHEAST, selectedSquareCoordinate)).occupant is None:
                        legalMoves.append([self.rel(NORTHEAST, selectedSquareCoordinate)])

            elif playerTurn is RED or king is True:
                if self.onBoard(self.rel(SOUTHWEST, selectedSquareCoordinate)):
                    if self.location(self.rel(SOUTHWEST, selectedSquareCoordinate)).occupant is None:
                        legalMoves.append([self.rel(SOUTHWEST, selectedSquareCoordinate)])
                if self.onBoard(self.rel(SOUTHEAST, selectedSquareCoordinate)):
                    if self.location(self.rel(SOUTHEAST, selectedSquareCoordinate)).occupant is None:
                        legalMoves.append([self.rel(SOUTHEAST, selectedSquareCoordinate)])

            # Any peace can jump over an opponent for any position

            # Check if there's a piece to jump over
            if self.canJumpDirection(selectedSquareCoordinate, playerTurn, NORTHWEST):
                # Append the piece's coordinate that will be jumped over
                legalMoves.append([self.rel(NORTHWEST, selectedSquareCoordinate)])
                # Append the piece destination
                legalMoves[-1] += [self.relIncrement(NORTHWEST, selectedSquareCoordinate)]
                legalMoves[-1] += [self.legalMoves(playerTurn, self.relIncrement(NORTHWEST, selectedSquareCoordinate),
                                                   True, king, legalMoves[-1])]

            if self.canJumpDirection(selectedSquareCoordinate, playerTurn, NORTHEAST):
                legalMoves.append([self.rel(NORTHEAST, selectedSquareCoordinate)])
                legalMoves[-1] += [self.relIncrement(NORTHEAST, selectedSquareCoordinate)]
                legalMoves[-1] += [self.legalMoves(playerTurn, self.relIncrement(NORTHEAST, selectedSquareCoordinate),
                                                   True, king, legalMoves[-1])]

            if self.canJumpDirection(selectedSquareCoordinate, playerTurn, SOUTHWEST):
                legalMoves.append([self.rel(SOUTHWEST, selectedSquareCoordinate)])
                legalMoves[-1] += [self.relIncrement(SOUTHWEST, selectedSquareCoordinate)]
                legalMoves[-1] += [self.legalMoves(playerTurn, self.relIncrement(SOUTHWEST, selectedSquareCoordinate),
                                                   True, king, legalMoves[-1])]

            if self.canJumpDirection(selectedSquareCoordinate, playerTurn, SOUTHEAST):
                legalMoves.append([self.rel(SOUTHEAST, selectedSquareCoordinate)])
                legalMoves[-1] += [self.relIncrement(SOUTHEAST, selectedSquareCoordinate)]
                legalMoves[-1] += [self.legalMoves(playerTurn, self.relIncrement(SOUTHEAST, selectedSquareCoordinate),
                                                   True, king, legalMoves[-1])]

        # Jumped at least once already
        if jump:

            print("recursive legalMoves =", legalMoves)

            if self.canJumpDirection(selectedSquareCoordinate, playerTurn, NORTHWEST):
                # It should be replicated based in number of
                # canMoveOrJumpCount() return testing a unique move path for now
                legalMoves[-1]([self.rel(NORTHWEST, selectedSquareCoordinate)])
                print("recursive NORTHWEST before = ", legalMoves[-1])
                legalMoves[-1] = [legalMoves[-1]] + [self.relIncrement(NORTHWEST, selectedSquareCoordinate)]
                print("recursive NORTHWEST after = ", legalMoves[-1])
                legalMoves[-1] += [self.legalMoves(playerTurn, self.relIncrement(NORTHWEST, selectedSquareCoordinate),
                                                   True, king, legalMoves)]

            if self.canJumpDirection(selectedSquareCoordinate, playerTurn, NORTHEAST):
                legalMoves[-1]([self.rel(NORTHEAST, selectedSquareCoordinate)])
                print("legalMoves[-1] NORTHWEST before = ", legalMoves[-1])
                legalMoves[-1] = [legalMoves[-1]] + [self.relIncrement(NORTHEAST, selectedSquareCoordinate)]
                print("legalMoves[-1] NORTHWEST after = ", legalMoves[-1])
                legalMoves[-1] += [self.legalMoves(playerTurn, self.relIncrement(NORTHEAST, selectedSquareCoordinate),
                                                   True, king, legalMoves)]

            if self.canJumpDirection(selectedSquareCoordinate, playerTurn, SOUTHWEST):
                legalMoves[-1]([self.rel(SOUTHWEST, selectedSquareCoordinate)])
                print("legalMoves[-1] SOUTHWEST before = ", legalMoves[-1])
                legalMoves[-1] = [legalMoves[-1]] + [self.relIncrement(SOUTHWEST, selectedSquareCoordinate)]
                print("legalMoves[-1] SOUTHWEST after = ", legalMoves[-1])
                legalMoves[-1] += [self.legalMoves(playerTurn, self.relIncrement(SOUTHWEST, selectedSquareCoordinate),
                                                   True, king, legalMoves)]

            if self.canJumpDirection(selectedSquareCoordinate, playerTurn, SOUTHEAST):
                legalMoves[-1]([self.rel(SOUTHEAST, selectedSquareCoordinate)])
                print("legalMoves[-1] SOUTHEAST before = ", legalMoves[-1])
                legalMoves[-1] = [legalMoves[-1]] + [self.relIncrement(SOUTHEAST, selectedSquareCoordinate)]
                print("legalMoves[-1] SOUTHEAST after = ", legalMoves[-1])
                legalMoves[-1] += [self.legalMoves(playerTurn, self.relIncrement(SOUTHEAST, selectedSquareCoordinate),
                                                   True, king, legalMoves)]

        return self.filterNoneMoves(legalMoves)

    def getLongestMoves(self, legalMoves):

        longestMoves = [[]]

        if legalMoves is None:
            return

        # Get the largest move
        for legalMove in legalMoves:
            if len(legalMove) > len(longestMoves[0]):
                longestMoves[0] = legalMove

        # Check if there's another move with the same size
        for legalMove in legalMoves:
            if len(legalMove) == len(longestMoves[0]) and legalMove not in longestMoves:
                longestMoves.append(legalMove)

        return longestMoves

    def filterNoneMoves(self, moves):
        for move in moves:
            if None in move:
                move.pop()
        return moves

    def exists(it):
        return (it is not None)

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
        self.king(endCoordinate)

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
        if self.location(coordinate).occupant != None:
            if (self.location(coordinate).occupant.color == WHITE and coordinate.y == 0) or (
                    self.location(coordinate).occupant.color == RED and coordinate.y == 7):
                self.location(coordinate).occupant.king = True


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
