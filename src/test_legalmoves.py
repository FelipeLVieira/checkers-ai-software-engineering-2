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
        self.graphics.fps = 30
        self.aiPlayer = FakeAIPlayer()

    def mainLoop(self, pieceToClick):
        boardScreenTime = 5.
        clicked = False
        while ((self.state == "playerTurn" or self.state == "anim")
                and boardScreenTime > 0):
            if boardScreenTime < 4.3 and not clicked:
                self.handleBoardClick(pieceToClick)
                clicked = True
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    return
            self.updateMainGame()
            boardScreenTime -= self.timeDelta
            if self.exitedGame: return

    def getBoardCoords(self, pos):
        return pos

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
        ], (4, 5)),
        ([
        "#r#r#r#r",
        "r# #r# #",
        "#r#r# #r",
        " # # # #",
        "# #r# # ",
        "w# #w#w#",
        "#r#w#w#w",
        "w#w#w#w#"
        ], (0, 7)),
        ([
        "#r#r#r#r",
        " #r# #r#",
        "#r#w#r#r",
        " # # # #",
        "#r# #r# ",
        " # # #w#",
        "#r#r#w#w",
        "w#w#w#w#"
        ], (2, 7)),
        ([
        "#r#r#r#r",
        "r# #r#r#",
        "#r#r#r#r",
        " # # # #",
        "# #r#r# ",
        "w# #w# #",
        "#r#w#r#w",
        "w#w# #w#"
        ], (0, 7)),
        ([
        "#r#r#r# ",
        " #r#r# #",
        "# #r# #r",
        " # # # #",
        "# #W# # ",
        "w# # #w#",
        "# #w# #w",
        "w#w#w# #"
        ], (3, 4)),
        ([
        "#r#r#r# ",
        "r#r#r# #",
        "#r#r# #r",
        " # # # #",
        "# # # # ",
        "w# #w#w#",
        "# #w#w#w",
        "W#w#w#w#"
        ], (0, 7))
]

def main():
    graphicsBackend = GraphicsBackend()
    for board in boardList:
        game = TestingGameLoop(graphicsBackend, 2, "", board[0]).mainLoop(
                pieceToClick=board[1])
        clearScreen(graphicsBackend)
    print("\n\nAll tests done. Exiting.")
        
def clearScreen(graphicsBackend):
    graphicsBackend.screen.fill(pygame.Color(0, 0, 0))
    pygame.display.flip()
    graphicsBackend.clock.tick(5)

if __name__ == "__main__": main()
