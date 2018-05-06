import pygame
from Board import *
import glob
import math

class Graphics:
    def __init__(self):
        self.caption = "Checkers"

        self.fps = 60
        self.clock = pygame.time.Clock()

        self.windowSize = 720
        self.screen = pygame.display.set_mode((self.windowSize, self.windowSize))
        self.background = pygame.image.load("../graphics-proto/checker.png")

        self.squareSize = int(round(self.windowSize / 8))
        self.pieceSize = int(round(self.squareSize / 2))

        self.message = False

    def setupWindow(self):
        pygame.init()
        pygame.display.set_caption(self.caption)

    def updateDisplay(self, board, legalMovements, selectedPiece):
        """
        This updates the current display.
        """
        self.screen.blit(self.background, (0, 0))

        # self.highlight_squares(legal_moves, selected_piece)
        self.drawBoardPieces(board)
        self.highlightLegalMoves(legalMovements, selectedPiece, board)
        self.drawBoardKings(board)

        if self.message:
            self.screen.blit(self.text_surface_obj, self.text_rect_obj)

        pygame.display.update()
        self.clock.tick(self.fps)

    """-----------------------------------------------------------------------------+
    |  Victor: I don't think these routines are supposed to be here...              |
    |  they're all related to the GameBoard class and should be called from there,  |
    |  with the Graphics class handling low level graphical functions.              |
    |  We'll discuss this in the next meetup so we can define where these go.       |
    +-----------------------------------------------------------------------------"""

    def drawBoardSquares(self, board):
        """
            Takes a board object and draws all of its squares to the display
            """
        for x in range(8):
            for y in range(8):
                pygame.draw.rect(self.screen, board[x][y].color,
                                 (x * self.squareSize, y * self.squareSize, self.squareSize, self.squareSize), )

    def drawBoardPieces(self, board):
        for x in range(8):
            for y in range(8):
                if board.matrix[x][y].occupant is not None and board.matrix[x][y].color is BLACK and board.matrix[x][y].occupant.color is RED:
                    redPiece = pygame.image.load("../graphics-proto/piece_red.png")
                    self.screen.blit(redPiece, (x * 90, y * 90))

                if board.matrix[x][y].occupant is not None and board.matrix[x][y].color is BLACK and board.matrix[x][y].occupant.color is WHITE:
                    whitePiece = pygame.image.load("../graphics-proto/piece_white.png")
                    self.screen.blit(whitePiece, (x * 90, y * 90))

    def drawBoardKings(self, board):
        for x in range(8):
            for y in range(8):
                if board.matrix[x][y].occupant is not None and board.matrix[x][y].occupant.king == True:
                    kingPiece = pygame.image.load("../graphics-proto/crown.png")
                    self.screen.blit(kingPiece, (x * 90, y * 90))

    def highlightLegalMoves(self, legalMoves, selectedPiece, board):
        if selectedPiece is not None and legalMoves is not None:
            """--------------------------------------------------------------------+
            | VitinhoCarneiro: Don't load stuff every time you're going to use it, |
            | it's unnecessary and slow. Cache it somewhere.                       |
            +--------------------------------------------------------------------"""
            goldPiece = pygame.image.load("../graphics-proto/gold.png")

            for movePath in legalMoves:
                # self.screen.blit(goldPiece, (movePath.x * 90, movePath.y * 90))
                for coordinate in movePath:
                    if coordinate is not None and not board.location(coordinate).occupant:
                        self.screen.blit(goldPiece, (coordinate.x * 90, coordinate.y * 90))

    def pixelCoords(self, boardCoords):
        """
            Takes in a tuple of board coordinates (x,y)
            and returns the pixel coordinates of the center of the square at that location.
        """
        return (
            boardCoords[0] * self.squareSize + self.pieceSize, boardCoords[1] * self.squareSize + self.pieceSize)

    def boardCoords(self, pixelCoordinate):
        """
           Does the reverse of pixel_coords(). Takes in a tuple of of pixel coordinates and returns what square they are in.
        """
        return Coordinate(int(pixelCoordinate[0] / self.squareSize), int(pixelCoordinate[1] / self.squareSize))


    def pixelToSquarePosition(self, pixelCoordinate):
        """
            Does the reverse of pixel_coords(). Takes in a tuple of of pixel coordinates and returns what square they are in.
        """
        return Coordinate(pixelCoordinate.x / self.squareSize, pixelCoordinate.y / self.squareSize)

    def piecePositionToPixel(self, boardPiece):
        return True

    def draw_message(self, message):
        """
        Draws message to the screen.
        """
        self.message = True
        self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
        self.text_surface_obj = self.font_obj.render(message, True, HIGH, BLACK)
        self.text_rect_obj = self.text_surface_obj.get_rect()
        self.text_rect_obj.center = (self.windowSize / 2, self.windowSize / 2)

    def onBoard(self, coordinates):
        """
        Checks to see if the given square (x,y) lies on the board.
        If it does, then on_board() return True. Otherwise it returns false.
        """

    def isEndSquare(self, coordinate):
        """
        Is passed a coordinate tuple (x,y), and returns true or
        false depending on if that square on the board is an end square.
        """

        if coordinate.x == 0 or coordinate.y == 7:
            return True
        else:
            return False

    """--------------------------------------------------+
    | VitinhoCarneiro: Why the heck are these functions  |
    | below, unrelated to graphics, in here?             |
    +--------------------------------------------------"""

    def removePiece(self, coordinate, board):
        """
        Removes a piece from the board at position (x,y).
        """
        board.matrix[coordinate.x][coordinate.y].occupant = None

    def movePiece(self, startCoordinate, endCoordinate, board):
        """
        Move a piece from (start_x, start_y) to (end_x, end_y).
        """

        board.matrix[endCoordinate.x][endCoordinate.y].occupant = board.matrix[startCoordinate.x][
            startCoordinate.y].occupant
        self.removePiece(startCoordinate, board)

        board.king(endCoordinate)

    def isEndSquare(self, coords):

        if coords[1] == 0 or coords[1] == 7:
            return True
        else:
            return False

