from GameLoop import *
from Constants import *

class testingGraphicsBackend(GraphicsBackend):
    def __init__(self):
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.timeDelta = 0
        self.windowWidth = 1280
        self.windowHeight = 720
        self.screen = None

class testingGraphics(Graphics):
    def __init__(self, graphicsBackend, board, playerName):
        self.fps = graphicsBackend.fps
        self.clock = graphicsBackend.clock
        self.timeDelta = graphicsBackend.timeDelta
        self.windowWidth = graphicsBackend.windowWidth
        self.windowHeight = graphicsBackend.windowHeight
        self.screen = graphicsBackend.screen
        # Coordinates
        self.pauseButtonCoords = (877, 619)
        self.exitButtonCoords = (1012, 619)
        self.upperScoreBaselineCoords = (980, 256)
        self.lowerScoreBaselineCoords = (980, 524)
        self.turnTextBaselineCoords = (988, 323)
        self.upperNameBaselineCoords = (988, 48)
        self.lowerNameBaselineCoords = (988, 590)
        self.pauseBannerBaselineCoords = (640, 224)
        self.pauseContinueBaselineCoords = (640, 333)
        self.pauseRestartBaselineCoords = (640, 400)
        self.pauseExitBaselineCoords = (640, 467)
        self.pauseContinueButtonCoords = (499, 295)
        self.pauseRestartButtonCoords = (499, 362)
        self.pauseExitButtonCoords = (499, 429)
        self.winLoseBaselineRelCoords = (300, 95)
        self.endRestartBaselineRelCoords = (151, 176)
        self.endExitBaselineRelCoords = (449, 176)
        self.endRestartButtonRelCoords = (12, 136)
        self.endExitButtonRelCoords = (310, 136)
        self.endOverlayTextsRelCoords = {
                "winLoseFanfare": self.winLoseBaselineRelCoords,
                "endRestart": self.endRestartBaselineRelCoords,
                "endExit": self.endExitBaselineRelCoords,
                }
        self.endOverlayButtonsRelCoords = {
                BUTTON_END_HOVER_RESTART: self.endRestartButtonRelCoords,
                BUTTON_END_HOVER_EXIT: self.endExitButtonRelCoords
                }
        self.boardUpperLeftCoords = (139, 37)
        self.endOverlayFinalCoords = ()
        # Other values
        self.boardSpacing = 82
        self.pieceBaseMoveSpeed = 460
        self.endOverlayDimensions = (600, 210)
        # Screen regions
        self.regions = {
                REGION_BOARD: pygame.Rect(self.boardUpperLeftCoords, (656, 656)),
                BUTTON_INGAME_HOVER_PAUSE: pygame.Rect(
                        self.pauseButtonCoords, (82, 82)),
                BUTTON_INGAME_HOVER_EXIT: pygame.Rect(
                        self.exitButtonCoords, (82, 82))
                }
        self.pauseRegions = {
                BUTTON_PAUSE_HOVER_CONTINUE: pygame.Rect(
                        self.pauseContinueButtonCoords, (279, 54)),
                BUTTON_PAUSE_HOVER_RESTART: pygame.Rect(
                        self.pauseRestartButtonCoords, (279, 54)),
                BUTTON_PAUSE_HOVER_EXIT: pygame.Rect(
                        self.pauseExitButtonCoords, (279, 54))
                }
        self.gameOverRegions = {
                BUTTON_END_HOVER_RESTART: pygame.Rect(
                        tplsum(tplsum(self.endRestartButtonRelCoords, 
                                tplscale(self.endOverlayDimensions, -0.5)), 
                                        (640, 360)),
                        (278, 58)),
                BUTTON_END_HOVER_EXIT: pygame.Rect(
                        tplsum(tplsum(self.endExitButtonRelCoords, 
                                tplscale(self.endOverlayDimensions, -0.5)), 
                                        (640, 360)),
                        (278, 58)),
                BUTTON_INGAME_HOVER_EXIT: pygame.Rect(
                        self.exitButtonCoords, (82, 82))
                }
        self.UIButtonsHoverCoords = {
                BUTTON_INGAME_HOVER_NONE: None,
                BUTTON_INGAME_HOVER_PAUSE: self.pauseButtonCoords,
                BUTTON_INGAME_HOVER_EXIT: self.exitButtonCoords
                }

        self.pauseButtonsHoverCoords = {
                BUTTON_PAUSE_HOVER_NONE: None,
                BUTTON_PAUSE_HOVER_CONTINUE: self.pauseContinueButtonCoords,
                BUTTON_PAUSE_HOVER_RESTART: self.pauseRestartButtonCoords,
                BUTTON_PAUSE_HOVER_EXIT: self.pauseExitButtonCoords
                }

class testingGameLoop(GameLoop):
    def __init__(self, graphicsBackend, difficultyLevel, playerName):
        self.board = Board()
        self.graphics = testingGraphics(graphicsBackend, self.board, playerName)
        self.aiPlayer = None
        # Cache parameters for when we need to restart the game
        self.graphicsBackend = graphicsBackend
        self.difficultyLevel = difficultyLevel
        self.playerName = playerName

        self.done = False

        self.mousePos = None

        self.hoverPiece = None
        self.hoverButton = 0
        self.selectedPiece = None
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

