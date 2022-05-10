from time import sleep
from typing import List
import asyncio
from wrapper.wrapper import DobotWrapper, Position
from game.game import *
import math

PLAYER_ONE_SYMBOL = 'O'
PLAYER_TWO_SYMBOL = "X"
DEBUG = True

offsets = []
offsets.append(Position(-50, 50, 0, 0))
offsets.append(Position(0, 50, 0, 0))
offsets.append(Position(50, 50, 0, 0))
offsets.append(Position(-50, 0, 0, 0))
offsets.append(Position(0, 0, 0, 0))
offsets.append(Position(50, 0, 0, 0))
offsets.append(Position(-50, -50, 0, 0))
offsets.append(Position(0, -50, 0, 0))
offsets.append(Position(50, -50, 0, 0))
DEBUG = True


class Renderer:
    __renderState: List[str]
    __robotOne: DobotWrapper  # the first player's dobot
    __robotTwo: DobotWrapper  # the second player's dobot
    __toggle: bool  # switch dobots after every move made

    def __init__(self, robotOne: DobotWrapper, robotTwo: DobotWrapper):
        self.__robotOne = robotOne
        self.__robotTwo = robotTwo
        self.__toggle = False
        self.__renderState = List[str]
        pass

    def render(self, board: List[str]):
        # first we print the state to stdout
        print(board[0], board[1], board[2])
        print(board[3], board[4], board[5])
        print(board[6], board[7], board[8])
        if DEBUG:
            return
        # get the cell where the last move was made
        deltaCell = self.findDeltaCell(board)
        # get the symbol that was last placed
        symbolPlaced = board[deltaCell]
        # place this symbol on the paper using the current player's dobot
        self.__placeSymbol(deltaCell, symbolPlaced)
        # update the render state
        self.__renderState = board
        # flip the toggle so the other dodot will be used next
        self.__toggle = not self.__toggle

    def findDeltaCell(self, board: List[str]) -> int:
        for i in range(len(board)):
            if not board[i] == self.__renderState[i]:
                return i
        return -1

    async def placeSymbol(self, index: int, symbol: str):
        # TODO we should probably pass most of these as parameters
        # setting some measurements for the symbols
        down = 10
        corners = 16
        size = 4

        # get our dobot instance
        robot = self.__robotOne
        if self.__toggle:
            robot = self.__robotTwo
        # get the offset for the target field
        offset = offsets[index]
        # get our current position
        pos = robot.getPosition()
        # compute our target position
        target = Position(pos.X+offset.X, pos.Y+offset.Y,
                          pos.Z+offset.Z, pos.R+offset.R)
        # move to the target position
        await robot.move(target)
        # draw the symbols
        if symbol == "X":
            self.drawX(robot, target, down, size)
        elif symbol == "O":
            self.drawO(robot, target, down, corners, size)
        else:
            print("Cannot draw symbols other thatn X or O")
        # move back to the starting position
        await robot.move(pos)
    
    def drawX(robot, target, deltaZ, size):
        # defining the corner points for readability
        upperX = target.X + size/2
        lowerX = target.X - size/2
        upperY = target.Y + size/2
        lowerY = target.Y - size/2
        zUp = target.Z
        zDown = target.Z - deltaZ
        r = target.r
        
        #actual drawing begins
        robot.move(Position(upperX, upperY, zUp, r))
        robot.moveDown(deltaZ)
        robot.move(Position(lowerX, lowerY, zDown, r))
        robot.moveUp(deltaZ)
        robot.move(Position(lowerX, upperY, zUp, r))
        robot.moveDown(deltaZ)
        robot.move(Position(upperX, lowerY, zDown, r))
        robot.moveUp(deltaZ)
    
    def drawO(robot, target, deltaZ, corners, size):
        #draws a regular polygon with specified number of corners
        #more corners make the polygon closer to a circle, but take longer
        #circles would require a new, complicated movement function that cannot be achieved with PTP commands
        
        #getting in position
        targetReady= Position(target.X, target.Y+size/2, target.Z, target.R)
        zDown = target.Z-deltaZ
        robot.move(targetReady)

        for i in range(corners):
            #transforms the polar coordinates into cartesian to find next corner
            cornerX = target.X + size/2 * math.cos(i*2*math.pi/corners)
            cornerY = target.Y + size/2 * math.sin(i*2*math.pi/corners)

            #draws line to next corner
            point = Position(cornerX, cornerY, zDown, target.r)
            robot.move(point)
        
        robot.moveUp(deltaZ)






class TicTacToe:
    __board: List[str]  # board representation
    __playerOneTurn: bool
    __renderer: Renderer

    def __init__(self, renderer: Renderer):
        self.__renderer = renderer
        self.__playerOneTurn = True
        self.__board = ["","","","","","","","",""]
        pass

    # blocks until its your turn
    async def awaitTurn(self, playerOne: bool):
        while (not self.__playerOneTurn == playerOne):
            await asyncio.sleep(0.25)
        pass

    def placeSymbol(self, position: int) -> bool:
        # places the symbol of the active player at the specified position,
        # ensuring that the position is empty. If the position is not empty, returns false
        self.__renderer.render(self.__board)
        pass

    def passTurn(self):
        self.__playerOneTurn = not self.__playerOneTurn

    def getBoard(self) -> List[str]:
        return self.__board

    def getGameState(self) -> int:
        # returns the state of the game as an integer 'enum'
        # 0 = in_progress, 1 = player_one_won, 2 = player_two_one, 3 = tied
        pass

    def __debugRender(self):
        # sould render a text based representation of the board to the standard output.
        # This should be called after every placeSymbol call when DEBUG is set to true.
        pass

