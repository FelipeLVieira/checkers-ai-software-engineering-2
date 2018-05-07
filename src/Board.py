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
        for m in move:
            if m.x == coordinate.x and m.y == coordinate.y:
                return True
        return False

    def canMoveOrJumpCount(self, playerTurn, currentCoordinate, jump, move):

        possibleJumpsCount = 0

        # Checks for all directions if a piece can jump an enemy given a coordinate
        if self.onBoard(self.nextCoordinate(NORTHWEST, currentCoordinate)) \
                and self.onBoard(self.afterNextCoordinate(NORTHWEST, currentCoordinate)) \
                and self.location(self.nextCoordinate(NORTHWEST, currentCoordinate)).occupant is not None \
                and self.location(self.afterNextCoordinate(NORTHWEST, currentCoordinate)).occupant is None \
                and not self.moveContainsCoordinate(self.afterNextCoordinate(NORTHWEST, currentCoordinate), move) \
                and playerTurn is not self.location(
            self.nextCoordinate(NORTHWEST, currentCoordinate)).occupant.color:
            possibleJumpsCount += 1

        if self.onBoard(self.nextCoordinate(NORTHEAST, currentCoordinate)) \
                and self.onBoard(self.afterNextCoordinate(NORTHEAST, currentCoordinate)) \
                and self.location(self.nextCoordinate(NORTHEAST, currentCoordinate)).occupant is not None \
                and self.location(self.afterNextCoordinate(NORTHEAST, currentCoordinate)).occupant is None \
                and not self.moveContainsCoordinate(self.afterNextCoordinate(NORTHEAST, currentCoordinate), move) \
                and playerTurn is not self.location(
            self.nextCoordinate(NORTHEAST, currentCoordinate)).occupant.color:
            possibleJumpsCount += 1

        if self.onBoard(self.nextCoordinate(SOUTHWEST, currentCoordinate)) \
                and self.onBoard(self.afterNextCoordinate(SOUTHWEST, currentCoordinate)) \
                and self.location(self.nextCoordinate(SOUTHWEST, currentCoordinate)).occupant is not None \
                and self.location(self.afterNextCoordinate(SOUTHWEST, currentCoordinate)).occupant is None \
                and not self.moveContainsCoordinate(self.afterNextCoordinate(SOUTHWEST, currentCoordinate), move) \
                and playerTurn is not self.location(
            self.nextCoordinate(SOUTHWEST, currentCoordinate)).occupant.color:
            possibleJumpsCount += 1

        if self.onBoard(self.nextCoordinate(SOUTHEAST, currentCoordinate)) \
                and self.onBoard(self.afterNextCoordinate(SOUTHEAST, currentCoordinate)) \
                and self.location(self.nextCoordinate(SOUTHEAST, currentCoordinate)).occupant is not None \
                and self.location(self.afterNextCoordinate(SOUTHEAST, currentCoordinate)).occupant is None \
                and not self.moveContainsCoordinate(self.afterNextCoordinate(SOUTHEAST, currentCoordinate), move) \
                and playerTurn is not self.location(
            self.nextCoordinate(SOUTHEAST, currentCoordinate)).occupant.color:
            possibleJumpsCount += 1

        # Check if the piece never jumped before
        if not jump and possibleJumpsCount == 0:
            if playerTurn is WHITE:
                # Check if there is a empty square to move forward
                if self.onBoard(self.nextCoordinate(NORTHWEST, currentCoordinate)):
                    if self.location(self.nextCoordinate(NORTHWEST, currentCoordinate)).occupant is None:
                        possibleJumpsCount += 1
                if self.onBoard(self.nextCoordinate(NORTHEAST, currentCoordinate)):
                    if self.location(self.nextCoordinate(NORTHEAST, currentCoordinate)).occupant is None:
                        possibleJumpsCount += 1
            elif playerTurn is RED:
                if self.onBoard(self.nextCoordinate(SOUTHWEST, currentCoordinate)):
                    if self.location(self.nextCoordinate(SOUTHWEST, currentCoordinate)).occupant is None:
                        possibleJumpsCount += 1
                if self.onBoard(self.nextCoordinate(SOUTHEAST, currentCoordinate)):
                    if self.location(self.nextCoordinate(SOUTHEAST, currentCoordinate)).occupant is None:
                        possibleJumpsCount += 1

        return possibleJumpsCount

    def canJumpDirection(self, coordinate, playerTurn, DIRECTION, move):
        """
            Given a coordinate, color, direction and a list of moves, checks if there's another available jump
        """
        return self.onBoard(self.nextCoordinate(DIRECTION, coordinate)) \
               and self.onBoard(self.afterNextCoordinate(DIRECTION, coordinate)) \
               and self.location(self.nextCoordinate(DIRECTION, coordinate)).occupant is not None \
               and self.location(self.afterNextCoordinate(DIRECTION, coordinate)).occupant is None \
               and playerTurn is not self.location(self.nextCoordinate(DIRECTION, coordinate)).occupant.color

    def legalMoves(self, playerTurn, currentCoordinate, jump, previous, move):
        # Get the number of actions in this call
        canMoveOrJumpCount = self.canMoveOrJumpCount(playerTurn, currentCoordinate, jump, move)
        # No positions to jump, return
        if canMoveOrJumpCount == 0:
            return move

        if not jump:
            legalMoves = []

            if playerTurn is WHITE:
                # Check if there is a empty square to move forward
                if self.onBoard(self.nextCoordinate(NORTHWEST, currentCoordinate)):
                    if self.location(self.nextCoordinate(NORTHWEST, currentCoordinate)).occupant is None:
                        legalMoves.append([self.nextCoordinate(NORTHWEST, currentCoordinate)])
                if self.onBoard(self.nextCoordinate(NORTHEAST, currentCoordinate)):
                    if self.location(self.nextCoordinate(NORTHEAST, currentCoordinate)).occupant is None:
                        legalMoves.append([self.nextCoordinate(NORTHEAST, currentCoordinate)])

            elif playerTurn is RED:
                if self.onBoard(self.nextCoordinate(SOUTHWEST, currentCoordinate)):
                    if self.location(self.nextCoordinate(SOUTHWEST, currentCoordinate)).occupant is None:
                        legalMoves.append([self.nextCoordinate(SOUTHWEST, currentCoordinate)])
                if self.onBoard(self.nextCoordinate(SOUTHEAST, currentCoordinate)):
                    if self.location(self.nextCoordinate(SOUTHEAST, currentCoordinate)).occupant is None:
                        legalMoves.append([self.nextCoordinate(SOUTHEAST, currentCoordinate)])

            # Has no jump moves
            if len(legalMoves) == 2:
                return self.filterMoves(legalMoves)

            # Will jump
            # Check where to jump over and call recursive for that direction
            if self.canJumpDirection(currentCoordinate, playerTurn, NORTHWEST, move):
                # Append the piece's coordinate that will be jumped over
                move = [self.nextCoordinate(NORTHWEST, currentCoordinate)]
                # Append the piece destination
                move += [self.afterNextCoordinate(NORTHWEST, currentCoordinate)]
                legalMoves.append(self.legalMoves(playerTurn, self.afterNextCoordinate(NORTHWEST, currentCoordinate),
                                                  True, currentCoordinate, move))

            if self.canJumpDirection(currentCoordinate, playerTurn, NORTHEAST, move):
                move = [self.nextCoordinate(NORTHEAST, currentCoordinate)]
                move += [self.afterNextCoordinate(NORTHEAST, currentCoordinate)]
                legalMoves.append(self.legalMoves(playerTurn, self.afterNextCoordinate(NORTHEAST, currentCoordinate),
                                                  True, currentCoordinate, move))

            if self.canJumpDirection(currentCoordinate, playerTurn, SOUTHWEST, move):
                move = [self.nextCoordinate(SOUTHWEST, currentCoordinate)]
                move += [self.afterNextCoordinate(SOUTHWEST, currentCoordinate)]
                legalMoves.append(self.legalMoves(playerTurn, self.afterNextCoordinate(SOUTHWEST, currentCoordinate),
                                                  True, currentCoordinate, move))

            if self.canJumpDirection(currentCoordinate, playerTurn, SOUTHEAST, move):
                move = [self.nextCoordinate(SOUTHEAST, currentCoordinate)]
                move += [self.afterNextCoordinate(SOUTHEAST, currentCoordinate)]
                legalMoves.append(self.legalMoves(playerTurn, self.afterNextCoordinate(SOUTHEAST, currentCoordinate),
                                                  True, currentCoordinate, move))

        # Jumped at least once already
        # LegalMoves is temporally a simple array when enters here
        if jump:

            if self.canJumpDirection(currentCoordinate, playerTurn, NORTHWEST, move):
                move += [self.nextCoordinate(NORTHWEST, currentCoordinate)]
                move += [self.afterNextCoordinate(NORTHWEST, currentCoordinate)]
                return self.legalMoves(playerTurn, self.afterNextCoordinate(NORTHWEST, currentCoordinate),
                                       True, currentCoordinate, move)

            if self.canJumpDirection(currentCoordinate, playerTurn, NORTHEAST, move):
                move += [self.nextCoordinate(NORTHEAST, currentCoordinate)]
                move += [self.afterNextCoordinate(NORTHEAST, currentCoordinate)]
                return self.legalMoves(playerTurn, self.afterNextCoordinate(NORTHEAST, currentCoordinate),
                                       True, currentCoordinate, move)

            if self.canJumpDirection(currentCoordinate, playerTurn, SOUTHWEST, move):
                move += [self.nextCoordinate(SOUTHWEST, currentCoordinate)]
                move += [self.afterNextCoordinate(SOUTHWEST, currentCoordinate)]
                return self.legalMoves(playerTurn, self.afterNextCoordinate(SOUTHWEST, currentCoordinate),
                                       True, currentCoordinate, move)

            if self.canJumpDirection(currentCoordinate, playerTurn, SOUTHEAST, move):
                move += [self.nextCoordinate(SOUTHEAST, currentCoordinate)]
                move += [self.afterNextCoordinate(SOUTHEAST, currentCoordinate)]
                return self.legalMoves(playerTurn, self.afterNextCoordinate(SOUTHEAST, currentCoordinate),
                                       True, currentCoordinate, move)

        return self.filterMoves(legalMoves)

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

    def filterMoves(self, moves):

        for move in moves:
            if None in move:
                move.pop()

        return moves

    def exists(self):
        return self is not None

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
