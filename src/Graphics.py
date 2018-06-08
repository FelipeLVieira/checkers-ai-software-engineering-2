import pygame
from Board import *
import glob
import math
import sys
import copy
from Constants import *

# For testing only
import random


class GraphicsBackend:
    def __init__(self):
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.timeDelta = 0

        self.windowWidth = 1280
        self.windowHeight = 720

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        pygame.display.set_caption(WINDOW_CAPTION)



class Graphics:
    def __init__(self, graphicsBackend, board, playerName):
        self.fps = graphicsBackend.fps
        self.clock = graphicsBackend.clock
        self.timeDelta = graphicsBackend.timeDelta
        self.windowWidth = graphicsBackend.windowWidth
        self.windowHeight = graphicsBackend.windowHeight
        self.screen = graphicsBackend.screen

        self.board = copy.deepcopy(board)
        self.auxBoard = None
        if playerName == "": playerName = PLAYER_NAME_DEFAULT

        # Assets
        self.background = Graphic("../assets/images/bg-game.png")
        self.selMoveMarkerPath = "../assets/images/highlight-possible_spot_marker-f*"
        self.kingWhitePiece = Graphic(
                "../assets/images/king_marker-white_piece.png")
        self.kingRedPiece = Graphic(
                "../assets/images/king_marker-red_piece.png")
        self.redPiece = Graphic("../assets/images/piece-red.png")
        self.whitePiece = Graphic("../assets/images/piece-white.png")
        self.redPieceHover = Graphic("../assets/images/piece-red-hover.png")
        self.whitePieceHover = Graphic(
                "../assets/images/piece-white-hover.png")
        self.redPieceSelected = Graphic(
                "../assets/images/piece-red-select.png")
        self.whitePieceSelected = Graphic(
                "../assets/images/piece-white-select.png")
        self.ingameButtonHover = Graphic(
                "../assets/images/highlight-ingame_buttons-hover-f5.png")
        self.pauseButtonHover = Graphic(
                "../assets/images/highlight-pause_menu-button-hover.png")
        self.pauseOverlay = Graphic("../assets/images/overlay-pause.png")
        self.endOverlay = Graphic("../assets/images/overlay-end.png")
        self.endOverlayButtonHover = Graphic(
                "../assets/images/highlight-end_overlay-button-hover.png")
        self.pieceWithLegalMovesMarkerPath = "../assets/images/highlight-piece_with_legal_moves-f*"

        # Coordinates
        self.pauseButtonCoords = (877, 619)
        self.exitButtonCoords = (1012, 619)
        self.upperScoreBaselineCoords = (980, 256)
        self.lowerScoreBaselineCoords = (980, 524)
        self.turnTextBaselineCoords = (988, 323)
        self.upperNameBaselineCoords = (988, 48)
        self.lowerNameBaselineCoords = (988, 590)
        self.pauseBannerBaselineCoords = (640, 224)
        self.pauseContinueBaselineCoords = (640, 333)
        self.pauseRestartBaselineCoords = (640, 400)
        self.pauseExitBaselineCoords = (640, 467)
        self.pauseContinueButtonCoords = (499, 295)
        self.pauseRestartButtonCoords = (499, 362)
        self.pauseExitButtonCoords = (499, 429)
        self.winLoseBaselineRelCoords = (300, 95)
        self.endRestartBaselineRelCoords = (151, 176)
        self.endExitBaselineRelCoords = (449, 176)
        self.endRestartButtonRelCoords = (12, 136)
        self.endExitButtonRelCoords = (310, 136)


        self.endOverlayTextsRelCoords = {
                "winLoseFanfare": self.winLoseBaselineRelCoords,
                "endRestart": self.endRestartBaselineRelCoords,
                "endExit": self.endExitBaselineRelCoords,
                }

        self.endOverlayButtonsRelCoords = {
                BUTTON_END_HOVER_RESTART: self.endRestartButtonRelCoords,
                BUTTON_END_HOVER_EXIT: self.endExitButtonRelCoords
                }
        
        
        self.boardUpperLeftCoords = (139, 37)
        self.endOverlayFinalCoords = ()
        
        # Screen regions
        self.regions = {
                REGION_BOARD: pygame.Rect(self.boardUpperLeftCoords, (656, 656)),
                BUTTON_INGAME_HOVER_PAUSE: pygame.Rect(
                        self.pauseButtonCoords, (82, 82)),
                BUTTON_INGAME_HOVER_EXIT: pygame.Rect(
                        self.exitButtonCoords, (82, 82))
                }

        self.pauseRegions = {
                BUTTON_PAUSE_HOVER_CONTINUE: pygame.Rect(
                        self.pauseContinueButtonCoords, (279, 54)),
                BUTTON_PAUSE_HOVER_RESTART: pygame.Rect(
                        self.pauseRestartButtonCoords, (279, 54)),
                BUTTON_PAUSE_HOVER_EXIT: pygame.Rect(
                        self.pauseExitButtonCoords, (279, 54))
                }

        self.gameOverRegions = {
                BUTTON_END_HOVER_RESTART: pygame.Rect(
                        tplsum(self.endRestartButtonRelCoords, (640, 360)),
                        (278, 58)),
                BUTTON_END_HOVER_EXIT: pygame.Rect(
                        tplsum(self.endExitButtonRelCoords, (640, 360)),
                        (278, 58)),
                BUTTON_INGAME_HOVER_EXIT: pygame.Rect(
                        self.exitButtonCoords, (82, 82))
                }

        # Other values
        self.boardSpacing = 82
        self.pieceBaseMoveSpeed = 320
        self.endOverlayDimensions = (600, 210)
        
        # Motion paths
        self.endOverlayMotion = EasingMotion([
                PathNode((640, -210), 1),
                PathNode((640, 360), 700, decelerate=True)
                ])
        
        # UI object containers
        self.textObjects = {
                "upperName": TextElement(OPPONENT_NAME, 
                        self.upperNameBaselineCoords, 
                        alignment=FONT_ALIGN_CENTER, fontSize=36),
                "lowerName": TextElement(playerName, 
                        self.lowerNameBaselineCoords, 
                        alignment=FONT_ALIGN_CENTER, fontSize=36),
                "turnText": DynamicTextElement(TURNSTRING.format(1), 
                        self.turnTextBaselineCoords, 
                        alignment=FONT_ALIGN_CENTER, fontSize=32),
                "upperScore": DynamicTextElement("12", 
                        self.upperScoreBaselineCoords,
                        alignment=FONT_ALIGN_CENTER, fontSize=228, fontFace=
                        "../assets/fonts/NimbusSansNarrow-Bold.otf"),
                "lowerScore": DynamicTextElement("12", 
                        self.lowerScoreBaselineCoords,
                        alignment=FONT_ALIGN_CENTER, fontSize=228, fontFace=
                        "../assets/fonts/NimbusSansNarrow-Bold.otf"),
                }
        
        self.endGameTextObjects = {
                "winLoseFanfare": DynamicTextElement("",
                        self.winLoseBaselineRelCoords,
                        alignment=FONT_ALIGN_CENTER, fontSize=75, fontFace=
                        "../assets/fonts/OpenSans-Bold.ttf"),
                "endRestart": TextElement(PAUSE_RESTART,
                        self.endRestartBaselineRelCoords,
                        alignment=FONT_ALIGN_CENTER, fontSize=26,
                        color=pygame.Color(48, 48, 48)),
                "endExit": TextElement(PAUSE_QUIT,
                        self.endExitBaselineRelCoords,
                        alignment=FONT_ALIGN_CENTER, fontSize=26,
                        color=pygame.Color(68, 40, 40))
                }

        self.pauseTextObjects = {
                "pauseBanner": TextElement(PAUSE_BANNER, 
                        self.pauseBannerBaselineCoords, 
                        alignment=FONT_ALIGN_CENTER, fontSize=100, fontFace=
                        "../assets/fonts/OpenSans-Bold.ttf"),
                "pauseContinue": TextElement(PAUSE_CONTINUE, 
                        self.pauseContinueBaselineCoords, 
                        alignment=FONT_ALIGN_CENTER, fontSize=26,
                        color=pygame.color.Color(64, 64, 64, 255)),
                "pauseRestart": TextElement(PAUSE_RESTART, 
                        self.pauseRestartBaselineCoords, 
                        alignment=FONT_ALIGN_CENTER, fontSize=26,
                        color=pygame.color.Color(48, 48, 48, 255)),
                "pauseExit": TextElement(PAUSE_QUIT, 
                        self.pauseExitBaselineCoords, 
                        alignment=FONT_ALIGN_CENTER, fontSize=26,
                        color=pygame.color.Color(68, 40, 40, 255)),
                }

        self.UIButtonsHoverCoords = {
                BUTTON_INGAME_HOVER_NONE: None,
                BUTTON_INGAME_HOVER_PAUSE: self.pauseButtonCoords,
                BUTTON_INGAME_HOVER_EXIT: self.exitButtonCoords
                }

        self.pauseButtonsHoverCoords = {
                BUTTON_PAUSE_HOVER_NONE: None,
                BUTTON_PAUSE_HOVER_CONTINUE: self.pauseContinueButtonCoords,
                BUTTON_PAUSE_HOVER_RESTART: self.pauseRestartButtonCoords,
                BUTTON_PAUSE_HOVER_EXIT: self.pauseExitButtonCoords
                }

        self.selMoveAnimations = []
        for i in range(8):
            self.selMoveAnimations.append([])
            for j in range(8):
                self.selMoveAnimations[-1].append(None)
        
        self.piecesWithLegalMovesAnimations = []
        for i in range(8):
            self.piecesWithLegalMovesAnimations.append([])
            for j in range(8):
                self.piecesWithLegalMovesAnimations[-1].append(None)

        self.movingPiece = None
        self.maskedPiece = None

    def setupWindow(self):
        pygame.init()
        pygame.display.set_caption(self.caption)




    def vanishPiece(self, event):
        self.board.removePiece(event.coords)

    def registerMove(self, newBoard, movement, eatenPieces):
        pieceColor = self.board.location(movement[0]).occupant.color
        self.maskedPiece = movement[0]
        path = [PathNode(self.mapToScrCoords(movement[0]), 1)]
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
                    self.appendNode(path, coord, False, True, 1)
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
                    self.appendNode(path, nextCoord, True, True, arcLength)
                    arcing = False

                event = pygame.event.Event(pygame.USEREVENT, 
                        eventType=EVENT_PIECE_VANISH, coords=coord)
                self.appendNode(path, coord, True, False, 1, event)

        # End an unfinished arc
        if arcing and arcLength > 0:
            self.appendNode(path, nextCoord, True, True, arcLength)

        path[-1].eventOnComplete = pygame.event.Event(pygame.USEREVENT,
                    eventType=EVENT_PATH_END)

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

    def updateAndDraw(self, hoverPosition, selectedPiece, hoverButton, 
            gamePaused, turnNumber, isPlayerTurn, gameEnded, playerScore, 
            opponentScore):
        self.timeDelta = self.clock.tick(self.fps) / 1000.
        self.background.blitAt(self.screen, (0, 0))
        self.drawBoardPieces()
        self.drawSelectedPiece(selectedPiece)
        if not gamePaused and gameEnded is None:
            self.drawHoverPiece(hoverPosition)
        self.updateAndDrawPossibleMoves(gamePaused)
        self.updateAndDrawPiecesWithLegalMovesAnim(gamePaused)
        self.updateAndDrawMovingPiece(gamePaused, self.timeDelta)
        if not gamePaused: 
            self.drawHoverButton(hoverButton)
        self.updateAndDrawSidebarText(isPlayerTurn, turnNumber, playerScore, 
                opponentScore)
        if gameEnded:
            self.updateAndDrawEndOverlay(self.timeDelta, hoverButton, 
                    gameEnded)
        if gamePaused: 
            self.drawPauseMenu(hoverButton)

        pygame.display.update()

        return self.timeDelta

        

    def drawBoardPieces(self):
        for col in range(8):
            for row in range(8):
                if self.board.matrix[col][row].occupant is not None:
                    if self.maskedPiece == (col, row): continue
                    if self.board.matrix[col][row].occupant.color is RED:
                        self.redPiece.blitAt(self.screen, 
                                self.mapToScrCoords((col, row)))

                        if self.board.matrix[col][row].occupant.king:
                            self.kingRedPiece.blitAt(self.screen,
                                    self.mapToScrCoords((col, row)))

                    elif self.board.matrix[col][row].occupant.color is WHITE:
                        self.whitePiece.blitAt(self.screen, 
                                self.mapToScrCoords((col, row)))

                        if self.board.matrix[col][row].occupant.king:
                            self.kingwhitePiece.blitAt(self.screen,
                                    self.mapToScrCoords((col, row)))

                    else: raise RuntimeError("Graphics.py::Graphics:drawBoardPieces: Invalid piece color `{}'".format(self.board.matrix[col][row].occupant.color))

    def setPossibleMoves(self, selPossibleMoves):
        for path in selPossibleMoves:
            for c in range(len(path)):
                if (path[c] is not None 
                        and lookup(self.selMoveAnimations, path[c]) is None 
                        and not self.board.location(path[c]).occupant):
                    self.selMoveAnimations[path[c][0]][path[c][1]] = ( 
                            AnimatedGraphic(self.selMoveMarkerPath, 1, 
                            delayStart=(c)))
        #print(self.selMoveAnimations)
    
    def clearPossibleMoves(self):
        for col in range(8):
            for row in range(8):
                self.selMoveAnimations[col][row] = None
    
    def updateAndDrawPossibleMoves(self, gamePaused):
        for x in range(8):
            for y in range(8):
                if not (self.selMoveAnimations[x][y] is None):
                    if not gamePaused: 
                        self.selMoveAnimations[x][y].update()
                    self.selMoveAnimations[x][y].blitAt(self.screen, 
                            self.mapToScrCoords((x, y)))

    def showPiecesWithLegalMoves(self, pieces):
        for p in pieces:
            self.piecesWithLegalMovesAnimations[p[0]][p[1]] = AnimatedGraphic(
                    self.pieceWithLegalMovesMarkerPath, 1)

    def updateAndDrawPiecesWithLegalMovesAnim(self, gamePaused):
        for x in range(8):
            for y in range(8):
                p = self.piecesWithLegalMovesAnimations[x][y]
                if p is not None:
                    if p.stopped:
                        self.piecesWithLegalMovesAnimations[x][y] = None
                        continue
                    if not gamePaused: 
                        self.piecesWithLegalMovesAnimations[x][y].update()
                    self.piecesWithLegalMovesAnimations[x][y].blitAt(
                            self.screen, self.mapToScrCoords((x, y)))

    def updateAndDrawMovingPiece(self, gamePaused, timeDelta):
        if isinstance(self.movingPiece, tuple):
            if not gamePaused:
                self.movingPiece[1].update(timeDelta)
            #print(self.movingPiece[1].currentPos)
            self.movingPiece[0].blitAt(self.screen,
                    self.movingPiece[1].currentPos)

    def drawHoverPiece(self, hoverPiece):
        if (isinstance(hoverPiece, tuple)):
            if (self.board.location(hoverPiece).occupant 
                    and not hoverPiece == self.maskedPiece):
                if self.board.location(hoverPiece).occupant.color is RED:
                    self.redPieceHover.blitAt(self.screen, 
                         self.mapToScrCoords(hoverPiece))

                elif self.board.location(hoverPiece).occupant.color is WHITE:
                    self.whitePieceHover.blitAt(self.screen, 
                            self.mapToScrCoords(hoverPiece))

                else: raise RuntimeError("Graphics.py::Graphics:drawHoverPiece: Invalid piece color `{}'".format(self.board.location(hoverPiece).occupant.color))
            elif lookup(self.selMoveAnimations, hoverPiece) is not None:
                lookup(self.selMoveAnimations, hoverPiece).blitAt(self.screen,
                        self.mapToScrCoords(hoverPiece))

    def drawSelectedPiece(self, selectedPiece):
        if (isinstance(selectedPiece, tuple)
                and self.board.location(selectedPiece).occupant
                and not selectedPiece == self.maskedPiece):
            if self.board.location(selectedPiece).occupant.color is RED:
                self.redPieceSelected.blitAt(self.screen, 
                        self.mapToScrCoords(selectedPiece))

            elif self.board.location(selectedPiece).occupant.color is WHITE:
                self.whitePieceSelected.blitAt(self.screen, 
                        self.mapToScrCoords(selectedPiece))

            else: raise RuntimeError("Graphics.py::Graphics:drawSelectedPiece: Invalid piece color `{}'".format(self.board.location(selectedPiece).occupant.color))
            

    def drawHoverButton(self, hoverButton):
        if hoverButton in self.UIButtonsHoverCoords:
            self.ingameButtonHover.blitAt(self.screen, 
                    self.UIButtonsHoverCoords[hoverButton])
        elif hoverButton in self.endOverlayButtonsRelCoords: pass
        else: raise RuntimeError("Graphics.py::Graphics:drawHoverButton: Invalid UI button `{}'".format(hoverButton))

    def updateAndDrawSidebarText(self, isPlayerTurn, turnNumber, playerScore, opponentScore):
        if isPlayerTurn:
            self.textObjects["turnText"].update(TURNSTRING.format(turnNumber))
        else:
            self.textObjects["turnText"].update(WAITSTRING)
        #self.textObjects["upperScore"].update(str(12 - self.board.whiteCounterAux))
        #self.textObjects["lowerScore"].update(str(12 - self.board.redCounterAux))
        self.textObjects["upperScore"].update(str(playerScore))
        self.textObjects["lowerScore"].update(str(opponentScore))
        for (key, o) in self.textObjects.items():
            o.blitAt(self.screen)

    def drawPauseMenu(self, hoverButton):
        self.pauseOverlay.blitAt(self.screen, (0, 0))
        for (key, o) in self.pauseTextObjects.items():
            o.blitAt(self.screen)
        
        if hoverButton in self.pauseButtonsHoverCoords:
            self.pauseButtonHover.blitAt(self.screen, 
                    self.pauseButtonsHoverCoords[hoverButton])
        else: raise RuntimeError(
                "Graphics.py::Graphics:drawPauseMenu: Invalid pause button `{}'".format(hoverButton))

    def updateAndDrawEndOverlay(self, timeDelta, hoverButton, gameEnded):
        self.endOverlayMotion.update(timeDelta)
        self.endGameTextObjects["winLoseFanfare"].update(gameEnded)
        endOverlayCorner = tplsum(self.endOverlayMotion.currentPos, 
                tplscale(self.endOverlayDimensions, -0.5))
        self.endOverlay.blitAt(self.screen, endOverlayCorner)
        if hoverButton in self.endOverlayButtonsRelCoords:
            self.endOverlayButtonHover.blitAt(self.screen, tplsum(
                    self.endOverlayButtonsRelCoords[hoverButton],
                    endOverlayCorner))
        for key, text in self.endGameTextObjects.items():
            text.blitAt(self.screen, tplsum(endOverlayCorner, text.coords))
    
    def mapToScrCoords(self, coords):
        """Maps board coordinates to screen coordinates."""
        return (coords[0] * self.boardSpacing + self.boardUpperLeftCoords[0], 
                coords[1] * self.boardSpacing + self.boardUpperLeftCoords[1])


    def appendNode(self, path, coord, accelerated, decelerated, moveLength, 
            event=None):
        speed = self.pieceBaseMoveSpeed * (moveLength ** 0.5)
        path.append(PathNode(self.mapToScrCoords(coord), speed, 
                accelerate=accelerated, decelerate=decelerated, 
                eventOnComplete=event))


