import pygame, sys
from Graphics import Graphics
from Board import *
from Constants import *
from pygame.locals import *

# Using 'import numpy as np' to have a better view of printed array

pygame.font.init()  # Victor: Just to make it clear, we won't use system fonts in the final version.


# TODO: Create a class to handle blitting text on the screen!


class GameLoop:
    def __init__(self):

        self.graphics = Graphics()
        self.board = Board()

        """print(np.array(self.board.boardString(self.board.matrix)))

        for x in range(0,8):
            for y in range(0,8):
                if self.board.matrix[x][y].occupant is not None:
                    print(self.board.matrix[x][y].occupant.color)
                else:
                    print("empty")
            print("\n")"""

        self.turn = WHITE
        self.selectedPieceCoordinate = None

        self.hop = False
        self.selectedLegalMoves = []
        self.done = False

    def setup(self):
        self.graphics.setupWindow()

    def eventLoop(self):
        self.mousePos = self.graphics.boardCoords(pygame.mouse.get_pos())  # what square is the mouse in?
        for event in pygame.event.get():
            # ESC quits the game (just for now)... (by the way, closing the window works too because of pygame.QUIT)
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.terminateGame()

            # Main variables
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get selected square object
                selectedSquare = self.board.location(self.mousePos)
                # Get coordinates
                selectedSquareCoordinate = Coordinate(self.mousePos.x, self.mousePos.y)

                # Select piece and get legal moves
                if self.selectedPieceCoordinate is None and self.board.location(self.mousePos).occupant is not None:

                    # Get legal moves
                    self.selectedLegalMoves = self.board.legalMoves(selectedSquareCoordinate)

                    # Validate selection
                    if selectedSquare.occupant is not None and selectedSquare.occupant.color is self.turn:
                        self.selectedPieceCoordinate = self.mousePos

                # Cancel piece selection
                elif self.board.location(self.selectedPieceCoordinate) == self.board.location(self.mousePos):
                    self.selectedPieceCoordinate = None

                # Move piece
                if self.board.location(self.mousePos).occupant is None and self.selectedPieceCoordinate is not None:
                    selectedSquareCoordinate = Coordinate(self.mousePos.x, self.mousePos.y)
                    # List of legal paths
                    for movepath in self.selectedLegalMoves:
                        if movepath.x == selectedSquareCoordinate.x and movepath.y == selectedSquareCoordinate.y:
                            self.board.movePiece(self.selectedPieceCoordinate, self.mousePos)
                            self.selectedPieceCoordinate = None
                            self.selectedLegalMoves = None
                            self.endTurn()
                        # Coordinates of a legal path
                        """for move in movepath:
                            if move.x == selectedSquareCoordinate.x and move.y == selectedSquareCoordinate.y:
                                self.board.movePiece(self.selectedPieceCoordinate, self.mousePos)
                                self.selectedPieceCoordinate = None
                                self.selectedLegalMoves = None
                                self.endTurn()"""

    def update(self):
        self.graphics.updateDisplay(self.board, self.selectedLegalMoves, self.selectedPieceCoordinate)
        pygame.display.flip()

    def endTurn(self):
        if self.checkForEndgame():
            return True

    def checkForEndgame(self):

        if self.turn is WHITE:
            self.turn = RED
        else:
            self.turn = WHITE

        return True

    def terminateGame(self):
        pygame.quit()
        sys.exit()

    def main(self):
        self.setup()

        while True:
            self.eventLoop()
            self.update()


def main():
    game = GameLoop()
    game.main()


if __name__ == "__main__":
    main()
