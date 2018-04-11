from src.Constants import *


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
                    matrix[y][x] = Square(BLACK)
                elif (x % 2 != 0) and (y % 2 != 0):
                    matrix[y][x] = Square(WHITE)
                elif (x % 2 == 0) and (y % 2 != 0):
                    matrix[y][x] = Square(BLACK)
                elif (x % 2 == 0) and (y % 2 == 0):
                    matrix[y][x] = Square(WHITE)

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

        boardString = [[None] * 8] * 8

        for x in range(8):
            for y in range(8):
                if board[x][y].color == WHITE:
                    boardString[x][y] = "WHITE"
                else:
                    boardString[x][y] = "BLACK"

        return boardString


    def rel(self, dir, coordinate):
        """
        Returns the coordinates one square in a different direction to (x,y).
        """
        if dir == NORTHWEST:
            return (coordinate.x - 1, coordinate.y - 1)
        elif dir == NORTHEAST:
            return (coordinate.x + 1, coordinate.y - 1)
        elif dir == SOUTHWEST:
            return (coordinate.x - 1, coordinate.y + 1)
        elif dir == SOUTHEAST:
            return (coordinate.x + 1, coordinate.y + 1)
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

        return self.matrix[coordinate.x][coordinate.y]

    def blindLegalMoves(self, coordinate):
        """
        Returns a list of blind legal move locations from a set of coordinates (x,y) on the board.
        If that location is empty, then blind_legal_moves() return an empty list.
        """

        if self.matrix[coordinate.x][coordinate.y].occupant != None:

            if self.matrix[coordinate.x][coordinate.y].occupant.king == False and self.matrix[coordinate.x][coordinate.y].occupant.color == BLUE:
                blindLegalMoves = [self.rel(NORTHWEST, coordinate), self.rel(NORTHEAST, coordinate)]

            elif self.matrix[coordinate.x][coordinate.y].occupant.king == False and self.matrix[coordinate.x][coordinate.y].occupant.color == RED:
                blindLegalMoves = [self.rel(SOUTHWEST, coordinate), self.rel(SOUTHEAST, coordinate)]

            else:
                blindLegalMoves = [self.rel(NORTHWEST, coordinate), self.rel(NORTHEAST, coordinate),
                                     self.rel(SOUTHWEST, coordinate), self.rel(SOUTHEAST, coordinate)]

        else:
            blindLegalMoves = []

        return blindLegalMoves



    def legalMoves(self, coordinate, hop=False):
        """
        Returns a list of legal move locations from a given set of coordinates (x,y) on the board.
        If that location is empty, then legal_moves() returns an empty list.
        """

        blind_legal_moves = self.blind_legal_moves((coordinate.x, coordinate.y))
        legalMoves = []

        if hop == False:
            for move in blind_legal_moves:
                if hop == False:
                    if self.on_board(move):
                        if self.location(move).occupant == None:
                            legalMoves.append(move)

                        elif self.location(move).occupant.color != self.location(
                                (coordinate.x, coordinate.y)).occupant.color and self.on_board(
                                (move[0] + (move[0] - coordinate.x), move[1] + (move[1] - coordinate.y))) and self.location((move[0] + (
                            move[0] - coordinate.x), move[1] + (
                            move[1] - coordinate.y))).occupant == None:  # is this location filled by an enemy piece?
                            legalMoves.append((move[0] + (move[0] - coordinate.x), move[1] + (move[1] - coordinate.y)))

        else:  # hop == True
            for move in blind_legal_moves:
                if self.on_board(move) and self.location(move).occupant != None:
                    if self.location(move).occupant.color != self.location((coordinate.x, coordinate.y)).occupant.color and self.on_board(
                            (move[0] + (move[0] - coordinate.x), move[1] + (move[1] - coordinate.y))) and self.location((move[0] + (
                        move[0] - coordinate.x), move[1] + (
                        move[1] - coordinate.y))).occupant == None:  # is this location filled by an enemy piece?
                        legalMoves.append((move[0] + (move[0] - coordinate.x), move[1] + (move[1] - coordinate.y)))

        return legalMoves

    def remove_piece(self, coordinate):
        """
        Removes a piece from the board at position (x,y).
        """
        self.matrix[coordinate.x][coordinate.y].occupant = None

    def move_piece(self, startCoordinate, endCoordinate):
        """
        Move a piece from (start_x, start_y) to (end_x, end_y).
        """

        self.matrix[endCoordinate.x][endCoordinate.y].occupant = self.matrix[startCoordinate.x][
            startCoordinate.y].occupant
        self.remove_piece((startCoordinate.x, startCoordinate.y))

        self.king((endCoordinate.x, endCoordinate.y))

    def isEndSquare(self, coords):
        """
        Is passed a coordinate tuple (x,y), and returns true or
        false depending on if that square on the board is an end square.
        """

        if coords[1] == 0 or coords[1] == 7:
            return True
        else:
            return False

    def on_board(self, coordinate):
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
