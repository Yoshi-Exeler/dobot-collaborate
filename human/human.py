from typing import Any
from game.game import TicTacToe
import asyncio


class HumanPlayer:
    __game: TicTacToe

    def __init__(self, game: TicTacToe):
        self.__game = game
        pass

    async def run(self):
        while True:
            # first, block until its our turn
            self.__game.awaitTurn(True)

            # next, generate a turn and execute it
            self.__game.placeSymbol(self.__queryUserForTurn())

            # finally, check the game state and process it
            state = self.__game.getGameState()
            # ... react to the state here
        pass

    def __queryUserForTurn(self) -> int:
        # returns the index of the cell that the AI wants to place a symbol in
        pass
