from time import sleep
from typing import List
import asyncio

PLAYER_ONE_SYMBOL = 'O'
PLAYER_TWO_SYMBOL = "X"
DEBUG = True


class TicTacToe:
    __board: List[str]  # board representation
    __playerOneTurn: bool

    def __init__(self):
        self.__playerOneTurn = True
        pass

    # blocks until its your turn
    async def awaitTurn(self, playerOne: bool):
        while (not self.__playerOneTurn == playerOne):
            await asyncio.sleep(0.25)
        pass

    def placeSymbol(self, position: int) -> bool:
        # places the symbol of the active player at the specified position,
        # ensuring that the position is empty. If the position is not empty, returns false
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
