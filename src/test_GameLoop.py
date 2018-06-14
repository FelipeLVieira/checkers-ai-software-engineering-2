from GameLoop import *
from Constants import *
import Graphics

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
    graphicsBackend = Graphics.GraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = GameLoop(graphicsBackend,
                                 selectedDifficultyButton, playerName)
    # VitinhoCarneiro: Why is this even necessary? handleClick does not handle
    # individual board pieces, just screen regions.
    # And you know, there's a thing called a for loop...
    i = 0
    j = 0
    while i < 8:
        while j < 8:
            selectedPiece.append((i, j))
            j = j + 1
        i = i + 1

    for coord in selectedPiece:
        pixelPosition = (coord[0] * boardSpacing + boardUpperLeftCoords[0],
              coord[1] * boardSpacing + boardUpperLeftCoords[1])

        result = gameLoop.handleClick(pixelPosition)
        assert result == REGION_BOARD

def test_handleClick2():
    pauseButton = (877, 619)
    graphicsBackend = Graphics.GraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = GameLoop(graphicsBackend,
                                 selectedDifficultyButton, playerName)

    result = gameLoop.handleClick(pauseButton)

    assert result == BUTTON_INGAME_HOVER_PAUSE

def test_handleClick3():
    exitButton = (1012, 619)
    graphicsBackend = Graphics.GraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = GameLoop(graphicsBackend,
                                 selectedDifficultyButton, playerName)

    result = gameLoop.handleClick(exitButton)

    assert result == BUTTON_INGAME_HOVER_EXIT

def test_handleClick4():
    pauseContinueButton = (499, 295)
    graphicsBackend = Graphics.GraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = GameLoop(graphicsBackend,
                                 selectedDifficultyButton, playerName)

    gameLoop.stateBeforePause = "playerTurn"
    gameLoop.state = "pause"
    gameLoop.hoverButton = 0

    result = gameLoop.handleClick(pauseContinueButton)

    assert result == BUTTON_PAUSE_HOVER_CONTINUE

def test_handleClick5():
    pauseRestartButton = (499, 362)
    graphicsBackend = Graphics.GraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = GameLoop(graphicsBackend,
                                 selectedDifficultyButton, playerName)

    gameLoop.stateBeforePause = "playerTurn"
    gameLoop.state = "pause"
    gameLoop.hoverButton = 0

    result = gameLoop.handleClick(pauseRestartButton)

    assert result == BUTTON_PAUSE_HOVER_RESTART

def test_handleClick6():
    pauseExitButton = (499, 429)
    graphicsBackend = Graphics.GraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = GameLoop(graphicsBackend,
                                 selectedDifficultyButton, playerName)

    gameLoop.stateBeforePause = "playerTurn"
    gameLoop.state = "pause"
    gameLoop.hoverButton = 0

    result = gameLoop.handleClick(pauseExitButton)

    assert result == BUTTON_PAUSE_HOVER_EXIT

def test_handleClick7():
    endRestartButton = (506, 420)
    graphicsBackend = Graphics.GraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = GameLoop(graphicsBackend,
                                 selectedDifficultyButton, playerName)

    gameLoop.state = "gameOver"
    gameLoop.stateBeforePause = None
    gameLoop.stateAfterAnimation = "gameOver"
    #gameLoop.hoverButton = 0

    result = gameLoop.handleClick(endRestartButton)

    assert result == BUTTON_END_HOVER_RESTART

def test_handleClick8():
    endExittButton = (721, 430)
    graphicsBackend = Graphics.GraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = GameLoop(graphicsBackend,
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
    graphicsBackend = Graphics.GraphicsBackend()
    selectedDifficultyButton = 1
    playerName = ""

    gameLoop = GameLoop(graphicsBackend,
                                 selectedDifficultyButton, playerName)
    # I now see what happened.
    i = 0
    while i < 8:
        j = 0
        while j < 8:
            selectedPiece.append((i, j))
            j = j + 1
        i = i + 1

    i = 0
    for coord in selectedPiece:
        pixelPosition = (coord[0] * boardSpacing + boardUpperLeftCoords[0],
              coord[1] * boardSpacing + boardUpperLeftCoords[1])

        result = gameLoop.getBoardCoords(pixelPosition)
        assert result == selectedPiece[i]
        i = i + 1
