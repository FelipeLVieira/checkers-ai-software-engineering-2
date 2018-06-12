from GameLoop import *

class TestingGameLoop(GameLoop):
    def __init__(self, graphicsBackend, difficultyLevel, playerName, boardDesc):
        GameLoop.__init__(self, graphicsBackend, difficultyLevel, playerName)
        self.board = Board(boardDesc)
        self.board.playerTurn = RED
        self.graphics = Graphics(graphicsBackend, self.board, playerName)
        self.aiPlayer = AI.AIPlayer(self.board, RED, difficultyLevel)
        self.state = "AITurn"

    def mainLoop(self):
        self.aiPlayer.play()
        while self.state == "AITurn" or self.state == "anim":
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
        "w# # #w#",
        "#w#w#w#w",
        "w#w#w#w#"
        ],
        [
        "#r#r#r#r",
        "r#r#r#r#",
        "#r# #w#r",
        " # # # #",
        "# #w# # ",
        "w# #w#w#",
        "#w#w#w#w",
        "w#w#w#w#"
        ],
        [
        "#r#r#r#r",
        "r#r#r#r#",
        "# # #w#r",
        " #r# # #",
        "# #w# # ",
        "w# #r#w#",
        "#w#w# #w",
        "w#w#w#w#"
        ],
        [
        "#r#r#r# ",
        "r#r#r#w#",
        "#r#r# #r",
        " # #w# #",
        "# # # # ",
        "w#w#w#w#",
        "# #w#w#w",
        "R#w#w#w#"
        ],
        [
        "#r#r#r#r",
        "r#r#r#r#",
        "#r#r# #r",
        " # #w# #",
        "# # #w# ",
        " # # # #",
        "#w# # # ",
        "R# # # #"
        ],
        [
        "#w#w#w#w",
        " # # # #",
        "# # # # ",
        " # # # #",
        "# #R# # ",
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
    graphicsBackend.clock.tick(1)
    graphicsBackend.screen.fill(pygame.Color(0, 0, 0))
    pygame.display.flip()
    graphicsBackend.clock.tick(5)

if __name__ == "__main__": main()
