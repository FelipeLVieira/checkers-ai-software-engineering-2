import pygame, sys
from src.Graphics import Graphics
from src.Board import Board
from src.Constants import *
from pygame.locals import *

pygame.font.init()


class GameLoop:
    def __init__(self):

        self.graphics = Graphics()
        self.board = Board()

        self.turn = BLUE
        self.selectedPiece = None
        self.hop = False
        self.selectedLegalMoves = []

        self.done = False

    def setup(self):
        self.graphics.setupWindow()

    def eventLoop(self):
        self.mousePos = self.graphics.boardCoords(pygame.mouse.get_pos())  # what square is the mouse in?
        for event in pygame.event.get():
            # ESC encerra o jogo (temporário)
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.terminateGame()

            if event.type == pygame.MOUSEBUTTONDOWN:
                boardLocation = self.board.location(self.mousePos)
                if boardLocation.occupant !=  None and boardLocation.occupant.color == boardLocation.occupant.getPlayerColor():
                    self.selectedPiece = self.mousePos





    def update(self):
        self.graphics.updateDisplay(self.board, self.selectedLegalMoves, self.selectedPiece)
        pygame.display.flip()

    def endTurn(self):
        if self.checkForEndgame():
            return True

    def checkForEndgame(self):
        return True

    def terminateGame(self):
        pygame.quit()
        sys.exit()

    def main(self):
        self.setup()

        print(self.board.matrix)
        while True:
            self.eventLoop()
            self.update()


def main():
    game = GameLoop()
    game.main()

if __name__ == "__main__":
    main()
