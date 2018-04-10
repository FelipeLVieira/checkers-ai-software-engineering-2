import pygame, sys
from pygame.locals import *

pygame.font.init()

##COLORS##
#             R    G    B
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
HIGH = (160, 190, 255)

##DIRECTIONS##
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"


class Game:
    """
    The main game control.
    """

    def __init__(self):

        self.graphics = Graphics()
        self.board = Board()



        self.turn = BLUE
        self.selected_piece = None  # a board location.
        self.hop = False
        self.selected_legal_moves = []

    def setup(self):
        """Draws the window and board at the beginning of the game"""
        self.graphics.setup_window()

    def event_loop(self):
        """
        The event loop. This is where events are triggered
        (like a mouse click) and then effect the game state.
        """
        self.mouse_pos = self.graphics.board_coords(pygame.mouse.get_pos())  # what square is the mouse in?

        if self.selected_piece != None:
            self.selected_legal_moves = self.board.legal_moves(self.selected_piece, self.hop)

        for event in pygame.event.get():

            if event.type == QUIT:
                self.terminate_game()

            if event.type == MOUSEBUTTONDOWN:
                if self.hop == False:
                    if self.board.location(self.mouse_pos).occupant != None and self.board.location(
                            self.mouse_pos).occupant.color == self.turn:
                        self.selected_piece = self.mouse_pos

                    elif self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece):

                        self.board.move_piece(self.selected_piece, self.mouse_pos)

                        if self.mouse_pos not in self.board.adjacent(self.selected_piece):
                            self.board.remove_piece((self.selected_piece[0] + (
                            self.mouse_pos[0] - self.selected_piece[0]) / 2, self.selected_piece[1] + (
                                                     self.mouse_pos[1] - self.selected_piece[1]) / 2))

                            self.hop = True
                            self.selected_piece = self.mouse_pos

                        else:
                            self.end_turn()

                if self.hop == True:
                    if self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece,
                                                                                                self.hop):
                        self.board.move_piece(self.selected_piece, self.mouse_pos)
                        self.board.remove_piece((self.selected_piece[0] + (
                        self.mouse_pos[0] - self.selected_piece[0]) / 2, self.selected_piece[1] + (
                                                 self.mouse_pos[1] - self.selected_piece[1]) / 2))

                    if self.board.legal_moves(self.mouse_pos, self.hop) == []:
                        self.end_turn()

                    else:
                        self.selected_piece = self.mouse_pos

    def update(self):
        """Calls on the graphics class to update the game display."""
        self.graphics.update_display(self.board, self.selected_legal_moves, self.selected_piece)

    def terminate_game(self):
        """Quits the program and ends the game."""
        pygame.quit()
        sys.exit

    def main(self):
        """"This executes the game and controls its flow."""
        self.setup()

        while True:  # main game loop
            self.event_loop()
            self.update()

    def end_turn(self):
        """
        End the turn. Switches the current player.
        end_turn() also checks for and game and resets a lot of class attributes.
        """
        if self.turn == BLUE:
            self.turn = RED
        else:
            self.turn = BLUE

        self.selected_piece = None
        self.selected_legal_moves = []
        self.hop = False

        if self.check_for_endgame():
            if self.turn == BLUE:
                self.graphics.draw_message("RED WINS!")
            else:
                self.graphics.draw_message("BLUE WINS!")

    def check_for_endgame(self):
        """
        Checks to see if a player has run out of moves or pieces. If so, then return True. Else return False.
        """
        for x in range(8):
            for y in range(8):
                if self.board.location((x, y)).color == BLACK and self.board.location(
                        (x, y)).occupant != None and self.board.location((x, y)).occupant.color == self.turn:
                    if self.board.legal_moves((x, y)) != []:
                        return False

        return True


