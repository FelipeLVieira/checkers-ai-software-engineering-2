import pygame
from Board import *
import glob
import math
import sys
import copy
from Constants import *

pygame.font.init()


class Graphics:
    def __init__(self, board):
        self.caption = WINDOW_CAPTION

        self.fps = 60
        self.clock = pygame.time.Clock()

        self.windowWidth = 1280
        self.windowHeight = 720
        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.boardSize = 655
        self.squareSize = int(round(self.boardSize / 8))
        self.pieceSize = int(round(self.squareSize / 2))

        self.message = False

        self.board = copy.deepcopy(board)
        self.auxBoard = None

        # Assets
        self.background = Graphic("../assets/images/bg-game.png")
        self.selMoveMarkerPath = "../assets/images/highlight-possible_spot_marker-"
        self.kingWhitePiece = Graphic("../assets/images/king_marker-white_piece.png")
        self.kingRedPiece = Graphic("../assets/images/king_marker-red_piece.png")
        self.redPiece = Graphic("../assets/images/piece-red.png")
        self.whitePiece = Graphic("../assets/images/piece-white.png")
        self.redPieceHover = Graphic("../assets/images/piece-red-hover.png")
        self.whitePieceHover = Graphic("../assets/images/piece-white-hover.png")
        self.ingameButtonHover = Graphic("../assets/images/highlight-ingame_buttons-hover-f5.png")
        self.pauseButtonHover = Graphic("../assets/images/highlight-pause_menu-button-hover.png")
        self.pauseOverlay = Graphic("../assets/images/overlay-pause.png")

        # Coordinates
        self.pauseButtonCoords = (877, 619)
        self.exitButtonCoords = (1012, 619)
        self.upperScoreBaselineCoords = (988, 250)
        self.lowerScoreBaselineCoords = (988, 520)
        self.turnTextBaselineCoords = (988, 330)
        self.upperNameBaselineCoords = (988, 60)
        self.lowerNameBaselineCoords = (988, 580)
        self.pauseBannerBaselineCoords = (640, 224)
        self.pauseContinueBaselineCoords = (640, 340)
        self.pauseRestartBaselineCoords = (640, 400)
        self.pauseExitBaselineCoords = (640, 460)
        self.pauseContinueButtonCoords = (499, 295)
        self.pauseRestartButtonCoords = (499, 362)
        self.pauseExitButtonCoords = (499, 429)

        self.boardUpperLeftCoords = (138, 36)

        # Other values
        self.boardSpacing = 82
        self.pieceBaseMoveSpeed = 224

        # UI object containers
        self.textObjects = 
                {"upperName": TextElement(OPPONENT_NAME, upperNameBaselineCoords,
                alignment=FONT_ALIGN_CENTER),
                "lowerName": TextElement(PLAYER_NAME_DEFAULT, 
                lowerNameBaselineCoords, alignment=FONT_ALIGN_CENTER),
                "turnText": DynamicTextElement(TURNSTRING.format(1), 
                turnTextBaselineCoords, alignment=FONT_ALIGN_CENTER),
                "upperScore": DynamicTextElement("12", upperScoreBaselineCoords,
                alignment=FONT_ALIGN_CENTER, fontSize=100, fontFace=
                "../assets/fonts/NimbusSansNarrow-Bold.otf"),
                "lowerScore": DynamicTextElement("12", lowerScoreBaselineCoords,
                alignment=FONT_ALIGN_CENTER, fontSize=100, fontFace=
                "../assets/fonts/NimbusSansNarrow-Bold.otf"),
                }

        self.pauseTextObjects =
                {"pauseBanner": TextElement(PAUSE_BANNER, 
                pauseBannerBaselineCoords, alignment=FONT_ALIGN_CENTER),
                "pauseContinue": TextElement(PLAYER_NAME_DEFAULT, 
                pauseContinueBaselineCoords, alignment=FONT_ALIGN_CENTER),
                "pauseRestart": TextElement(PLAYER_NAME_DEFAULT, 
                pauseRestartBaselineCoords, alignment=FONT_ALIGN_CENTER),
                "pauseExit": TextElement(PLAYER_NAME_DEFAULT, 
                pauseExitBaselineCoords, alignment=FONT_ALIGN_CENTER)
                }

        self.UIButtonsHoverCoords =
                {BUTTON_INGAME_HOVER_NONE: None,
                BUTTON_INGAME_HOVER_PAUSE: self.pauseButtonCoords,
                BUTTON_INGAME_HOVER_EXIT: self.exitButtonCoords
                }

        self.pauseButtonsHoverCoords =
                {BUTTON_PAUSE_HOVER_NONE: None,
                BUTTON_PAUSE_HOVER_CONTINUE: pauseContinueButtonCoords,
                BUTTON_PAUSE_HOVER_RESTART: pauseRestartButtonCoords,
                BUTTON_PAUSE_HOVER_EXIT: pauseExitButtonCoords
                }

        self.selMoveAnimations = [[None] * 8] * 8
        
        self.movingPiece = None
        self.maskedPiece = None

    def setupWindow(self):
        pygame.init()
        pygame.display.set_caption(self.caption)


