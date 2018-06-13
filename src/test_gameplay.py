from GameLoop import *

class TestingGameLoop(GameLoop):
    def __init__(self, graphicsBackend, difficultyLevel, playerName, boardDesc):
        GameLoop.__init__(self, graphicsBackend, difficultyLevel, playerName)
        self.board = Board(boardDesc)
        self.graphics = Graphics(graphicsBackend, self.board, playerName)
        self.aiPlayer = AI.AIPlayer(self.board, RED, difficultyLevel)
        self.numTurnsLeft = None

    def mainLoop(self, numTurns):
        self.numTurnsLeft = numTurns
        while (((self.state == "playerTurn" or self.state == "AITurn") and self.numTurnsLeft > 0) or self.state == "anim"):
            self.states[self.state]()
            self.updateMainGame()
            if self.exitedGame: return

    def endTurn(self):
        self.numTurnsLeft -= 1
        if self.checkForEndgame():
            return False
        if self.board.playerTurn is WHITE:
            self.board.playerTurn = RED
        else:
            self.board.playerTurn = WHITE
        return True
        

boardList = [
        ([
        "#r#r#r#r",
        "r#r#r#r#",
        "#r#r#r#r",
        " # # # #",
        "# # # # ",
        "w#w#w#w#",
        "#w#w#w#w",
        "w#w#w#w#"
        ], 2),
        ([
        "#r#r#r#r",
        "r#r#r#r#",
        "# #r#r#r",
        " # # # #",
        "# #r# # ",
        "w#w#w#w#",
        "#w#w#w#w",
        "w#w#w#w#"
        ], 2),
        ([
        "#r#r#r#r",
        "r#r#r#r#",
        "#r# # #r",
        " # #r# #",
        "#w# # # ",
        " #w#w#r#",
        "#w#w#w#w",
        "w#w#w#w#"
        ], 2),
        ([
        "#r#r#r#r",
        "r#r#r#r#",
        "# #r#r#r",
        " #r# # #",
        "#w# #w# ",
        " #r#r#w#",
        "#w#w# #w",
        "w# #w#r#"
        ], 2),
        ([
        "#r#r# # ",
        " #r#r# #",
        "# #w# # ",
        " #r# # #",
        "#r#r# # ",
        "w#r#w#w#",
        "#w#w#w#w",
        "w#w# #w#"
        ], 2),
        ([
        "#r#r#r# ",
        "w#r#r# #",
        "#w#R# #r",
        "w# # #r#",
        "# #W# # ",
        "w# # #w#",
        "#w#w# #w",
        "w#w#w#w#"
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
