from GameLoop import *

class FakeAIPlayer(AI.AIPlayer):
    def play():
        return

class TestingGameLoop(GameLoop):
    def __init__(self, graphicsBackend, difficultyLevel, playerName, boardDesc):
        GameLoop.__init__(self, graphicsBackend, difficultyLevel, playerName)
        self.board = Board(boardDesc)
        self.graphics = Graphics(graphicsBackend, self.board, playerName)
        self.aiPlayer = AI.AIPlayer(self.board, RED, difficultyLevel)

    def mainLoop(self):
        for i in self.board.boardToStrings():
            print(i)
        while self.state == "playerTurn" or self.state == "anim":
            self.states[self.state]()
            self.updateMainGame()
            if self.exitedGame: return

boardList = [
        [
        "#r#r#r#r",
        "r#r#r#r#",
        "#r#r#r#r",
        " # # # #",
        "# # # # ",
        "w#w#w#w#",
        "#w#w#w#w",
        "w#w#w#w#"
        ],
        [
        "#r#r#r#r",
        "r#r#r#r#",
        "#r#r# #r",
        " # #r# #",
        "# #w# # ",
        "w# #w#w#",
        "#w#w#w#w",
        "w#w#w#w#"
        ],
        [
        "#r#r#r#r",
        "r#r#r#r#",
        "# #r# #r",
        " #r#r# #",
        "# #w# # ",
        "w# #w#w#",
        "#w#w#w#w",
        "w#w#w#w#"
        ],
        [
        "#r#r#r#r",
        "r#r#r#r#",
        "#r# # #r",
        " # #r# #",
        "# # # # ",
        "w#r#w#w#",
        "#w#w#w#w",
        "w#w#w#w#"
        ],
        [
        "#r#r#r#r",
        "r#r#r#r#",
        "# # # #r",
        " #r# # #",
        "# # # # ",
        "w#r#r#w#",
        "#w#w# #w",
        "w#w#w#w#"
        ],
        [
        "#r#r#r# ",
        "r#r#r#r#",
        "#r#r# #r",
        " # #r# #",
        "# # # # ",
        "w#r#w#w#",
        "# #w#w#w",
        "W#w#w#w#"
        ],
        [
        "#r#r#r#r",
        "r#r#r#r#",
        "#r#r# #r",
        " # #r# #",
        "# # # # ",
        " # # # #",
        "#r# # # ",
        "W# # # #"
        ],
        [
        "#r#r#r#r",
        " # # # #",
        "# # # # ",
        " # # # #",
        "# #W# # ",
        " # # # #",
        "# # # # ",
        " # # # #"
        ],
]

def main():
    graphicsBackend = GraphicsBackend()
    for board in boardList:
        game = TestingGameLoop(graphicsBackend, 2, "", board).mainLoop()
        clearScreen(graphicsBackend)
    print("\n\nAll tests done. Exiting.")
        
def clearScreen(graphicsBackend):
    graphicsBackend.clock.tick(2.5)
    graphicsBackend.screen.fill(pygame.Color(0, 0, 0))
    pygame.display.flip()
    graphicsBackend.clock.tick(5)

if __name__ == "__main__": main()