class Graphic:
    """Implements a graphic object that caches an image surface."""
    surface = None
    # This mutex is used for the Motion class, to assure that it's only being
    # moved by one Motion object.
    mutex = None

    def __init__(self, path):
        self.surface = pygame.image.load(path)
        self.mutex = False

    def blitat(self, surface, coordsOrX, y = None):
        """Blits this graphic's surface over another surface."""
        if y is not None:
            coordsOrX = (coordsOrX, y)

        surface.blit(self.surface, coordsOrX)

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
    
    def __init__(self, path, frameDelay, loop = False):
        paths = glob.glob(path)
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
                self.surface = self.surfaces(self.frame)

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

    def update(self, timeDelta = 1.0/60):
        """Updates the movement coordinates."""
        if self.hasCompleted: return

        self.nodeCompletion += self.currentSpeed * timeDelta

        if(self.nodeCompletion >= 1.0):
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
            node = self.path.pop[0]
            self.coord2 = node.coords
            self.currentSpeed = node.speed / euclideanDist(coord1, coord2)
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

    def __init__(self, coords, speed, eventOnComplete = None, accelerate = False, decelerate = False):
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
           return self.coord2 * (self.nodeCompletion ** 2) + self.coord1 * (1.0 - (self.nodeCompletion ** 2))

        # Case 2: deceleration only
        if self.decelerate and not self.accelerate:
            return self.coord2 * (1.0 - ((1.0 - self.nodeCompletion) ** 2)) + self.coord1 * ((1.0 - self.nodeCompletion) ** 2) 
        
        # Case 3: acceleration and deceleration
        if self.decelerate and self.accelerate:
            # This function is decomposed into two quadratic curves. 1st half:
            if(nodeCompletion < 0.5):
                return self.coord2 * (2.0 * self.nodeCompletion ** 2) / 2.0 + self.coord1 * (1.0 - ((2.0 * self.nodeCompletion) ** 2) / 2.0)
            # 2nd half:
            else:
                return self.coord2 * (1.0 - (2.0 * (1.0 - self.nodeCompletion) ** 2 / 2.0)) + self.coord1 * (2.0 * (1.0 - self.nodeCompletion) ** 2 / 2.0)

        # Case 4: linear motion (not accelerated or decelerated)
        return Motion.calcPosition(self)


def euclideanDist(coord1, coord2):
    """Returns the euclidean distance of two coordinates - (x, y) tuples"""
    return math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)


