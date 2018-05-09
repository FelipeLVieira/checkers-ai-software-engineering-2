import pygame

from Constants import *


class Board:
    def __init__(self):
        self.matrix = self.newBoard()

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

    """-------------------+
    |  Piece Moves Logic  |
    +-------------------"""

    def legalMoves(self, playerTurn, currentCoordinate, jump, previous, move, king):
        """
        Look for all possible movements recursively and return a list of possible moves
        """

        # Count the number of adjacent movements available on this coordinate
        canMoveOrJumpCount = self.canMoveOrJumpCount(playerTurn, currentCoordinate, jump, previous, move, king)
        print("legalMoves -> canMoveorJumpCount: ", canMoveOrJumpCount)

        # No positions to jump, return the move created by previous function(s) call(s)
        if canMoveOrJumpCount == 0:
            print("canMoveorJumpCount == 0 ", move)
            return move

        if not jump:

            """---------------+
            |   First Call    |
            +---------------"""

            legalMoves = []

            auxNorthwestmove = []
            auxNortheastmove = []
            auxSouthwestmove = []
            auxSoutheastmove = []

            if playerTurn is WHITE or king:
                # Check if there is a empty square to move forward
                if self.onBoard(self.nextCoordinate(NORTHWEST, currentCoordinate)):
                    if self.location(self.nextCoordinate(NORTHWEST, currentCoordinate)).occupant is None:
                        if king:
                            auxNorthwestmove = [self.nextCoordinate(NORTHWEST, currentCoordinate)]
                        else:
                            legalMoves.append([self.nextCoordinate(NORTHWEST, currentCoordinate)])

                if self.onBoard(self.nextCoordinate(NORTHEAST, currentCoordinate)):
                    if self.location(self.nextCoordinate(NORTHEAST, currentCoordinate)).occupant is None:
                        if king:
                            auxNortheastmove = [self.nextCoordinate(NORTHEAST, currentCoordinate)]
                        else:
                            legalMoves.append([self.nextCoordinate(NORTHEAST, currentCoordinate)])

            if playerTurn is RED or king:

                if self.onBoard(self.nextCoordinate(SOUTHWEST, currentCoordinate)):
                    if self.location(self.nextCoordinate(SOUTHWEST, currentCoordinate)).occupant is None:
                        if king:
                            auxSouthwestmove = [self.nextCoordinate(SOUTHWEST, currentCoordinate)]
                        else:
                            legalMoves.append([self.nextCoordinate(SOUTHWEST, currentCoordinate)])

                if self.onBoard(self.nextCoordinate(SOUTHEAST, currentCoordinate)):
                    if self.location(self.nextCoordinate(SOUTHEAST, currentCoordinate)).occupant is None:
                        if king:
                            auxSoutheastmove = [self.nextCoordinate(SOUTHEAST, currentCoordinate)]
                        else:
                            legalMoves.append([self.nextCoordinate(SOUTHEAST, currentCoordinate)])

            # Build kings path and also checks if king can jump
            if king:

                # NW

                # Will check if the direction is free to move and will stop at the first piece or end of board
                if auxNorthwestmove:
                    nextCoord = auxNorthwestmove[0]
                    while self.onBoard(nextCoord):
                        if self.location(self.nextCoordinate(NORTHWEST, nextCoord)) \
                                and self.onBoard(self.nextCoordinate(NORTHWEST, nextCoord)) \
                                and self.location(self.nextCoordinate(NORTHWEST, nextCoord)).occupant is None:
                            auxNorthwestmove += [self.nextCoordinate(NORTHWEST, nextCoord)]
                            nextCoord = self.nextCoordinate(NORTHWEST, nextCoord)
                        else:
                            break

                # Will check if it's possible to jump over a enemy piece
                if auxNorthwestmove and self.canJumpDirection(auxNorthwestmove[-1], playerTurn, NORTHWEST, previous,
                                                              auxNorthwestmove):
                    auxNorthwestmove = [self.nextCoordinate(NORTHWEST, auxNorthwestmove[-1])]
                    auxNorthwestmove += [self.afterNextCoordinate(NORTHWEST, auxNorthwestmove[-1])]
                elif not auxNorthwestmove and self.canJumpDirection(currentCoordinate, playerTurn, NORTHWEST, previous,
                                                                    auxNorthwestmove):
                    auxNorthwestmove = [self.nextCoordinate(NORTHWEST, currentCoordinate)]
                    auxNorthwestmove += [self.afterNextCoordinate(NORTHWEST, currentCoordinate)]
                # There is at least one jump, so call recursive to search for more jumps
                if auxNorthwestmove:
                    legalMoves.append(
                        self.legalMoves(playerTurn, auxNorthwestmove[-1],
                                        True, auxNorthwestmove[-1], auxNorthwestmove, king))

                # NE
                if auxNortheastmove:
                    nextCoord = auxNortheastmove[0]
                    while self.onBoard(nextCoord):
                        if self.onBoard(self.nextCoordinate(NORTHEAST, nextCoord)) \
                                and self.location(self.nextCoordinate(NORTHEAST, nextCoord)) \
                                and self.location(self.nextCoordinate(NORTHEAST, nextCoord)).occupant is None:
                            auxNortheastmove += [self.nextCoordinate(NORTHEAST, nextCoord)]
                            nextCoord = self.nextCoordinate(NORTHEAST, nextCoord)
                        else:
                            break
                if auxNortheastmove and self.canJumpDirection(auxNortheastmove[-1], playerTurn, NORTHEAST, previous,
                                                              auxNortheastmove):
                    auxNortheastmove = [self.nextCoordinate(NORTHEAST, auxNortheastmove[-1])]
                    auxNortheastmove += [self.afterNextCoordinate(NORTHEAST, auxNortheastmove[-1])]
                elif not auxNortheastmove and self.canJumpDirection(currentCoordinate, playerTurn, NORTHEAST, previous,
                                                                    auxNortheastmove):
                    auxNortheastmove = [self.nextCoordinate(NORTHEAST, currentCoordinate)]
                    auxNortheastmove += [self.afterNextCoordinate(NORTHEAST, currentCoordinate)]
                if auxNortheastmove:
                    legalMoves.append(
                        self.legalMoves(playerTurn, auxNortheastmove[-1],
                                        True, auxNortheastmove[-1], auxNortheastmove, king))

                # SW
                if auxSouthwestmove:
                    nextCoord = auxSouthwestmove[0]
                    while self.onBoard(nextCoord):
                        if self.onBoard(self.nextCoordinate(SOUTHWEST, nextCoord)) \
                                and self.location(self.nextCoordinate(SOUTHWEST, nextCoord)) \
                                and self.location(self.nextCoordinate(SOUTHWEST, nextCoord)).occupant is None:
                            auxSouthwestmove += [self.nextCoordinate(SOUTHWEST, nextCoord)]
                            nextCoord = self.nextCoordinate(SOUTHWEST, nextCoord)
                        else:
                            break
                if auxSouthwestmove and self.canJumpDirection(auxSouthwestmove[-1], playerTurn, SOUTHWEST, previous,
                                                              auxSouthwestmove):
                    auxSouthwestmove = [self.nextCoordinate(SOUTHWEST, auxSouthwestmove[-1])]
                    auxSouthwestmove += [self.afterNextCoordinate(SOUTHWEST, auxSouthwestmove[-1])]
                elif not auxSouthwestmove and self.canJumpDirection(currentCoordinate, playerTurn, SOUTHWEST, previous, auxSouthwestmove):
                    auxSouthwestmove = [self.nextCoordinate(SOUTHWEST, currentCoordinate)]
                    auxSouthwestmove += [self.afterNextCoordinate(SOUTHWEST, currentCoordinate)]

                if auxSouthwestmove:
                    legalMoves.append(
                        self.legalMoves(playerTurn, auxSouthwestmove[-1],
                                        True, auxSouthwestmove[-1], auxSouthwestmove, king))

                # SE
                if auxSoutheastmove:
                    nextCoord = auxSoutheastmove[0]
                    while self.onBoard(nextCoord):
                        if self.onBoard(self.nextCoordinate(SOUTHEAST, nextCoord)) \
                                and self.location(self.nextCoordinate(SOUTHEAST, nextCoord)) \
                                and self.location(self.nextCoordinate(SOUTHEAST, nextCoord)).occupant is None:
                            auxSoutheastmove += [self.nextCoordinate(SOUTHEAST, nextCoord)]
                            nextCoord = self.nextCoordinate(SOUTHEAST, nextCoord)
                        else:
                            break
                if auxSoutheastmove and self.canJumpDirection(auxSoutheastmove[-1], playerTurn, SOUTHEAST, previous,
                                                              auxSoutheastmove):
                    auxSoutheastmove = [self.nextCoordinate(SOUTHEAST, auxSoutheastmove[-1])]
                    auxSoutheastmove += [self.afterNextCoordinate(SOUTHEAST, auxSoutheastmove[-1])]
                elif not auxSoutheastmove and self.canJumpDirection(currentCoordinate, playerTurn, SOUTHEAST, previous, auxSoutheastmove):
                    auxSoutheastmove = [self.nextCoordinate(SOUTHEAST, currentCoordinate)]
                    auxSoutheastmove += [self.afterNextCoordinate(SOUTHEAST, currentCoordinate)]

                if auxSoutheastmove:
                    legalMoves.append(
                        self.legalMoves(playerTurn, auxSoutheastmove[-1],
                                        True, auxSoutheastmove[-1], auxSoutheastmove, king))

            """----------------+
            |  Recursive call  |
            +----------------"""

            if not king:
                # Check where to jump over and call recursive for that direction
                if self.canJumpDirection(currentCoordinate, playerTurn, NORTHWEST, previous, move):
                    # Append the piece's coordinate that will be jumped over
                    move = [self.nextCoordinate(NORTHWEST, currentCoordinate)]
                    # Append the piece destination
                    move += [self.afterNextCoordinate(NORTHWEST, currentCoordinate)]
                    legalMoves.append(
                        self.legalMoves(playerTurn, self.afterNextCoordinate(NORTHWEST, currentCoordinate),
                                        True, currentCoordinate, move, king))

                if self.canJumpDirection(currentCoordinate, playerTurn, NORTHEAST, previous, move):
                    move = [self.nextCoordinate(NORTHEAST, currentCoordinate)]
                    move += [self.afterNextCoordinate(NORTHEAST, currentCoordinate)]
                    legalMoves.append(
                        self.legalMoves(playerTurn, self.afterNextCoordinate(NORTHEAST, currentCoordinate),
                                        True, currentCoordinate, move, king))

                if self.canJumpDirection(currentCoordinate, playerTurn, SOUTHWEST, previous, move):
                    move = [self.nextCoordinate(SOUTHWEST, currentCoordinate)]
                    move += [self.afterNextCoordinate(SOUTHWEST, currentCoordinate)]
                    legalMoves.append(
                        self.legalMoves(playerTurn, self.afterNextCoordinate(SOUTHWEST, currentCoordinate),
                                        True, currentCoordinate, move, king))

                if self.canJumpDirection(currentCoordinate, playerTurn, SOUTHEAST, previous, move):
                    move = [self.nextCoordinate(SOUTHEAST, currentCoordinate)]
                    move += [self.afterNextCoordinate(SOUTHEAST, currentCoordinate)]
                    legalMoves.append(
                        self.legalMoves(playerTurn, self.afterNextCoordinate(SOUTHEAST, currentCoordinate),
                                        True, currentCoordinate, move, king))

        # Jumped at least once already
        # LegalMoves is temporally a simple array when enters here
        if jump:

            if self.canJumpDirection(currentCoordinate, playerTurn, NORTHWEST, previous, move):
                aux = move
                aux += [self.nextCoordinate(NORTHWEST, currentCoordinate)]
                aux += [self.afterNextCoordinate(NORTHWEST, currentCoordinate)]
                aux = self.legalMoves(playerTurn, self.afterNextCoordinate(NORTHWEST, currentCoordinate),
                                      True, currentCoordinate, aux, king)
                print("aux NORTHWEST", aux)
                return aux

            if self.canJumpDirection(currentCoordinate, playerTurn, NORTHEAST, previous, move):
                aux = move
                aux += [self.nextCoordinate(NORTHEAST, currentCoordinate)]
                aux += [self.afterNextCoordinate(NORTHEAST, currentCoordinate)]
                aux = self.legalMoves(playerTurn, self.afterNextCoordinate(NORTHEAST, currentCoordinate),
                                      True, currentCoordinate, aux, king)
                print("aux NORTHEAST", aux)
                return aux

            if self.canJumpDirection(currentCoordinate, playerTurn, SOUTHWEST, previous, move):
                aux = move
                aux += [self.nextCoordinate(SOUTHWEST, currentCoordinate)]
                aux += [self.afterNextCoordinate(SOUTHWEST, currentCoordinate)]
                aux = self.legalMoves(playerTurn, self.afterNextCoordinate(SOUTHWEST, currentCoordinate),
                                      True, currentCoordinate, aux, king)
                print("aux SOUTHWEST", aux)
                return aux

            if self.canJumpDirection(currentCoordinate, playerTurn, SOUTHEAST, previous, move):
                aux = move
                aux += [self.nextCoordinate(SOUTHEAST, currentCoordinate)]
                aux += [self.afterNextCoordinate(SOUTHEAST, currentCoordinate)]
                aux = self.legalMoves(playerTurn, self.afterNextCoordinate(SOUTHEAST, currentCoordinate),
                                      True, currentCoordinate, aux, king)
                print("aux SOUTHEAST", aux)
                return aux

        print("legalMoves ", legalMoves)

        return self.filterMoves(legalMoves)

    def getLongestMoves(self, legalMoves, king):

        """
        Given a list of possible moves, filter the largest.
        If draw, return all with the same size of the first largest move found
        """

        longestMoves = []

        if legalMoves is None:
            return

        for move in legalMoves:
            if len(move) > 1 and not king:
                longestMoves.append(move)

        if len(longestMoves) == 0:
            return legalMoves
        else:
            return longestMoves

        # Get the largest move
        """
        for legalMove in legalMoves:
            if len(legalMove) > len(longestMoves[0]):
                longestMoves[0] = legalMove
        
        # Check if there's another move with the same size
        
        for legalMove in legalMoves:
            if len(legalMove) == len(longestMoves[0]) and legalMove not in longestMoves:
                longestMoves.append(legalMove)
        """

        return longestMoves

    def filterMoves(self, moves):

        moves = [x for x in moves if x]

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

    """def removePiece(self, selectedLegalMoves, selectedSquareCoordinate, selectedPieceCoordinate):
        # Move the piece and check (and remove) pieces that it jumped over
        for movepath in selectedLegalMoves:
            for move in movepath:
                if move is not None:
                    if move.x == selectedSquareCoordinate.x and move.y == selectedSquareCoordinate.y and move is movepath[-1]:
                        self.board.movePiece(self.selectedPieceCoordinate, self.mousePos)
                        # Odd moves are moves that jump over pieces
                        # Call removePiece on even positions
                        if not len(movepath) % 2 != 0 and len(movepath) > 1:
                            for i in range(0, len(movepath), 2):
                                if self.board.location(movepath[i]).occupant and self.board.location(
                                        movepath[i]).occupant.color is not self.turn:
                                    self.board.removePiece(movepath[i])
                        self.selectedPieceCoordinate = None
                        self.selectedLegalMoves = None
                        self.endTurn()"""

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
