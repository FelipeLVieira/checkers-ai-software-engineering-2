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

        self.hoverPiece = None
        self.hoverButton = 0
        self.selectedPiece = None

        # Last timeDelta from last graphics update
        self.timeDelta = 0.

        # Player's turn switcher
        self.board.playerTurn = WHITE

        # Game state variables
        self.exitedGame = False
        self.states = {
                "playerTurn": playerTurnEventLoop,
                "AITurn": AITurnEventLoop,
                "pause": pauseEventLoop,
                "gameOver": gameOverEventLoop,
                "anim": waitForAnimationEventLoop
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
                    
                elif clickedRegion == BUTTON_PAUSE_HOVER_RESTART:
                    self.restartGame()
                    
                elif clickedRegion == BUTTON_PAUSE_HOVER_EXIT:
                    self.exitedGame = True
        
    
    def playerTurnEventLoop(self):
        """State "playerTurn": runs whenever the game is running and it's the
        (human) player's turn."""
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
                    
                elif clickedRegion == BUTTON_INGAME_HOVER_EXIT:
                    self.exitedGame = True
    
    def AITurnEventLoop(self):
        """State "AITurn": runs whenever the game is running, while the AI is
        playing."""
        AIResult = self.aiPlayer.updateAndCheckCompletion(self.timeDelta)
        if AIResult:
            self.graphics.registerMove(AIResult)
            self.state = "anim"
            self.stateAfterAnimation = "playerTurn"
            
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
                
                elif clickedRegion == BUTTON_INGAME_HOVER_EXIT:
                    self.exitedGame = True
            
            # Trap animation-triggered events
            elif event.type == EVENT_PIECE_VANISH:
                self.graphics.vanishPiece(event)
            
            elif event.type == EVENT_PATH_END:
                self.graphics.endPath()
                # Set next game state
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
        raise NotImplementedError()

    """---------------------+
    |  Auxiliary functions  |
    +---------------------"""

    def getBoardCoords(self, pos):
        return (min(0, max(7, (pos[0] - graphics.boardUpperLeftCoords) / 
                            graphics.boardSpacing)),
                min(0, max(7, (pos[1] - graphics.boardUpperLeftCoords) / 
                            graphics.boardSpacing))
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

        #--------------------------------------+
        # REMOVE ALL OF THESE STUBS when their |
        # actual functions are implemented,    |
        # replacing them with actual values.   |
        #--------------------------------------+

        # Reminder: gameEnded is False if the game is not over, or the string
        # constants ENDGAME_WIN or ENDGAME_LOSE if the game is over and the
        # (human) player has won or lost, respectively.
        stub_gameEnded = False

        # The player and opponent's score is the number of pieces they each have.
        stub_scorePlayer = 12
        stub_scoreOpponent = 12
        # This is the turn number. It should be incremented after the
        # (human) player finishes playing.
        # (or after the AI finishes, doesn't really make a difference)
        # Don't increment it in both loops! Only once.
        stub_turnNumber = 1

        self.timeDelta = self.graphics.updateAndDraw(hoverPosition, 
                selectedPiece, hoverButton, gamePaused, 
                stub_turnNumber, isPlayerTurn, stub_gameEnded, 
                stub_scorePlayer, stub_scoreOpponent)

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
    
    def restartGame(self):
        raise NotImplementedError()

    """--------------+
    |      Main      |
    +--------------"""

    def main(self):

        while True:
            self.states[self.state]()
            self.updateMainGame()

def main():
    graphicsBackend = GraphicsBackend()
    game = GameLoop(graphicsBackend, 2, "")
    game.main()

if __name__ == "__main__":
    main()
