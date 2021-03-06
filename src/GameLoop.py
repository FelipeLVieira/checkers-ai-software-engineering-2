import pygame, sys
from Graphics import Graphics, GraphicsBackend
from Board import *
from Constants import *
from pygame.locals import *
import AI
import cProfile, pstats, io


class GameLoop:
    def __init__(self, graphicsBackend, difficultyLevel, playerName):

        self.board = Board()

        self.graphics = Graphics(graphicsBackend, self.board, playerName)
        self.aiPlayer = AI.AIPlayer(self.board, RED, difficultyLevel)
        # Cache parameters for when we need to restart the game
        self.graphicsBackend = graphicsBackend
        self.difficultyLevel = difficultyLevel
        self.playerName = playerName

        self.done = False

        self.mousePos = None

        self.hoverPiece = None
        self.hoverButton = 0
        self.selectedPiece = None
        self.profiler = cProfile.Profile()

        # Last timeDelta from last graphics update
        self.timeDelta = 0.

        self.turnNumber = 1

        # Player's turn switcher
        self.board.playerTurn = WHITE

        # Game state variables
        self.exitedGame = False
        self.gameEnded = None
        self.forceMove = None
        self.forcedMove = False
        self.states = {
            "playerTurn": self.playerTurnEventLoop,
            "AITurn": self.AITurnEventLoop,
            "pause": self.pauseEventLoop,
            "gameOver": self.gameOverEventLoop,
            "anim": self.waitForAnimationEventLoop
        }
        self.state = "playerTurn"
        self.stateBeforePause = None
        self.stateAfterAnimation = None

    """--------------+
    |  Event Loops   |
    +--------------"""

    def gameOverEventLoop(self):
        """State "gameOver": runs when the game has ended."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminateGame()

            elif event.type == pygame.MOUSEMOTION:
                self.updateMousePos(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                clickedRegion = self.handleClick(event.pos)

                if clickedRegion == BUTTON_END_HOVER_RESTART:
                    self.restartGame()

                elif clickedRegion == BUTTON_END_HOVER_EXIT or \
                        clickedRegion == BUTTON_INGAME_HOVER_EXIT:
                    self.exitedGame = True

    def pauseEventLoop(self):
        """State "pause": runs while the game is paused."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminateGame()

            elif event.type == pygame.MOUSEMOTION:
                self.updateMousePos(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                clickedRegion = self.handleClick(event.pos)

                if clickedRegion == BUTTON_PAUSE_HOVER_CONTINUE:
                    self.state = self.stateBeforePause
                    self.hoverButton = 0

                elif clickedRegion == BUTTON_PAUSE_HOVER_RESTART:
                    self.restartGame()

                elif clickedRegion == BUTTON_PAUSE_HOVER_EXIT:
                    self.exitedGame = True

    def playerTurnEventLoop(self):
        """State "playerTurn": runs whenever the game is running and it's the
        (human) player's turn."""
        if self.forceMove and not self.forcedMove:
            self.board.mouseClick = self.forceMove
            self.grabLegalMoves()
            self.forcedMove = True
            #print("Forcing move {}".format(self.forceMove))
            #print("self.mousePos: {}".format(self.board.mouseClick))
            #print("Legal moves: {}".format(self.board.legalMoveSet))
            #print("All legal moves: {}".format(self.board.fullLegalMoveSet))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminateGame()

            elif event.type == pygame.MOUSEMOTION:
                self.updateMousePos(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                clickedRegion = self.handleClick(event.pos)

                if clickedRegion == REGION_BOARD:
                    self.handleBoardClick(event.pos)

                elif clickedRegion == BUTTON_INGAME_HOVER_PAUSE:
                    self.stateBeforePause = "playerTurn"
                    self.state = "pause"
                    self.hoverButton = 0

                elif clickedRegion == BUTTON_INGAME_HOVER_EXIT:
                    self.exitedGame = True

    def AITurnEventLoop(self):
        """State "AITurn": runs whenever the game is running, while the AI is
        playing."""
        AIResult = self.aiPlayer.updateAndCheckCompletion(self.timeDelta)
        if AIResult:
            eatenPieces = self.board.computeEatenPieces(AIResult)
            self.board.executeMove(AIResult)
            self.board.clearCachedVariables()
            self.graphics.registerMove(self.board, AIResult, eatenPieces)
            self.state = "anim"
            self.stateAfterAnimation = "playerTurn"
            self.turnNumber += 1
            self.endTurn()
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminateGame()

            elif event.type == pygame.MOUSEMOTION:
                self.updateMousePos(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                clickedRegion = self.handleClick(event.pos)

                if clickedRegion == BUTTON_INGAME_HOVER_PAUSE:
                    self.stateBeforePause = "AITurn"
                    self.state = "pause"
                    self.hoverButton = 0

                elif clickedRegion == BUTTON_INGAME_HOVER_EXIT:
                    self.exitedGame = True

    def waitForAnimationEventLoop(self):
        """State "anim": begins running when a movement is registered and runs
        until its screen animation finishes."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminateGame()

            elif event.type == pygame.MOUSEMOTION:
                self.updateMousePos(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                clickedRegion = self.handleClick(event.pos)

                if clickedRegion == BUTTON_INGAME_HOVER_PAUSE:
                    self.stateBeforePause = "anim"
                    self.state = "pause"
                    self.hoverButton = 0

                elif clickedRegion == BUTTON_INGAME_HOVER_EXIT:
                    self.exitedGame = True
        if not self.graphics.pieceIsMoving:
            self.state = self.stateAfterAnimation

    """--------------------------+ 
    |  Event handling functions  |
    +--------------------------"""

    def updateMousePos(self, pos):
        """Determines where the mouse is hovering above and updates
        self.hoverPiece and self.hoverButton.
        Note that self.hoverPiece is a tuple within the board, whereas
        self.hoverButton is a region identifier within Constants.py.
        (e.g. BUTTON_INGAME_HOVER_PAUSE)
        Remember to never check region identifiers for non-visible regions!
        (e.g. pause buttons, when game is not paused...)"""
        # I know, the function is called handleClick and we are not clicking.
        # But it's a pure function and it works in this case, so it makes
        # sense to use it.
        region = self.handleClick(pos)

        if region is REGION_BOARD:
            self.hoverButton = 0
            self.hoverPiece = self.getBoardCoords(pos)
        else:
            self.hoverPiece = None
            self.hoverButton = region

    def handleClick(self, pos):
        """Determines the region where the mouse was clicked and returns it."""
        regions = {
            "playerTurn": self.graphics.regions,
            "AITurn": self.graphics.regions,
            "pause": self.graphics.pauseRegions,
            "anim": self.graphics.regions,
            "gameOver": self.graphics.gameOverRegions
        }
        for key, region in regions[self.state].items():
            if region.collidepoint(pos):
                return key
        return 0

    def handleBoardClick(self, pos):
        """Given the mouse was clicked within the board, determine the
        coordinates of where it was clicked and act accordingly, by grabbing
        a new set of legal moves or performing a move.

        If a new piece is selected, first clearPossibleMoves should be called
        on the Graphics object, then setPossibleMoves should be called on the
        Graphics object, passing the set of legal moves for that piece as an
        argument.

        If a move is issued, first call clearPossibleMoves on the Graphics
        object, then call registerMove on the Graphics object,
        switch to the "anim" state to wait for the animation to complete, and
        set stateAfterAnimation to the correct state before proceeding.
        ("playerTurn" if the movement is incomplete, "AITurn otherwise")"""

        self.board.mouseClick = self.getBoardCoords(pos)
        square = derefer(self.board.matrix, self.board.mouseClick)
        #print("Mouse click", self.board.mouseClick)

        if (square.occupant and square.occupant.color is self.board.playerTurn
                and not self.forceMove):
            self.grabLegalMoves()
	
        elif self.board.legalMoveSet and self.board.clickOnLegalMoveCoord():
            finishMoveExec = self.executeMovement()
            if finishMoveExec:
                self.board.clearCachedVariables()
                self.stateAfterAnimation = "AITurn"
                self.forceMove = None
                if self.endTurn():
                    self.aiPlayer.play()
            else:
                self.stateAfterAnimation = "playerTurn"
                self.forceMove = self.board.movedPath[-1]
                self.forcedMove = False
            self.state = "anim"

        #print("Selected piece coord", self.board.selectedPieceCoordinate)

        # raise NotImplementedError()

    def executeMovement(self):
        finishMoveExec = self.board.executeMove()
        self.graphics.clearPossibleMoves()
        #print(self.board.movedPath)
        self.graphics.registerMove(self.board, self.board.movedPath,
                                   self.board.jumpedPieces)
        return finishMoveExec

    def grabLegalMoves(self):
        oldSelectedPiece = self.board.selectedPieceCoordinate
        self.board.selectedPieceCoordinate = self.board.mouseClick

        legalMoves = self.board.getLegalMoves(
            self.board.mouseClick)

        if not legalMoves:
            self.graphics.showPiecesWithLegalMoves(
                self.board.getPiecesWithLegalMoves())
            self.board.selectedPieceCoordinate = oldSelectedPiece
            if oldSelectedPiece: self.board.getLegalMoves(oldSelectedPiece)
        else:
            self.board.legalMoveSet = legalMoves
            self.graphics.clearPossibleMoves()
            self.graphics.setPossibleMoves(self.board.legalMoveSet)

    """---------------------+
    |  Auxiliary functions  |
    +---------------------"""

    def getBoardCoords(self, pos):
        return (int(min(7, max(0, (pos[0] -
                                   self.graphics.boardUpperLeftCoords[0])
                               / self.graphics.boardSpacing))),
                int(min(7, max(0, (pos[1] -
                                   self.graphics.boardUpperLeftCoords[1])
                               / self.graphics.boardSpacing)))
                )


    """-----------------+
    |  Screen Updaters  |
    +-----------------"""

    def updateMainGame(self):
        selectedPiece = self.selectedPiece
        # The coordinates on the board where the mouse is hovering.
        hoverPosition = self.hoverPiece
        hoverButton = self.hoverButton

        gamePaused = (self.state == "pause")
        isPlayerTurn = (self.state == "playerTurn" or
                        self.state == "pause" and self.stateBeforePause == "playerTurn" or
                        self.state == "anim" and self.stateAfterAnimation == "playerTurn" or
                        self.state == "gameOver")

        # --------------------------------------+
        # REMOVE ALL OF THESE STUBS when their |
        # actual functions are implemented,    |
        # replacing them with actual values.   |
        # --------------------------------------+

        # Reminder: gameEnded is None if the game is not over, or the string
        # constants ENDGAME_WIN or ENDGAME_LOSE if the game is over and the
        # (human) player has won or lost, respectively.
        if self.state == "gameOver":
            gameEnded = self.gameEnded
        else: gameEnded = None

        # The player and opponent's score is the number of pieces they each have.
        scorePlayer = self.board.getNumberOfPlayerPieces()
        scoreOpponent = self.board.getNumberOfOpponentPieces()

        # This is the turn number. It should be incremented after the
        # (human) player finishes playing.
        # (or after the AI finishes, doesn't really make a difference)
        # Don't increment it in both loops! Only once.

        self.timeDelta = self.graphics.updateAndDraw(hoverPosition,
                selectedPiece, hoverButton, gamePaused, 
                self.turnNumber, isPlayerTurn, gameEnded,
                scorePlayer, scoreOpponent)

    """------------------+
    |  Game Controllers  |
    +------------------"""

    def pauseGame(self):
        return

    def endTurn(self):
        if self.checkForEndgame():
            return False
        if self.board.playerTurn is WHITE:
            self.board.playerTurn = RED
        else:
            self.board.playerTurn = WHITE
        return True

    def checkForEndgame(self):
        endGame = self.board.checkWinCondition()
        if not endGame:
            endGame = self.board.isDraw
        #print(endGame)
        if endGame:
            self.gameEnded = {
                    RED: ENDGAME_LOSE,
                    WHITE: ENDGAME_WIN,
                    True: ENDGAME_DRAW
                    }[endGame]
            self.stateAfterAnimation = "gameOver"
            return True
        return False

    def terminateGame(self):
        pygame.quit()
        sys.exit()

    def restartGame(self):
        raise gameRestartException()

    """--------------+
    |      Main      |
    +--------------"""

    def mainLoop(self):

        while True:
            self.states[self.state]()
            self.updateMainGame()
            if self.exitedGame: return


class gameRestartException(BaseException):
    pass


def main():
    graphicsBackend = GraphicsBackend()
    game = GameLoop(graphicsBackend, 2, "")
    game.mainLoop()


if __name__ == "__main__":
    main()