def tplsum(t1, t2):
    """Returns the sum of two tuples."""
    return tuple(map(lambda x, y: x + y, t1, t2)) 

def tplscale(t, mult):
    """Returns the multiplication of a tuple by a number."""
    return tuple(map(lambda x: x * mult, t))






def test_handleClick1():
    # VitinhoCarneiro: This variable is unused...
    selectedPiece = []
    boardUpperLeftCoords = (139, 37)
    boardSpacing = 82
    # VitinhoCarneiro: It would be a good idea to create a mock GraphicsBackend
    # to avoid having the window open up every time you run a test.
    # Moreover, you're making pyTest instance multiple GraphicsBackend
    # instances at the same time, which initializes pygame a bunch of times,
    # and that can cause problems.
    graphicsBackend = testingGraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = testingGameLoop(graphicsBackend,
                                 selectedDifficultyButton, playerName)
    # VitinhoCarneiro: Why is this even necessary? handleClick does not handle
    # individual board pieces, just screen regions.
    # And you know, there's a thing called a for loop...
    for i in range(8):
        for j in range(8):
            selectedPiece.append((i, j))

    for coord in selectedPiece:
        pixelPosition = (coord[0] * boardSpacing + boardUpperLeftCoords[0],
              coord[1] * boardSpacing + boardUpperLeftCoords[1])

        result = gameLoop.handleClick(pixelPosition)
        assert result == REGION_BOARD


def test_handleClick2():
    pauseButton = (877, 619)
    graphicsBackend = testingGraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = testingGameLoop(graphicsBackend,
                                 selectedDifficultyButton, playerName)

    result = gameLoop.handleClick(pauseButton)

    assert result == BUTTON_INGAME_HOVER_PAUSE
    pygame.quit()

def test_handleClick3():
    exitButton = (1012, 619)
    graphicsBackend = testingGraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = testingGameLoop(graphicsBackend,
                                 selectedDifficultyButton, playerName)

    result = gameLoop.handleClick(exitButton)

    assert result == BUTTON_INGAME_HOVER_EXIT

def test_handleClick4():
    pauseContinueButton = (499, 295)
    graphicsBackend = testingGraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = testingGameLoop(graphicsBackend,
                                 selectedDifficultyButton, playerName)

    gameLoop.stateBeforePause = "playerTurn"
    gameLoop.state = "pause"
    gameLoop.hoverButton = 0

    result = gameLoop.handleClick(pauseContinueButton)

    assert result == BUTTON_PAUSE_HOVER_CONTINUE
    pygame.quit()

def test_handleClick5():
    pauseRestartButton = (499, 362)
    graphicsBackend = testingGraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = testingGameLoop(graphicsBackend,
                                 selectedDifficultyButton, playerName)

    gameLoop.stateBeforePause = "playerTurn"
    gameLoop.state = "pause"
    gameLoop.hoverButton = 0

    result = gameLoop.handleClick(pauseRestartButton)

    assert result == BUTTON_PAUSE_HOVER_RESTART

def test_handleClick6():
    pauseExitButton = (499, 429)
    graphicsBackend = testingGraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = testingGameLoop(graphicsBackend,
                                 selectedDifficultyButton, playerName)

    gameLoop.stateBeforePause = "playerTurn"
    gameLoop.state = "pause"
    gameLoop.hoverButton = 0

    result = gameLoop.handleClick(pauseExitButton)

    assert result == BUTTON_PAUSE_HOVER_EXIT
    pygame.quit()

def test_handleClick7():
    endRestartButton = (506, 420)
    graphicsBackend = testingGraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = testingGameLoop(graphicsBackend,
                                 selectedDifficultyButton, playerName)

    gameLoop.state = "gameOver"
    gameLoop.stateBeforePause = None
    gameLoop.stateAfterAnimation = "gameOver"
    #gameLoop.hoverButton = 0

    result = gameLoop.handleClick(endRestartButton)

    assert result == BUTTON_END_HOVER_RESTART

def test_handleClick8():
    endExittButton = (721, 430)
    graphicsBackend = testingGraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = testingGameLoop(graphicsBackend,
                                 selectedDifficultyButton, playerName)

    gameLoop.state = "gameOver"
    gameLoop.stateBeforePause = None
    gameLoop.stateAfterAnimation = "gameOver"
    #gameLoop.hoverButton = 0

    result = gameLoop.handleClick(endExittButton)

    assert result == BUTTON_END_HOVER_EXIT

def test_getBoardCoords():
    selectedPiece = []
    boardUpperLeftCoords = (139, 37)
    boardSpacing = 82
    graphicsBackend = testingGraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = testingGameLoop(graphicsBackend,
                                 selectedDifficultyButton, playerName)

    for i in range(8):
        for j in range(8):
            selectedPiece.append((i, j))

    for i in range(len(selectedPiece)):
        coord = selectedPiece[i]
        pixelPosition = (coord[0] * boardSpacing + boardUpperLeftCoords[0],
              coord[1] * boardSpacing + boardUpperLeftCoords[1])

        result = gameLoop.getBoardCoords(pixelPosition)
        assert result == selectedPiece[i]
