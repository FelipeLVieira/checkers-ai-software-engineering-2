from GameLoop import *

class FakeAIPlayer(AI.AIPlayer):
    def __init__(self):
        pass

    def play(self):
        return

class TestingGameLoop(GameLoop):
    def __init__(self, graphicsBackend, difficultyLevel, playerName, boardDesc):
        GameLoop.__init__(self, graphicsBackend, difficultyLevel, playerName)
        self.board = Board(boardDesc)
        self.graphics = Graphics(graphicsBackend, self.board, playerName)
        self.aiPlayer = FakeAIPlayer()

    def mainLoop(self):
        while self.state == "playerTurn" or self.state == "anim":
            self.states[self.state]()
            self.updateMainGame()
            if self.exitedGame: return

    def playerTurnEventLoop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminateGame()

            elif event.type == pygame.MOUSEMOTION:
                self.updateMousePos(event.pos)

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
]

def main():
    graphicsBackend = GraphicsBackend()
    for board in boardList:
        game = TestingGameLoop(graphicsBackend, 2, "", board).mainLoop()
        clearScreen(graphicsBackend)
    print("\n\nAll tests done. Exiting.")
        
def clearScreen(graphicsBackend):
    graphicsBackend.screen.fill(pygame.Color(0, 0, 0))
    pygame.display.flip()
    graphicsBackend.clock.tick(5)

if __name__ == "__main__": main()
