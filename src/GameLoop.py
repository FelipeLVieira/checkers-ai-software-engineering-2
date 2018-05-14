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
        self.board.turn = WHITE

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
                        and selectedSquare.occupant.color is self.board.turn:

                    self.board.selectedPieceCoordinate = self.mousePos

                    # Get legal moves and filter for the longest moves only
                    self.board.selectedLegalMoves = \
                        self.board.legalMoves(self.board.turn, self.mousePos,
                                              False, None, [], self.board.location(self.board.selectedPieceCoordinate).occupant.king)

                    # Filter for the moves that jump over pieces
                    self.board.selectedLegalMoves = self.board.getLongestMoves(self.board.selectedLegalMoves, self.board.location(
                        self.board.selectedPieceCoordinate).occupant.king)

                    print("Selected Legal Moves ", self.board.selectedLegalMoves)

                # Cancel piece selection
                elif self.board.location(self.mousePos) == self.board.location(self.board.selectedPieceCoordinate):
                    self.board.selectedPieceCoordinate = None
                    self.board.selectedLegalMoves = None

                # Move piece to another position
                elif self.board.location(self.mousePos).occupant is None and self.board.selectedPieceCoordinate is not None \
                        and self.board.selectedLegalMoves is not None:
                    selectedSquareCoordinate = Coordinate(self.mousePos.x, self.mousePos.y)

                    self.board.executeMove(selectedSquareCoordinate)

                    self.board.selectedPieceCoordinate = None
                    self.board.selectedLegalMoves = None
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
        self.graphics.updateMainGameDisplay(self.board, self.board.selectedLegalMoves, self.board.selectedPieceCoordinate)
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

        if self.board.turn is WHITE:
            self.board.turn = RED
        else:
            self.board.turn = WHITE

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
