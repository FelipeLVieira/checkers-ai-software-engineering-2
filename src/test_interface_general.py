from GameLoop import *
import Title
import sys
import TitleGraphics

class TestingTitle(Title.Title):
    def __init__(self, graphicsBackend):
        self.graphicsBackend = graphicsBackend
        self.titleGraphics = TitleGraphics.TitleGraphics(self.graphicsBackend)
        
        # Editable text parameters
        self.playerName = ""
        self.cursorPos = -1
        
        # Other stuff
        
        # The button currently being hovered
        self.hoverButton = None
        # The difficulty level selected. From 0 to 2, starts at 1.
        self.selectedDifficultyButton = 1



class TestingGameLoop(GameLoop):
    def __init__(self, graphicsBackend, difficultyLevel, playerName, boardDesc):
        GameLoop.__init__(self, graphicsBackend, difficultyLevel, playerName)
        self.board = Board(boardDesc)
        self.graphics = Graphics(graphicsBackend, self.board, playerName)
        self.aiPlayer = AI.AIPlayer(self.board, RED, difficultyLevel)

    def mainLoop(self, numTurns=None):
        while True:
            self.states[self.state]()
            self.updateMainGame()
            if self.exitedGame: return


boardList = [
        ([
        "# # # # ",
        " # # # #",
        "# # # # ",
        " # # # #",
        "# #r# # ",
        "w#w#w#w#",
        "#w#w#w#w",
        "w#w#w#w#"
        ], 2),
]

def main():
    graphicsBackend = GraphicsBackend()
    for board in boardList:
        while True:
            try:
                game = TestingGameLoop(graphicsBackend, 2, "", board[0]).mainLoop(
                        board[1])
                break
            except gameRestartException:
                continue
    TestingTitle(graphicsBackend).titleLoop()
        
if __name__ == "__main__": main()
