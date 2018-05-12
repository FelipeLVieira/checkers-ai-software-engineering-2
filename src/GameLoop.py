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

        self.selectedPieceCoordinate = None
        self.mousePos = None
        self.selectedLegalMoves = []
        self.done = False

        # Player's turn switcher
        self.turn = WHITE

        # Boolean screen switchers
        self.startScreen = False
        self.mainGame = True
        self.gameOver = False
        self.pause = False

    def setup(self):
        self.graphics.setupWindow()

    """--------------+
    |  Event Loops   |
    +--------------"""

    def startScreenEventLoop(self):
        return

    def pauseEventLoop(self):
        return

    def mainGameEventLoop(self):
        self.mousePos = self.board.boardCoords(pygame.mouse.get_pos(),
                                               self.graphics.squareSize)  # what square is the mouse in?
        for event in pygame.event.get():
            # ESC quits the game (just for now)... (by the way, closing the window works too because of pygame.QUIT)
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.terminateGame()

            # Click event handling
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Get selected square object
                selectedSquare = self.board.location(self.mousePos)
                # Get coordinates
                selectedSquareCoordinate = Coordinate(self.mousePos.x, self.mousePos.y)

                # Select piece and get legal moves
                if self.board.location(self.mousePos).occupant is not None \
                        and selectedSquare.occupant.color is self.turn:

                    self.selectedPieceCoordinate = self.mousePos

                    # Get legal moves and filter for the longest moves only
                    self.selectedLegalMoves = \
                        self.board.legalMoves(self.turn, self.mousePos,
                                              False, None, [], self.board.location(self.selectedPieceCoordinate).occupant.king)

                    # Filter for the moves that jump over pieces
                    self.selectedLegalMoves = self.board.getLongestMoves(self.selectedLegalMoves, self.board.location(
                        self.selectedPieceCoordinate).occupant.king)

                    print("Selected Legal Moves ", self.selectedLegalMoves)

                # Cancel piece selection
                elif self.board.location(self.mousePos) == self.board.location(self.selectedPieceCoordinate):
                    self.selectedPieceCoordinate = None
                    self.selectedLegalMoves = None

                # Move piece to another position
                elif self.board.location(self.mousePos).occupant is None and self.selectedPieceCoordinate is not None \
                        and self.selectedLegalMoves is not None:
                    selectedSquareCoordinate = Coordinate(self.mousePos.x, self.mousePos.y)
                    # Move the piece and check (and remove) pieces that it jumped over
                    for movepath in self.selectedLegalMoves:
                        for idx, coordinate in enumerate(movepath):
                            if coordinate is not None:
                                # Check if the selected position is the position that jumps over all possible pieces
                                if coordinate.x == selectedSquareCoordinate.x and coordinate.y == selectedSquareCoordinate.y and coordinate is \
                                        movepath[-1]:
                                    self.board.movePiece(self.selectedPieceCoordinate, self.mousePos)
                                    self.board.removePiecesByMove(movepath, self.turn)

                                    self.selectedPieceCoordinate = None
                                    self.selectedLegalMoves = None
                                    selectedSquare = None

                                    self.endTurn()
                                # If the piece jump in a position smaller the farest square of the move
                                elif coordinate.x == selectedSquareCoordinate.x and coordinate.y == selectedSquareCoordinate.y and coordinate is not \
                                        movepath[-1] and self.board.location(
                                    self.selectedPieceCoordinate).occupant.king:
                                    auxMove = movepath[:idx]
                                    self.board.movePiece(self.selectedPieceCoordinate, self.mousePos)
                                    self.board.removePiecesByMove(auxMove, self.turn)

                                    self.selectedPieceCoordinate = None
                                    self.selectedLegalMoves = None
                                    selectedSquare = None

                                    self.endTurn()

    """-----------------+
    |  Screen Updaters  |
    +-----------------"""

    def updateStartScreen(self):
        return

    def updatePause(self):
        return

    def updateMainGame(self):
        self.graphics.updateMainGameDisplay(self.board, self.selectedLegalMoves, self.selectedPieceCoordinate, self.turn)
        pygame.display.flip()

    """------------------+
    |  Game Controllers  |
    +------------------"""

    def pauseGame(self):
        return

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

    """--------------+
    |      Main      |
    +--------------"""

    def main(self):
        self.setup()

        while True:
            if self.startScreen:
                self.startScreenEventLoop()
                self.updateStartScreen()
            if self.mainGame:
                self.mainGameEventLoop()
                self.updateMainGame()
            if self.pause:
                self.pauseEventLoop()
                self.updatePause()


def main():
    game = GameLoop()
    game.main()


if __name__ == "__main__":
    main()
