from GameLoop import *

class TestingGameLoop(GameLoop):
    def __init__(self, graphicsBackend, difficultyLevel, playerName, boardDesc):
        GameLoop.__init__(self, graphicsBackend, difficultyLevel, playerName)
        self.board = Board(boardDesc)
        self.graphics = Graphics(graphicsBackend, self.board, playerName)
        self.aiPlayer = AI.AIPlayer(self.board, RED, difficultyLevel)

    def mainLoop(self, numTurns=None):
        endGameTime = 1.4
        while (self.state == "playerTurn" or self.state == "AITurn" or self.state == "anim" or self.state == "gameOver") and endGameTime > 0:
            self.states[self.state]()
            if self.state == "gameOver": endGameTime -= self.timeDelta
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
        ([
        "#r#r#r#r",
        "r#r#r#r#",
        "#r#r#r#r",
        " # # # #",
        "# #w# # ",
        " # # # #",
        "# # # # ",
        " # # # #"
        ], 2),
        ([
        "# # # # ",
        " # # # #",
        "# #R# # ",
        " # # # #",
        "# # # # ",
        " # # # #",
        "# #W# # ",
        " # # # #"
        ], 2),
]

def main():
    graphicsBackend = GraphicsBackend()
    for board in boardList:
        game = TestingGameLoop(graphicsBackend, 2, "", board[0]).mainLoop(
                board[1])
        clearScreen(graphicsBackend)
    print("\n\nAll tests done. Exiting.")
        
def clearScreen(graphicsBackend):
    graphicsBackend.clock.tick(2.5)
    graphicsBackend.screen.fill(pygame.Color(0, 0, 0))
    pygame.display.flip()
    graphicsBackend.clock.tick(5)

if __name__ == "__main__": main()
