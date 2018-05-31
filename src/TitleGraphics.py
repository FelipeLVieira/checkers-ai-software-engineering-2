import pygame
from Graphics import *
from Constants import *

class TitleGraphics:
    def __init__(self, graphicsBackend):
        self.fps = graphicsBackend.fps
        self.clock = graphicsBackend.clock
        self.timeDelta = graphicsBackend.timeDelta
        self.windowWidth = graphicsBackend.windowWidth
        self.windowHeight = graphicsBackend.windowHeight
        self.screen = graphicsBackend.screen
        
        # Assets
        self.background = Graphic(
                "../assets/images/bg-mainmenu.png")
        self.diffButtonHover = Graphic(
                "../assets/images/highlight-difficulty_button-hover.png")
        self.diffButtonSelected = Graphic(
                "../assets/images/highlight-difficulty_button-selected.png")
        self.startButtonHover = Graphic(
                "../assets/images/highlight-start_button-click.png")
        
        # Coordinates
        self.title1BaselineCoords = (640, -152)
        self.title2BaselineCoords = (640, -32)
        self.titleLineSpacing = 120
        self.playerNameBaselineCoords = (640, 347)
        self.diffLabelBaselineCoords = (640, 424)
        self.diff1BaselineCoords = (296, 485)
        self.diff2BaselineCoords = (468, 485)
        self.diff3BaselineCoords = (641, 485)
        self.diff4BaselineCoords = (813, 485)
        self.diff5BaselineCoords = (985, 485)
        self.startBaselineCoords = (640, 605)
        self.buttonsHoverCoords = {
                "diffButton1": (222, 441),
                "diffButton2": (394, 441),
                "diffButton3": (567, 441),
                "diffButton4": (739, 441),
                "diffButton5": (911, 441),
                "startButton": (502, 549)
                }
        self.diffButtonsSelectedCoords = [
                (219, 438),
                (391, 438),
                (564, 438),
                (736, 438),
                (908, 438)
                ]
        self.startButtonHoverCoords = (502, 549)

        # Timers, states and flags
        self.cursorBlinkInterval = 0.5
        self.cursorDrawTimer = 0.5
        self.cursorDrawFlag = True
        self.lastDifficultySelected = 0

        # Colors
        self.diffTextColor = pygame.color.Color(80, 80, 80, 128)
        self.selectedDiffTextColor = pygame.color.Color(96, 80, 64, 255)
        
        # Clickable/hoverable regions
        self.mouseRegions = {
                "playerNameBox": pygame.Rect((480, 315), (322, 44)),
                "diffButton1": pygame.Rect(
                    self.buttonsHoverCoords["diffButton1"], (148, 70)),
                "diffButton2": pygame.Rect(
                    self.buttonsHoverCoords["diffButton2"], (148, 70)),
                "diffButton3": pygame.Rect(
                    self.buttonsHoverCoords["diffButton3"], (148, 70)),
                "diffButton4": pygame.Rect(
                    self.buttonsHoverCoords["diffButton4"], (148, 70)),
                "diffButton5": pygame.Rect(
                    self.buttonsHoverCoords["diffButton5"], (148, 70)),
                "startButton": pygame.Rect(
                    self.buttonsHoverCoords["startButton"], (276, 92)),
                }
        
        # Motion paths
        self.titlePath = [
                PathNode((640, -32), 1),
                PathNode((640, 252), 400, accelerate=False, decelerate=True)
                ]
        self.titleMotion = EasingMotion(self.titlePath)
        
        # UI object containers
        self.textObjects = {
                "titleLine1": TextElement(TITLE_LINE1, 
                        self.title1BaselineCoords,
                        alignment=FONT_ALIGN_CENTER, fontSize=120,
                        fontFace = "../assets/fonts/OpenSans-Bold.ttf"),
                "titleLine2": TextElement(TITLE_LINE2, 
                        self.title2BaselineCoords, 
                        alignment=FONT_ALIGN_CENTER, fontSize=120,
                        fontFace = "../assets/fonts/OpenSans-Bold.ttf"),
                "playerName": DynamicTextElement(TITLE_PLAYERNAME_EMPTY, 
                        self.playerNameBaselineCoords, 
                        alignment=FONT_ALIGN_CENTER, fontSize=32, 
                        color=pygame.color.Color(155, 164, 168, 255)),
                "difficultyLabel": TextElement(TITLE_DIFFICULTYLABEL, 
                        self.diffLabelBaselineCoords, 
                        alignment=FONT_ALIGN_CENTER, fontSize=27,
                        fontFace = "../assets/fonts/OpenSans-Bold.ttf"),
                "titleDifficulty1": DynamicTextElement(TITLE_DIFFICULTY1, 
                        self.diff1BaselineCoords, 
                        alignment=FONT_ALIGN_CENTER, fontSize=22,
                        color=self.diffTextColor),
                "titleDifficulty2": DynamicTextElement(TITLE_DIFFICULTY2, 
                        self.diff2BaselineCoords, 
                        alignment=FONT_ALIGN_CENTER, fontSize=22,
                        color=self.diffTextColor),
                "titleDifficulty3": DynamicTextElement(TITLE_DIFFICULTY3, 
                        self.diff3BaselineCoords, 
                        alignment=FONT_ALIGN_CENTER, fontSize=22,
                        color=self.diffTextColor),
                "titleDifficulty4": DynamicTextElement(TITLE_DIFFICULTY4, 
                        self.diff4BaselineCoords, 
                        alignment=FONT_ALIGN_CENTER, fontSize=22,
                        color=self.diffTextColor),
                "titleDifficulty5": DynamicTextElement(TITLE_DIFFICULTY5, 
                        self.diff5BaselineCoords, 
                        alignment=FONT_ALIGN_CENTER, fontSize=22,
                        color=self.diffTextColor),
                "startGame": TextElement(TITLE_START, 
                        self.startBaselineCoords, 
                        alignment=FONT_ALIGN_CENTER, fontSize=30,
                        fontFace = "../assets/fonts/OpenSans-Bold.ttf")
                }

        # Misc
        self.playerNameUnderlineRect = pygame.Rect((480, 355), (322, 2))
        self.maxPlayerNameWidth = 314
    
    def updateAndDraw(self, difficulty, hoverButton, playerName, textCursorPos):
        self.timeDelta = self.clock.tick(self.fps) / 1000.
        #print(self.timeDelta * 1000, "ms")
        self.background.blitAt(self.screen, (0, 0))
        self.drawButtonHover(hoverButton)
        self.drawDifficultySelection(difficulty)
        self.updatePlayerNameAndCursor(playerName, textCursorPos)
        self.drawTextElements()
        pygame.draw.rect(self.screen, pygame.Color(255, 255, 255, 255),
                self.playerNameUnderlineRect)
        self.updateTitle()
        pygame.display.update()
    
    def drawButtonHover(self, hoverButton):
        if hoverButton in self.buttonsHoverCoords:
            if hoverButton == "startButton":
                self.startButtonHover.blitAt(self.screen,
                        self.buttonsHoverCoords[hoverButton])
            else:
                self.diffButtonHover.blitAt(self.screen,
                        self.buttonsHoverCoords[hoverButton])
    
    def drawDifficultySelection(self, difficulty):
        self.diffButtonSelected.blitAt(self.screen,
                self.diffButtonsSelectedCoords[difficulty])
        if difficulty != self.lastDifficultySelected:
            new = self.textObjects[''.join(["titleDifficulty", 
                str(difficulty + 1)])]
            old = self.textObjects[''.join(["titleDifficulty", 
                str(self.lastDifficultySelected + 1)])]
            new.update(newColor=self.selectedDiffTextColor)
            old.update(newColor=self.diffTextColor)
            
    
    def drawTextElements(self):
        for (key, e) in self.textObjects.items():
            e.blitAt(self.screen)
    
    def updateTitle(self):
        self.titleMotion.update(self.timeDelta)
        self.textObjects["titleLine2"].update(
                newCoords=self.titleMotion.currentPos)
        self.textObjects["titleLine1"].update(newCoords=(
                self.titleMotion.currentPos[0],
                self.titleMotion.currentPos[1] - self.titleLineSpacing
                ))

    def updatePlayerNameAndCursor(self, playerName, textCursorPos):
        text = self.textObjects["playerName"]
        if len(playerName) > 0 or textCursorPos >= 0:
            text.update(playerName)
            text.color = pygame.color.Color(255, 255, 255, 255)
        else:
            text.update(TITLE_PLAYERNAME_EMPTY, 
                    newColor = pygame.color.Color(155, 172, 168, 255)) 
        
        self.cursorDrawTimer -= self.timeDelta
        if self.cursorDrawTimer < 0:
            self.cursorDrawTimer = self.cursorBlinkInterval
            self.cursorDrawFlag = not self.cursorDrawFlag
        
        if textCursorPos >= 0 and self.cursorDrawFlag:
            cursorPosRel = text.fontFace.size(text.text[:textCursorPos])[0]
            cursorTop = (text.getSurfaceOrigin(text.coords)[0] + cursorPosRel,
                text.getSurfaceOrigin(text.coords)[1])
            cursorHeight = text.fontFace.get_linesize()
            cursorBottom = (cursorTop[0], cursorTop[1] + cursorHeight)
            pygame.draw.line(self.screen, (255, 255, 255), cursorTop, 
                    cursorBottom)
