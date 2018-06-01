import sys
import pygame
from Graphics import Graphics
from Board import *
from Constants import *

# Using 'import numpy as np' to have a better view of printed array

pygame.font.init()  # Victor: Just to make it clear, we won't use system fonts in the final version.


# TODO: Create a class to handle blitting text on the screen!


class GameLoop:
    def __init__(self):

        self.graphics = Graphics()
        self.board = Board()

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
        self.board.mousePos = self.board.boardCoords(pygame.mouse.get_pos(),
                                                     self.graphics.squareSize)  # what square is the mouse in?

        for event in pygame.event.get():
            # ESC quits the game (just for now)... (by the way, closing the window works too because of pygame.QUIT)
            if (event.type == pygame.QUIT) or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.terminateGame()

            # Click event handling
            if event.type == pygame.MOUSEBUTTONDOWN and self.board.getDrawInformation() is False:

                self.board.mouseClick = self.board.mousePos

                print("mouseClick x", self.board.mouseClick[0], " y ",
                      self.board.mouseClick[1])

                print("Player color", self.board.playerTurn)

                # Select piece and get legal moves
                if self.board.location(
                        self.board.mouseClick).occupant is not None \
                        and self.board.location(
                    self.board.mouseClick).occupant.color == self.board.playerTurn and self.board.finishMoveExec:

                    self.board.selectedPieceCoordinate = self.board.mouseClick

                    print("Piece selected!")

                    # Get legal moves and filter for the longest moves only
                    self.board.legalMoveSet = self.board.getLegalMoves(
                        self.board.selectedPieceCoordinate)

                    print("self.board.legalMoveSet ",
                          self.board.legalMoveSet)

                # Move piece to another position
                elif self.board.legalMoveSet and self.board.validClick():

                    print("self.board.legalMoveSet", self.board.legalMoveSet)
                    print("self.board.executeMove()")
                    self.board.executeMove()

                    if self.board.finishMoveExec:
                        self.board.legalMoveSet = None
                        self.board.selectedPieceCoordinate = None
                        self.board.playerLegalMoves = None
                        self.board.mouseClick = None
                        self.endTurn()

    """-----------------+
    |  Screen Updaters  |
    +-----------------"""

    def updateStartScreen(self):
        return

    def updatePause(self):
        return

    def updateMainGame(self):
        self.graphics.updateMainGameDisplay(self.board,
                                            self.board.legalMoveSet,
                                            self.board.selectedPieceCoordinate)
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

        if self.board.playerTurn is WHITE:
            self.board.playerTurn = RED
        else:
            self.board.playerTurn = WHITE

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