"""
    def updateMainGameDisplay(self, board, legalMovements, selectedPiece, playerTurn):

        """ 

        """
        This updates the current display.
        """ 

        """

        self.screen.blit(self.background, (0, 0))

        board.drawBoardPieces(self.screen, self.redPiece, self.whitePiece)
        board.highlightLegalMoves(legalMovements, selectedPiece, self.screen, self.redHoverPiece, self.whiteHoverPiece, playerTurn)
        board.drawBoardKings(self.screen, self.kingWhitePiece, self.kingRedPiece)

        if self.message:
            self.screen.blit(self.text_surface_obj, self.text_rect_obj)

        pygame.display.update()
        self.clock.tick(self.fps)


    def draw_message(self, message):

        """

        """
        Draws message to the screen.
        """ 

        """
        self.message = True
        self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
        self.text_surface_obj = self.font_obj.render(message, True, HIGH, BLACK)
        self.text_rect_obj = self.text_surface_obj.get_rect()
        self.text_rect_obj.center = (self.windowSize / 2, self.windowSize / 2)
"""

    def registerMove(newBoard, movement, eatenPieces):
        pieceColor = self.board.location(movement[0]).occupant.color
        self.maskedPiece = movement[0]
        path = [PathNode(movement[0], 1)]
        # The path always begins as an arc of length zero
        arcing = True
        nextCoord = None
        # The arc length expresses how many squares are jumped in the arc;
        # this is used to calculate the actual movement speed
        arcLength = 0
        for coord in movement:
            if coord not in eatenPieces:
                if not arcing:
                    # Exit the capture node with a decelerated movement
                    appendNode(path, coord, False, True, 1)
                    # Start an arc - an arc is a node that jumps over multiple
                    # coordinates
                    arcing = True
                    arcLength = 0
                else:
                    # Continue the arc
                    arcLength += 1
                    nextCoord = coord
            else:
                if arcing and arcLength > 0:
                    # End the current arc before adding the capture node
                    appendNode(path, nextCoord, True, True, arcLength)
                    arcing = False

                event = pygame.event.Event(pygame.USEREVENT, 
                        eventType=EVENT_PIECE_VANISH, coords=coord)
                appendNode(path, coord, True, False, 1, event)

        # End an unfinished arc
        if arcing and arcLength > 0:
            event = pygame.event.Event(pygame.USEREVENT,
                    eventType=EVENT_PATH_END)
            appendNode(path, nextCoord, True, True, arcLength)

        # Instance the moving piece
        if pieceColor is RED:
            self.movingPiece = (self.redPiece, EasingMotion(path))
        elif pieceColor is WHITE:
            self.movingPiece = (self.whitePiece, EasingMotion(path))
        else:
            raise RuntimeError("Graphics.py::Graphics:registerMove: invalid piece color `{}'.".format(pieceColor))

        self.auxBoard = copy.deepcopy(newBoard)


    def endPath(self):
        self.maskedPiece = None
        self.movingPiece = None
        self.board = self.auxBoard

    def updateAndDraw(self, hoverPiece, selectedPiece, boardHoverCoords, 
            hoverButton, gamePaused, isPlayerTurn, timeDelta):
        self.background.blitAt(self.screen, (0, 0))
        self.drawBoardPieces()
        self.updateAndDrawPossibleMoves(gamePaused)
        self.updateAndDrawMovingPiece(gamePaused, timeDelta)
        self.drawHoverPiece(hoverPiece)
        self.drawHoverButton(hoverButton)
        self.updateAndDrawSidebarText(currentTurn)
        if gamePaused: self.drawPauseMenu(hoverButton)
        

    def drawBoardPieces(self):
        for col in range(8):
            for row in range(8):
                if self.board.matrix[col][row].occupant is not None:
                    if self.maskedPiece == (col, row): continue
                    if self.board.matrix[col][row].occupant.color is RED:
                        self.redPiece.blitAt(self.screen, 
                                mapToScrCoords((col, row)))

                        if self.board.matrix[col][row].occupant.king:
                            self.kingRedPiece.blitAt(self.screen,
                                    mapToScrCoords((col, row)))

                    elif self.board.matrix[col][row].occupant.color is WHITE:
                        self.whitePiece.blitAt(self.screen, 
                                mapToScrCoords((col, row)))

                        if self.board.matrix[col][row].occupant.king:
                            self.kingwhitePiece.blitAt(self.screen,
                                    mapToScrCoords((col, row)))

                    else: raise RuntimeError("Graphics.py::Graphics:drawBoardPieces: Invalid piece color `{}'".format(self.board.matrix[col][row].occupant.color))

    def setPossibleMoves(self, selPossibleMoves):
        for path in selPossibleMoves:
            for coord in path:
                if coord is not None 
                        and lookup(self.selMoveAnimations, coord) is None
                        and not board.location(coord).occupant:
                    lookup(self.selMoveAnimations, coord) = AnimatedGraphic(
                            self.selMoveMarkerPath, 1)
    
    def clearPossibleMoves(self):
        for col in self.selMoveAnimations:
            for cell in col:
                cell = None
    
    def updateAndDrawPossibleMoves(self, gamePaused):
        for x in range(8):
            for y in range(8):
                if not gamePaused: self.selMoveAnimations[x][y].update()
                self.selMoveAnimations[x][y].blitAt(self.screen, 
                        mapToScrCoords((x, y)))

    def updateAndDrawMovingPiece(self, gamePaused, timeDelta):
        if self.movingPiece is tuple:
            if not gamePaused:
                self.movingPiece[1].update(timeDelta)
            self.movingPiece[0].blitAt(self.screen,
                    self.movingPiece[1].currentPos)

    def drawHoverPiece(self, hoverPiece):
        if hoverPiece is tuple and board.location(hoverPiece).occupant:
            if board.location(hoverPiece).occupant.color is RED:
                self.redPieceHover.blitAt(self.screen, mapToScrCoords(hoverPiece))

            elif board.location(hoverPiece).occupant.color is WHITE:
                self.whitePieceHover.blitAt(self.screen, mapToScrCoords(hoverPiece))

            else: raise RuntimeError("Graphics.py::Graphics:drawHoverPiece: Invalid piece color `{}'".format(board.location(hoverPiece).occupant.color)

    def drawHoverButton(self, hoverButton):
        if hoverButton in self.UIButtonsHoverCoords:
            self.ingameButtonHover.blitAt(self.screen, 
                    self.UIButtonsHoverCoords[hoverButton])
        else: raise RuntimeError("Graphics.py::Graphics:drawHoverPiece: Invalid UI button `{}'".format(hoverButton))

    def updateAndDrawSidebarText(self, isPlayerTurn):
        if isPlayerTurn:
            #turnNumber = self.board.turnNumber
            turnNumber = 1
            self.textObjects["turnText"].update(TURNSTRING.format(turnNumber))
        else:
            self.textObjects["turnText"].update(WAITSTRING)
        #self.textObjects["upperScore"].update(str(12 - self.board.whiteCounterAux))
        #self.textObjects["lowerScore"].update(str(12 - self.board.redCounterAux))
        self.textObjects["upperScore"].update(str(12 - 0))
        self.textObjects["lowerScore"].update(str(12 - 0))
        for o in self.textObjects:
            o.blitAt(self.screen)

    def drawPauseMenu(self, hoverButton):
        pauseOverlay.blitAt(self.screen, (0, 0))
        for o in pauseTextObjects:
            o.blitAt(self.screen)
        
        if hoverButton in pauseButtonsHoverCoords:
            pauseButtonHover.blitAt(self.screen, 
                    pauseButtonsHoverCoords[hoverButton])
        else: raise RuntimeError(
                "Graphics.py::Graphics:drawPauseMenu: Invalid pause button `{}'".format(hoverButton))


def appendNode(path, coord, accelerated, decelerated, moveLength,  event=None):
    speed = self.pieceBaseMoveSpeed * (moveLength ** 0.5)
    path.append(PathNode(coord, speed, accelerate=accelerated, 
        decelerate=decelerated, eventOnComplete=event))


def lookup(matrix, index):
    """Looks up an index, defined by a tuple, in a multidimensional array."""
    result = matrix
    for i in index:
        result = result[i]
    return result

def mapToScrCoords(coords):
    """Maps board coordinates to screen coordinates."""
    return (coords[0] * self.boardSpacing + self.boardUpperLeftCoords[0], 
            coords[1] * self.boardSpacing + self.boardUpperLeftCoords[1])

class Graphic:
    """Implements a graphic object that caches an image surface."""
    surface = None

    def __init__(self, path):
        self.surface = pygame.image.load(path)

    def blitAt(self, surface, coords):
        """Blits this graphic's surface over another surface."""
        if coords is not None: surface.blit(self.surface, coords)

    def update(self):
        """A stub for abstraction purposes, does nothing."""
        pass


class AnimatedGraphic(Graphic):
    """Implements an animated graphic object."""
    surfaces = None
    frameDelay = None
    frameDelayCounter = None
    frame = None
    looping = None

    def __init__(self, path, frameDelay, loop=False):
        paths = sorted(glob.glob(path))
        print(paths)
        self.surfaces = list(map(pygame.image.load, paths))
        self.frameDelay = frameDelay
        self.frameDelayCounter = frameDelay
        self.frame = 0
        self.looping = loop
        Graphic.__init__(self, paths[1])

    def update(self):
        """Updates the animation. Must be called every frame."""
        if self.looping or not self.frame >= len(self.surfaces):
            self.frameDelayCounter -= 1
            if not self.frameDelayCounter > 0:
                self.frameDelayCounter = self.frameDelay
                self.frame += 1
                if self.frame >= len(self.surfaces):
                    self.frame = 0
                self.surface = self.surfaces[self.frame]


class Motion:
    """A basic class for controlling movement of graphics.
       It supports linear interpolation, paths with multiple nodes, and can
       fire Pygame events whenever a specific node is reached."""

    # A list of path nodes.
    # The starting node's speed and event are ignored.
    # Acceleration and deceleration are ignored for all nodes.
    path = None

    # The object (list) that contains this Motion instance. Used in order to 
    # destroy itself after the movement has been completed.
    container = None

    coord1 = None
    coord2 = None
    # currentSpeed is indicated in average percentage of completion per second.
    currentSpeed = None
    nodeCompletion = None
    accelerate = None
    decelerate = None
    
    #-----------------------------------------------------------------------+
    # This parameter holds the motion path's current position. This is what |
    # should be read to obtain the updated position every frame.            |
    #-----------------------------------------------------------------------+
    currentPos = None

    nextEvent = None

    hasCompleted = False

    def __init__(self, path):
        self.path = path
        self.coord1 = path[0].coords
        self.coord2 = path[0].coords
        self.currentSpeed = 0.0
        self.nodeCompletion = 1.0
        self.currentPos = self.coord2
        self.path.pop(0)

    def update(self, timeDelta=1.0 / 60):
        """Updates the movement coordinates."""
        if self.hasCompleted: return

        self.nodeCompletion += self.currentSpeed * timeDelta

        if self.nodeCompletion >= 1.0:
            self.loadNextNode()
            self.nodeCompletion -= 1.0

        self.currentPos = self.calcPosition()

    def calcPosition(self):
        """Calculates the position for the current movement state."""
        return self.coord2 * self.nodeCompletion + self.coord1 * (1.0 - self.nodeCompletion)

    def loadNextNode(self):
        """Loads the next node in the path, consuming it. Also fires the
           current node's event, if there's any."""
        if self.nextEvent is not None: pygame.event.post(self.nextEvent)

        self.coord1 = self.coord2

        if len(self.path) == 0:
            self.hasCompleted = True
            self.nodeCompletion = 1.0
        else:
            node = self.path.pop(0)
            self.coord2 = node.coords
            if(self.coord1 == self.coord2): self.currentSpeed = 1.0
            else: 
                self.currentSpeed = node.speed / euclideanDist(self.coord1, self.coord2)
            self.accelerate = node.accelerate
            self.decelerate = node.decelerate
            self.nextEvent = node.eventOnComplete


class PathNode:
    """Represents a node in a movement path.
       Speed is represented in average pixels per second."""
    coords = None
    speed = None
    eventOnComplete = None
    accelerate = None
    decelerate = None

    def __init__(self, coords, speed, eventOnComplete=None, accelerate=False, decelerate=False):
        self.coords = coords
        self.speed = speed
        self.eventOnComplete = eventOnComplete
        self.accelerate = accelerate
        self.decelerate = decelerate


class EasingMotion(Motion):
    """Subclass of Motion with support for accelerated/decelerated movement
       using quadratic interpolation."""

    def __init__(self, path):
        Motion.__init__(self, path)

    def calcPosition(self):
        """Calculates the position in the current movement state, using
           quadratic interpolation and the accelerate/decelerate flags."""
        # Case 1: acceleration only
        if self.accelerate and not self.decelerate:
            return (self.coord2[0] * (self.nodeCompletion ** 2) + 
                    self.coord1[0] * (1.0 - (self.nodeCompletion ** 2)),
                    self.coord2[1] * (self.nodeCompletion ** 2) + 
                    self.coord1[1] * (1.0 - (self.nodeCompletion ** 2)))


        # Case 2: deceleration only
        if self.decelerate and not self.accelerate:
            return (self.coord2[0] * (1.0 - ((1.0 - self.nodeCompletion) ** 2))
                  + self.coord1[0] * ((1.0 - self.nodeCompletion) ** 2), 
                    self.coord2[1] * (1.0 - ((1.0 - self.nodeCompletion) ** 2))
                  + self.coord1[1] * ((1.0 - self.nodeCompletion) ** 2))


            # Case 3: acceleration and deceleration
        if self.decelerate and self.accelerate:
            # This function is decomposed into two quadratic curves. 1st half:
            if (self.nodeCompletion < 0.5):
                return (self.coord2[0] * (2.0 * self.nodeCompletion ** 2) / 2.0 + 
                        self.coord1[0] * (1.0 - ((2.0 * self.nodeCompletion) ** 2) / 2.0),
                        self.coord2[1] * (2.0 * self.nodeCompletion ** 2) / 2.0 + 
                        self.coord1[1] * (1.0 - ((2.0 * self.nodeCompletion) ** 2) / 2.0))

            # 2nd half:
            else:
                return (self.coord2[0] * (1.0 - (2.0 * (1.0 - self.nodeCompletion) ** 2 / 2.0))
                      + self.coord1[0] * (2.0 * (1.0 - self.nodeCompletion) ** 2 / 2.0), 
                        self.coord2[1] * (1.0 - (2.0 * (1.0 - self.nodeCompletion) ** 2 / 2.0))
                      + self.coord1[1] * (2.0 * (1.0 - self.nodeCompletion) ** 2 / 2.0))


        # Case 4: linear motion (not accelerated or decelerated)
        return Motion.calcPosition(self)

class TextElement:
    fontFace = None
    alignment = None
    text = None
    surface = None
    color = None
    coords = None
    
    def __init__(self, text, coords, fontFace="../assets/fonts/Cantarell-Regular.otf", fontSize=36, alignment=FONT_ALIGN_LEFT, color=pygame.Color(255, 255, 255, 255)):
        if(alignment < 0 or alignment > 2): raise RuntimeError("TextElement @__init__: Invalid alignment type `{}'".format(alignment))
        self.fontFace = pygame.font.Font(fontFace, fontSize)
        self.alignment = alignment
        self.text = text
        self.color = color
        self.coords = coords
        self.render()

    def blitAt(self, surface, coords=None):
        if coords is None: coords = self.coords 
        surface.blit(self.surface, self.getSurfaceOrigin(coords))

    def render(self):
        self.surface = self.fontFace.render(self.text, True, self.color)

    def getSurfaceOrigin(self, coords):
        if(self.alignment == FONT_ALIGN_LEFT):
            return (coords[0], coords[1] - self.fontFace.get_linesize())
        elif(self.alignment == FONT_ALIGN_RIGHT):
            return (coords[0] - self.surface.get_width(), coords[1] - self.fontFace.get_linesize())
        else:
            return (coords[0] - (self.surface.get_width() / 2), coords[1] - self.fontFace.get_linesize())

    def update(self, value=None, newCoords=None):
        if newCoords is tuple: self.coords = newCoords

class DynamicTextElement(TextElement):
    def __init__(self, initialValue, coords, fontFace="../assets/fonts/Cantarell-Regular.otf", fontSize=36, alignment=FONT_ALIGN_LEFT, color=pygame.Color(255, 255, 255, 255)):
        TextElement.__init__(self, initialValue, coords, fontFace, fontSize, alignment, color)

    def update(self, newValue, newCoords=None):
        if newValue != self.text:
            self.text = newValue
            self.render()
        if newCoords is tuple: self.coords = newCoords

def euclideanDist(coord1, coord2):
    """Returns the euclidean distance of two coordinates - (x, y) tuples"""
    return math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)

