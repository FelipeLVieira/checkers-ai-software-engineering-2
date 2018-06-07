import pygame, sys
from Graphics import Graphics, GraphicsBackend
from Board import *
from Constants import *
from pygame.locals import *
import AI


class GameLoop:
    def __init__(self, graphicsBackend, difficultyLevel, playerName):

        self.board = Board()
        self.graphics = Graphics(graphicsBackend, self.board, playerName)
        self.aiPlayer = AI.AIPlayer(self.board, RED, difficultyLevel)
        self.done = False

        self.mousePos = None

        # Player's turn switcher
        self.board.playerTurn = WHITE

        # Boolean screen switchers
        self.startScreen = False
        self.mainGame = True
        self.gameOver = False
        self.pause = False

    """--------------+
    |  Event Loops   |
    +--------------"""

    def pauseEventLoop(self):
        return


    """-----------------------------------------------------+
    | VitinhoCarneiro: I'd recommend rewriting this.        |
    | I feel it'd be too much work to integrate it with the |
    | new board.                                            |
    | Use stubs as much as needed and then substitute it    |
    | for actual function calls when the Board              |
    | implementation is complete.                           |
    +-----------------------------------------------------"""
    def mainGameEventLoop(self):
        self.mousePos = self.board.boardCoords(pygame.mouse.get_pos(),
                                               self.graphics.boardSpacing, self.graphics.boardUpperLeftCoords)  # what square is the mouse in?

        for event in pygame.event.get():
            # ESC quits the game (just for now)... (by the way, closing the window works too because of pygame.QUIT)
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.terminateGame()

            # Click event handling
            if event.type == pygame.MOUSEBUTTONDOWN and self.board.getDrawInformation() is False:

                self.board.mouseClick = self.mousePos

                print(self.board.mouseClick)

                print("mouseClick x", self.board.mouseClick[0], " y ",
                      self.board.mouseClick[1])

                print("Player color", self.board.playerTurn)

                # Select piece and get legal moves
                if self.board.location(self.board.mouseClick).occupant is not None \
                        and self.board.location(self.board.mouseClick).occupant.color is self.board.playerTurn:
                    print("entered selectedPieceCoordinate")
                    self.board.selectedPieceCoordinate = Coordinate(self.board.mouseClick[0],
                                                                    self.board.mouseClick[1])

                    # Get legal moves and filter for the longest moves only
                    self.board.playerLegalMoves = self.board.getLegalMoves(self.board.selectedPieceCoordinate)

                    print("Selected Legal Moves ", self.board.playerLegalMoves)

                # Move piece to another position
                elif self.board.location(self.board.mouseClick).occupant is None and \
                        self.board.location(self.board.mouseClick) \
                        is not self.board.location(self.board.selectedPieceCoordinate):

                    print("execute move")
                    executed = self.board.executeMove()

                    if executed:
                        self.board.selectedPieceCoordinate = None
                        #self.board.selectedPieceMoves = None
                        self.board.playerLegalMoves = None
                        self.board.mouseClick = None
                        #self.board.selectedPieceMoves = None
                        self.endTurn()

    """-----------------+
    |  Screen Updaters  |
    +-----------------"""

    def updateStartScreen(self):
        return

    def updatePause(self):
        return

    def updateMainGame(self):
        #--------------------------------------+
        # REMOVE ALL OF THESE STUBS when their |
        # actual functions are implemented,    |
        # replacing them with actual values.   |
        #--------------------------------------+
        stub_selectedPiece = None
        stub_hoverPosition = None
        # Read Constants.py for the on-screen button identifiers
        stub_hoverButton = 0
        stub_gamePaused = False
        stub_isPlayerTurn = True
        stub_gameEnded = False

        # The player and opponent's score is the number of pieces they each have.
        stub_scorePlayer = 12
        stub_scoreOpponent = 12
        # This is the turn number. It should be incremented after the
        # (human) player finishes playing.
        # (or after the AI finishes, doesn't really make a difference)
        stub_turnNumber = 1

        self.graphics.updateAndDraw(stub_hoverPosition, stub_selectedPiece,
                stub_hoverButton, stub_gamePaused, stub_turnNumber, stub_isPlayerTurn,
                stub_gameEnded, stub_scorePlayer, stub_scoreOpponent)

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

        while True:
            if self.mainGame:
                self.mainGameEventLoop()
                self.updateMainGame()
            if self.pause:
                self.pauseEventLoop()
                self.updatePause()


def main():
    graphicsBackend = GraphicsBackend()
    game = GameLoop(graphicsBackend, 2, "")
    game.main()

if __name__ == "__main__":
    main()
