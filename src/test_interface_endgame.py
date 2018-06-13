from GameLoop import *

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
            except gameRestartException:
                continue
        
if __name__ == "__main__": main()