def tplsum(t1, t2):
    """Returns the sum of two tuples."""
    return tuple(map(lambda x, y: x + y, t1, t2)) 

def tplscale(t, mult):
    """Returns the multiplication of a tuple by a number."""
    return tuple(map(lambda x: x * mult, t))

def lookup(matrix, index):
    """Looks up an index, defined by a tuple, in a multidimensional array."""
    result = matrix
    for i in index:
        result = result[i]
    return result


class Graphic:
    """Implements a graphic object that caches an image surface."""
    surface = None

    def __init__(self, path):
        self.surface = pygame.image.load(path).convert_alpha()

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
    stopped = None

    def __init__(self, path, frameDelay, loop=False, delayStart=0):
        paths = sorted(glob.glob(path))
        #print(paths)
        self.surfaces = list(map(pygame.image.load, paths))
        self.frameDelay = frameDelay
        self.frameDelayCounter = frameDelay + delayStart
        self.frame = 0
        self.looping = loop
        self.stopped = False
        Graphic.__init__(self, paths[0])

    def update(self):
        """Updates the animation. Must be called every frame."""
        if self.looping or not self.frame >= len(self.surfaces):
            self.frameDelayCounter -= 1
            if not self.frameDelayCounter > 0:
                self.frameDelayCounter = self.frameDelay
                self.frame += 1
                if self.looping and self.frame >= len(self.surfaces):
                    self.frame = 0
                if self.frame < len(self.surfaces):
                    self.surface = self.surfaces[self.frame]
        else:
            self.stopped = True


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
                return (self.coord2[0] * (2.0 * (self.nodeCompletion ** 2)) + 
                        self.coord1[0] * (1.0 - (2.0 * (self.nodeCompletion ** 2))),
                        self.coord2[1] * (2.0 * (self.nodeCompletion ** 2)) + 
                        self.coord1[1] * (1.0 - (2.0 * (self.nodeCompletion ** 2))))

            # 2nd half:
            else:
                return (self.coord2[0] * (1.0 - (2.0 * ((1.0 - self.nodeCompletion) ** 2)))
                      + self.coord1[0] * (2.0 * ((1.0 - self.nodeCompletion) ** 2)), 
                        self.coord2[1] * (1.0 - (2.0 * ((1.0 - self.nodeCompletion) ** 2)))
                      + self.coord1[1] * (2.0 * ((1.0 - self.nodeCompletion) ** 2)))


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
            return (coords[0], coords[1] - self.fontFace.get_ascent())
        elif(self.alignment == FONT_ALIGN_RIGHT):
            return (coords[0] - self.surface.get_width(), coords[1] - self.fontFace.get_ascent())
        else:
            return (coords[0] - (self.surface.get_width() / 2), coords[1] - self.fontFace.get_ascent())

    def update(self, value=None, newCoords=None):
        if isinstance(newCoords, tuple): self.coords = newCoords

