import pygame
import sys
import Graphics
import TitleGraphics

class Title:
    def __init__(self):
       self.graphicsBackend = Graphics.GraphicsBackend()
       self.titleGraphics = TitleGraphics.TitleGraphics(self.graphicsBackend)

       # Editable text parameters
       self.playerName = ""
       self.cursorPos = -1

       # Other stuff
       
       # The button currently being hovered
       self.hoverButton = None
       # The difficulty level selected. From 0 to 4, starts at 2.
       self.selectedDifficultyButton = 2

    def titleLoop(self):
        pygame.key.set_repeat(400, 40)
        while True:
            self.titleGraphics.updateAndDraw(
                    self.selectedDifficultyButton, 
                    self.hoverButton, 
                    self.playerName, 
                    self.cursorPos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.handleHover(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handleClick(event)
                elif event.type == pygame.KEYDOWN:
                    self.handleKeystroke(event)

    def handleHover(self, event):
        for (key, region) in self.titleGraphics.mouseRegions.items():
            if region.collidepoint(event.pos):
                self.hoverButton = key
                return
        self.hoverButton = None
        

    def handleClick(self, event):
        area = None
        for (key, region) in self.titleGraphics.mouseRegions.items():
            if region.collidepoint(event.pos):
                area = key
                break
        if area == None:
            self.cursorPos = -1
            return
        if area == "startButton":
            # The game begins here
            # TODO: Change this to jump to the game loop,
            # passing the relevant parameters.
            pass
        elif area.startswith("diffButton"):
            self.selectedDifficultyButton = int(area[-1:]) - 1
        elif area == "playerNameBox":
            self.updateTextBoxCursor(event.pos)

    def handleKeystroke(self, event):
        if self.cursorPos < 0:
            return
        else:
            self.titleGraphics.cursorDrawFlag = True
            self.titleGraphics.cursorDrawTimer = \
                    self.titleGraphics.cursorBlinkInterval
            if len(event.unicode) > 0 and event.unicode.isprintable():
                #print("captured printable `{}' ({})".format(event.unicode, ord(event.unicode)))
                tempPlayerName = ''.join([
                    self.playerName[:self.cursorPos], 
                    event.unicode, 
                    self.playerName[self.cursorPos:]
                    ])
                if (self.titleGraphics.textObjects["playerName"].fontFace
                        .size(tempPlayerName)[0] <=
                        self.titleGraphics.maxPlayerNameWidth):
                    self.playerName = tempPlayerName
                    self.cursorPos += 1
            elif event.key == pygame.K_BACKSPACE:
                #print("captured K_BACKSPACE")
                if self.cursorPos > 0:
                    self.playerName = ''.join([
                        self.playerName[:self.cursorPos - 1],
                        self.playerName[self.cursorPos:]
                        ])
                    self.cursorPos -= 1
            elif event.key == pygame.K_DELETE:
                if self.cursorPos < len(self.playerName):
                    #print("captured K_DELETE")
                    self.playerName = ''.join([
                        self.playerName[:self.cursorPos],
                        self.playerName[self.cursorPos + 1:]
                        ])
            elif event.key == pygame.K_HOME:
                #print("captured K_HOME")
                self.cursorPos = 0
            elif event.key == pygame.K_END:
                #print("captured K_END")
                self.cursorPos = len(self.playerName)
            elif event.key == pygame.K_LEFT:
                #print("captured K_LEFT")
                if self.cursorPos > 0:
                    self.cursorPos -= 1
            elif event.key == pygame.K_RIGHT:
                #print("captured K_RIGHT")
                if self.cursorPos < len(self.playerName):
                    self.cursorPos += 1
            
    def updateTextBoxCursor(self, clickPos):
        textElement = self.titleGraphics.textObjects["playerName"]
        relativePos = clickPos[0] - textElement.getSurfaceOrigin(
                textElement.coords)[0]
        chosenPos = -1
        minError = 9999
        for pos in range(len(self.playerName) + 1):
            error = abs(relativePos 
                    - textElement.fontFace.size(self.playerName[:pos])[0])
            if error < minError:
                minError = error
                chosenPos = pos
            else: break
        self.cursorPos = chosenPos



def main():
    title = Title()
    title.titleLoop()

if __name__ == "__main__": main()
