import pygame
from src.Board import *


class Graphics:
    def __init__(self):
        self.caption = "Checkers"

        self.fps = 60
        self.clock = pygame.time.Clock()

        self.windowSize = 720
        self.screen = pygame.display.set_mode((self.windowSize, self.windowSize))
        self.background = pygame.image.load("../graphics-proto/checker.png")

        self.squareSize = int(round(self.windowSize / 8))
        self.pieceSize = int(round(self.squareSize / 2))

        self.message = False

    def setupWindow(self):
        pygame.init()
        pygame.display.set_caption(self.caption)

    def updateDisplay(self, board, legalMovements, selectedPiece):
        """
        This updates the current display.
        """
        self.screen.blit(self.background, (0, 0))

        # self.highlight_squares(legal_moves, selected_piece)
        self.drawBoardPieces(board)
        self.drawPossibleMovements(board, selectedPiece)

        if self.message:
            self.screen.blit(self.text_surface_obj, self.text_rect_obj)

        pygame.display.update()
        self.clock.tick(self.fps)

    def drawBoardSquares(self, board):
        """
            Takes a board object and draws all of its squares to the display
            """
        for x in range(8):
            for y in range(8):
                pygame.draw.rect(self.screen, board[x][y].color,
                                 (x * self.squareSize, y * self.squareSize, self.squareSize, self.squareSize), )

    def drawBoardPieces(self, board):
        for x in range(8):
            for y in range(8):
                if board.matrix[x][y].occupant is not None and board.matrix[x][y].color is BLACK and board.matrix[x][y].occupant.color is RED:
                    redPiece = pygame.image.load("../graphics-proto/piece_red.png")
                    self.screen.blit(redPiece, (x * 90, y * 90))

                if board.matrix[x][y].occupant is not None and board.matrix[x][y].color is BLACK and board.matrix[x][y].occupant.color is WHITE:
                    whitePiece = pygame.image.load("../graphics-proto/piece_white.png")
                    self.screen.blit(whitePiece, (x * 90, y * 90))

    def drawPossibleMovements(self, board, selectedPiece):
        if selectedPiece != None:
            goldPiece = pygame.image.load("../graphics-proto/gold.png")
            if (selectedPiece.x > 0 and selectedPiece.y > 0) and board.matrix[selectedPiece.x-1][selectedPiece.y-1].occupant is None:
                self.screen.blit(goldPiece, ((selectedPiece.x-1) * 90, (selectedPiece.y-1) * 90))
            if (selectedPiece.x < 7 and selectedPiece.y > 0) and board.matrix[selectedPiece.x+1][selectedPiece.y-1].occupant is None:
                self.screen.blit(goldPiece, ((selectedPiece.x+1) * 90, (selectedPiece.y-1) * 90))

            #CASO EXISTA UMA PEÇA EM VERMELHO PARA ATACAR
            if (selectedPiece.x-1 > 0 and selectedPiece.y-1 > 0) and board.matrix[selectedPiece.x-1][selectedPiece.y-1].occupant is not None and board.matrix[selectedPiece.x-1][selectedPiece.y-1].occupant.color == board.matrix[selectedPiece.x-1][selectedPiece.y-1].occupant.getEnemyColor():
                self.screen.blit(goldPiece, ((selectedPiece.x-2) * 90, (selectedPiece.y-2) * 90))
            if (selectedPiece.x-1 > 7 and selectedPiece.y-1 > 0) and board.matrix[selectedPiece.x+1][selectedPiece.y-1].occupant is not None and board.matrix[selectedPiece.x-1][selectedPiece.y-1].occupant.color == board.matrix[selectedPiece.x-1][selectedPiece.y-1].occupant.getEnemyColor():
                self.screen.blit(goldPiece, ((selectedPiece.x+2) * 90, (selectedPiece.y-2) * 90))



    def pixelCoords(self, boardCoords):
        """
            Takes in a tuple of board coordinates (x,y)
            and returns the pixel coordinates of the center of the square at that location.
        """
        return (
            boardCoords[0] * self.squareSize + self.pieceSize, boardCoords[1] * self.squareSize + self.pieceSize)

    def boardCoords(self, pixelCoordinate):
        """
           Does the reverse of pixel_coords(). Takes in a tuple of of pixel coordinates and returns what square they are in.
        """
        return Coordinate(int(pixelCoordinate[0] / self.squareSize), int(pixelCoordinate[1] / self.squareSize))


    def pixelToSquarePosition(self, pixelCoordinate):
        """
            Does the reverse of pixel_coords(). Takes in a tuple of of pixel coordinates and returns what square they are in.
        """
        return Coordinate(pixelCoordinate.x / self.squareSize, pixelCoordinate.y / self.squareSize)

    def piecePositionToPixel(self, boardPiece):
        return True

    def highlightSquares(self, squares, origin):
        return True

    def draw_message(self, message):
        """
        Draws message to the screen.
        """
        self.message = True
        self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
        self.text_surface_obj = self.font_obj.render(message, True, HIGH, BLACK)
        self.text_rect_obj = self.text_surface_obj.get_rect()
        self.text_rect_obj.center = (self.windowSize / 2, self.windowSize / 2)

    def onBoard(self, coordinates):
        """
        Checks to see if the given square (x,y) lies on the board.
        If it does, then on_board() return True. Otherwise it returns false.
        """

    def isEndSquare(self, coordinate):
        """
        Is passed a coordinate tuple (x,y), and returns true or
        false depending on if that square on the board is an end square.
        """

        if coordinate.x == 0 or coordinate.y == 7:
            return True
        else:
            return False

    def removePiece(self, coordinate, board):
        """
        Removes a piece from the board at position (x,y).
        """
        board.matrix[coordinate.x][coordinate.y].occupant = None

    def movePiece(self, startCoordinate, endCoordinate, board):
        """
        Move a piece from (start_x, start_y) to (end_x, end_y).
        """

        board.matrix[endCoordinate.x][endCoordinate.y].occupant = board.matrix[startCoordinate.x][
            startCoordinate.y].occupant
        self.removePiece(startCoordinate, board)

        board.king(endCoordinate)

    def isEndSquare(self, coords):

        if coords[1] == 0 or coords[1] == 7:
            return True
        else:
            return False