def main():
    graphics = Graphics()
    graphics.setupWindow()
    text = TextElement("Hey! Listen!", (100, 100))
    count = DynamicTextElement("0", (500, 100), fontFace="../assets/fonts/NimbusSansNarrow-Bold.otf", fontSize=50, alignment=FONT_ALIGN_CENTER)
    graphic = Graphic("../assets/images/piece-white.png")
    graphic2 = Graphic("../assets/images/piece-red.png")
    animation1 = AnimatedGraphic("../assets/images/highlight-possible_spot_marker-f*", 1, loop=True)
    animation2 = AnimatedGraphic("../assets/images/highlight-possible_spot_marker-f*", 2, loop=True)
    motion = EasingMotion([PathNode((232, 368), 0), PathNode((300, 300), 650, pygame.event.Event(pygame.USEREVENT), accelerate=True), PathNode((368, 232), 650, None, decelerate=True)])
    text.blitAt(graphics.screen)
    pygame.display.update()
    pygame.display.flip()
    counter = 0
    pieceDestroyed = False
    while(True):
        timeDelta = graphics.clock.tick(graphics.fps) / 1000.0
        counter += 1
        count.update(str(counter))
        animation1.update()
        animation2.update()
        motion.update(timeDelta)

        graphics.screen.fill((0, 0, 0))
        text.blitAt(graphics.screen)
        count.blitAt(graphics.screen)
        if not pieceDestroyed: graphic.blitAt(graphics.screen, (300, 300))
        graphic2.blitAt(graphics.screen, motion.currentPos)
        animation1.blitAt(graphics.screen, (300, 500))
        animation2.blitAt(graphics.screen, (400, 500))

        pygame.display.update()
        pygame.display.flip()
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            if(event.type == pygame.USEREVENT):
                pieceDestroyed = True
            

if __name__ == "__main__": main()
