from tkinter import SEL_FIRST
from game.game import TicTacToe
from typing import List
from wrapper.wrapper import DobotWrapper, Position

offsets = List[Position]
offsets[0] = Position(-50, 50, 0, 0)
offsets[1] = Position(0, 50, 0, 0)
offsets[2] = Position(50, 50, 0, 0)
offsets[3] = Position(-50, 0, 0, 0)
offsets[4] = Position(0, 0, 0, 0)
offsets[5] = Position(50, 0, 0, 0)
offsets[6] = Position(-50, -50, 0, 0)
offsets[7] = Position(0, -50, 0, 0)
offsets[8] = Position(50, -50, 0, 0)


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

    def render(self, game: TicTacToe):
        # first we print the state to stdout
        print(game.__board[0], game.__board[1], game.__board[2])
        print(game.__board[3], game.__board[4], game.__board[5])
        print(game.__board[6], game.__board[7], game.__board[8])
        # get the cell where the last move was made
        deltaCell = self.findDeltaCell(game)
        # get the symbol that was last placed
        symbolPlaced = game[deltaCell]
        # place this symbol on the paper using the current player's dobot
        self.__placeSymbol(deltaCell, symbolPlaced)
        # update the render state
        self.__renderState = game
        # flip the toggle so the other dodot will be used next
        self.__toggle = not self.__toggle

    def findDeltaCell(self, game: TicTacToe) -> int:
        for i in range(len(game.__board)):
            if not game.__board[i] == self.__renderState[i]:
                return i
        return -1

    async def placeSymbol(self, index: int, symbol: str):
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
        # draw the symbol
        # move back to the starting position
        await robot.move(pos)