class DynamicTextElement(TextElement):
    def __init__(self, initialValue, coords, fontFace="../assets/fonts/Cantarell-Regular.otf", fontSize=36, alignment=FONT_ALIGN_LEFT, color=pygame.Color(255, 255, 255, 255)):
        TextElement.__init__(self, initialValue, coords, fontFace, fontSize, alignment, color)

    def update(self, newValue=None, newCoords=None, newColor=None):
        if ((newValue is not None and newValue != self.text) 
                or newColor is not None):
            if newValue is not None: 
                self.text = newValue
            if newColor is not None: 
                self.color = newColor
            self.render()
        if isinstance(newCoords, tuple): self.coords = newCoords

def euclideanDist(coord1, coord2):
    """Returns the euclidean distance of two coordinates - (x, y) tuples"""
    return math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)

def main():
    random.seed()
    testBoard = Board()
    graphicsBackend = GraphicsBackend()
    graphics = Graphics(graphicsBackend, testBoard, "")
    #graphics.setPossibleMoves([[(0, 3), (1, 4), (2, 3), (3, 4), (4, 3), (5, 4), (6, 3), (7, 4)]])
    moveList = [[(0, 5), (1, 4)], [(3, 2), (2, 3)]]
    hoverPos = (0, 5)
    path = False
    paused = False
    button = 0
    while True:
        if (random.random() < 0.1):
            hoverPos = (int(random.random() * 8), int(random.random() * 8))
        if (random.random() < 0.1):
            y = int(random.random() * 3) + 5
            graphics.showPiecesWithLegalMoves([(int(random.random() * 4) * 2 + ((y + 1) & 1), y)])
        timeDelta = graphics.updateAndDraw(hoverPos, (2, 5), 
                button, paused, 1, True, ENDGAME_LOSE)
        #hoverPosition, selectedPiece, hoverButton,
        #    gamePaused, turnNumber, isPlayerTurn, gameEnded
        if (not path and len(moveList) > 0 and random.random() < 0.04):
            p = moveList.pop(0)
            #print(p)
            testBoard.movePiece(p[0], p[1])
            graphics.registerMove(testBoard, p, [])
            path = True
        if (not paused and random.random() < 0.01):
            paused = True
            button = int(random.random() * 3) + 3
        if (paused and random.random() < 0.04):
            paused = False
            button = int(random.random() * 3)
        if (random.random() < 0.07):
            button = int(random.random() * 2) + 6
            if paused: button -= 3
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT:
                if event.eventType == EVENT_PIECE_VANISH:
                    graphics.vanishPiece(event)
                elif event.eventType == EVENT_PATH_END:
                    graphics.endPath()
                    path = False
                    

if __name__ == "__main__": main()

