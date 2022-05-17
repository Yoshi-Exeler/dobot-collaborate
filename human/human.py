from typing import Any
from game.game import TicTacToe
import asyncio


class HumanPlayer:
    __game: TicTacToe

    def __init__(self, game: TicTacToe):
        self.__game = game
        print("[HumanPlayer] initialized")
        pass

    async def run(self):
        print("[HumanPlayer] enter main loop")
        while True:
            # first, block until its our turn
            await self.__game.awaitTurn(True)

            if self.__game.getGameState() != 0:
                print("[HumanPlayer] game state is not in progress, exiting")
                self.__game.passTurn()
                return

            print("[HumanPlayer] begin turn")
            # next, generate a turn and execute it
            self.__game.placeSymbol(self.__queryUserForTurn())

            # finally, check the game state and process it
            state = self.__game.getGameState()
            # ... react to the state here
            print("[HumanPlayer] end turn")
            self.__game.passTurn()


    def __queryUserForTurn(self) -> int:
        # returns the index of the cell that the human wants to place their symbol in
        while True:
            try:
                field = int(input("Please enter your desired field as it appears on your numpad > "))

                if field < 1 or field > 9:
                    raise ValueError # Please python, I just want to *throw* an exception.

                # Vertically mirror numbers as they appear on numpad
                if field <= 3:
                    field += 6
                elif field >= 7:
                    field -= 6

                print("You selected field", field - 1)
                return field - 1
            except ValueError:
                print("\nOnly values from 1 to 9 allowed.\n")