class Graphics:
    def __init__(self):
        self.caption = "Checkers"

        self.fps = 60
        self.clock = pygame.time.Clock()

        self.window_size = 600
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        self.background = pygame.image.load("graphics-proto/checker.png")

        self.square_size = self.window_size / 8
        self.piece_size = self.square_size / 2

        self.message = False

    def setup_window(self):
        """
        This initializes the window and sets the caption at the top.
        """
        pygame.init()
        pygame.display.set_caption(self.caption)

    def update_display(self, board, legal_moves, selected_piece):
        """
        This updates the current display.
        """
        self.screen.blit(self.background, (0, 0))

        self.highlight_squares(legal_moves, selected_piece)
        self.draw_board_pieces(board)

        if self.message:
            self.screen.blit(self.text_surface_obj, self.text_rect_obj)

        pygame.display.update()
        self.clock.tick(self.fps)

    def draw_board_squares(self, board):
        """
        Takes a board object and draws all of its squares to the display
        """
        for x in range(8):
            for y in range(8):
                pygame.draw.rect(self.screen, board[x][y].color,
                                 (x * self.square_size, y * self.square_size, self.square_size, self.square_size), )

    def draw_board_pieces(self, board):
        """
        Takes a board object and draws all of its pieces to the display
        """
        for x in range(8):
            for y in range(8):
                if board.matrix[x][y].occupant != None:
                    pygame.draw.circle(self.screen, board.matrix[x][y].occupant.color, self.pixel_coords((x, y)),
                                       self.piece_size)

                    if board.location((x, y)).occupant.king == True:
                        pygame.draw.circle(self.screen, GOLD, self.pixel_coords((x, y)), int(self.piece_size / 1.7),
                                           self.piece_size / 4)

    def pixel_coords(self, board_coords):
        """
        Takes in a tuple of board coordinates (x,y)
        and returns the pixel coordinates of the center of the square at that location.
        """
        return (
        board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)

    def board_coords(self, pixelCoordinate):
        """
        Does the reverse of pixel_coords(). Takes in a tuple of of pixel coordinates and returns what square they are in.
        """
        return Coordinate(pixelCoordinate.x / self.square_size, pixelCoordinate.y / self.square_size)

    def highlight_squares(self, squares, origin):
        """
        Squares is a list of board coordinates.
        highlight_squares highlights them.
        """
        for square in squares:
            pygame.draw.rect(self.screen, HIGH, (
            square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))

        if origin != None:
            pygame.draw.rect(self.screen, HIGH, (
            origin[0] * self.square_size, origin[1] * self.square_size, self.square_size, self.square_size))

    def draw_message(self, message):
        """
        Draws message to the screen.
        """
        self.message = True
        self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
        self.text_surface_obj = self.font_obj.render(message, True, HIGH, BLACK)
        self.text_rect_obj = self.text_surface_obj.get_rect()
        self.text_rect_obj.center = (self.window_size / 2, self.window_size / 2)


