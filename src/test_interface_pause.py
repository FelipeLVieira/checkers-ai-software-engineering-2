from GameLoop import *

class TestingGameLoop(GameLoop):
    def __init__(self, graphicsBackend, difficultyLevel, playerName, boardDesc):
        GameLoop.__init__(self, graphicsBackend, difficultyLevel, playerName)
        self.board = Board(boardDesc)
        self.graphics = Graphics(graphicsBackend, self.board, playerName)
        self.aiPlayer = AI.AIPlayer(self.board, RED, difficultyLevel)
        self.graphics.pieceBaseMoveSpeed = 200

    def mainLoop(self, numTurns=None):
        while True:
            self.states[self.state]()
            self.updateMainGame()
            if self.exitedGame: return


boardList = [
        ([
        "#r#r#r#r",
        "r#r#r# #",
        "#r#r#r#r",
        " # # #w#",
        "# #r# # ",
        "w# #w#w#",
        "#r#w# #w",
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