class Board:
    def __init__(self):
        self.matrix = self.new_board()

    def new_board(self):
        """
        Create a new board matrix.
        """

        # initialize squares and place them in matrix

        matrix = [[None] * 8 for i in range(8)]

        # The following code block has been adapted from
        # http://itgirl.dreamhosters.com/itgirlgames/games/Program%20Leaders/ClareR/Checkers/checkers.py
        for x in range(8):
            for y in range(8):
                if (x % 2 != 0) and (y % 2 == 0):
                    matrix[y][x] = Square(WHITE)
                elif (x % 2 != 0) and (y % 2 != 0):
                    matrix[y][x] = Square(BLACK)
                elif (x % 2 == 0) and (y % 2 != 0):
                    matrix[y][x] = Square(WHITE)
                elif (x % 2 == 0) and (y % 2 == 0):
                    matrix[y][x] = Square(BLACK)

        # initialize the pieces and put them in the appropriate squares

        for x in range(8):
            for y in range(3):
                if matrix[x][y].color == BLACK:
                    matrix[x][y].occupant = Piece(RED)
            for y in range(5, 8):
                if matrix[x][y].color == BLACK:
                    matrix[x][y].occupant = Piece(BLUE)

        return matrix

    def board_string(self, board):
        """
        Takes a board and returns a matrix of the board space colors. Used for testing new_board()
        """

        board_string = [[None] * 8] * 8

        for x in range(8):
            for y in range(8):
                if board[x][y].color == WHITE:
                    board_string[x][y] = "WHITE"
                else:
                    board_string[x][y] = "BLACK"

        return board_string

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

        return [self.rel(NORTHWEST, coordinate), self.rel(NORTHEAST, coordinate), self.rel(SOUTHWEST, coordinate),
                self.rel(SOUTHEAST, coordinate)]

    def location(self, coordinate):
        """
        Takes a set of coordinates as arguments and returns self.matrix[x][y]
        This can be faster than writing something like self.matrix[coords[0]][coords[1]]
        """

        return self.matrix[coordinate.x][coordinate.y]

    def blind_legal_moves(self, coordinate):
        """
        Returns a list of blind legal move locations from a set of coordinates (x,y) on the board.
        If that location is empty, then blind_legal_moves() return an empty list.
        """

        if self.matrix[coordinate.x][coordinate.y].occupant != None:

            if self.matrix[coordinate.x][coordinate.y].occupant.king == False and self.matrix[coordinate.x][coordinate.y].occupant.color == BLUE:
                blind_legal_moves = [self.rel(NORTHWEST, coordinate), self.rel(NORTHEAST, coordinate)]

            elif self.matrix[coordinate.x][coordinate.y].occupant.king == False and self.matrix[coordinate.x][coordinate.y].occupant.color == RED:
                blind_legal_moves = [self.rel(SOUTHWEST, coordinate), self.rel(SOUTHEAST, coordinate)]

            else:
                blind_legal_moves = [self.rel(NORTHWEST, coordinate), self.rel(NORTHEAST, coordinate),
                                     self.rel(SOUTHWEST, coordinate), self.rel(SOUTHEAST, coordinate)]

        else:
            blind_legal_moves = []

        return blind_legal_moves

    def legal_moves(self, coordinate, hop=False):
        """
        Returns a list of legal move locations from a given set of coordinates (x,y) on the board.
        If that location is empty, then legal_moves() returns an empty list.
        """

        blind_legal_moves = self.blind_legal_moves((coordinate.x, coordinate.y))
        legal_moves = []

        if hop == False:
            for move in blind_legal_moves:
                if hop == False:
                    if self.on_board(move):
                        if self.location(move).occupant == None:
                            legal_moves.append(move)

                        elif self.location(move).occupant.color != self.location(
                                (coordinate.x, coordinate.y)).occupant.color and self.on_board(
                                (move[0] + (move[0] - coordinate.x), move[1] + (move[1] - coordinate.y))) and self.location((move[0] + (
                            move[0] - coordinate.x), move[1] + (
                            move[1] - coordinate.y))).occupant == None:  # is this location filled by an enemy piece?
                            legal_moves.append((move[0] + (move[0] - coordinate.x), move[1] + (move[1] - coordinate.y)))

        else:  # hop == True
            for move in blind_legal_moves:
                if self.on_board(move) and self.location(move).occupant != None:
                    if self.location(move).occupant.color != self.location((coordinate.x, coordinate.y)).occupant.color and self.on_board(
                            (move[0] + (move[0] - coordinate.x), move[1] + (move[1] - coordinate.y))) and self.location((move[0] + (
                        move[0] - coordinate.x), move[1] + (
                        move[1] - coordinate.y))).occupant == None:  # is this location filled by an enemy piece?
                        legal_moves.append((move[0] + (move[0] - coordinate.x), move[1] + (move[1] - coordinate.y)))

        return legal_moves

    def remove_piece(self, coordinate):
        """
        Removes a piece from the board at position (x,y).
        """
        self.matrix[coordinate.x][coordinate.y].occupant = None

    def move_piece(self, startCoodinate, endCoordinate):
        """
        Move a piece from (start_x, start_y) to (end_x, end_y).
        """

        self.matrix[endCoordinate.x][endCoordinate.y].occupant = self.matrix[startCoodinate.x][startCoodinate.y].occupant
        self.remove_piece((startCoodinate.x, startCoodinate.y))

        self.king((endCoordinate.x, endCoordinate.y))

    def is_end_square(self, coords):
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
        if self.location(coordinate).occupant != None:
            if (self.location(coordinate).occupant.color == BLUE and coordinate.y == 0) or (
                    self.location(coordinate).occupant.color == RED and coordinate.y == 7):
                self.location(coordinate).occupant.king = True


class Piece:
    def __init__(self, color, king=False):
        self.color = color
        self.king = king


class Square:
    def __init__(self, color, occupant=None):
        self.color = color  # color is either BLACK or WHITE
        self.occupant = occupant  # occupant is a Square object

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def main():
    game = Game()
    game.main()


if __name__ == "__main__":
    main()