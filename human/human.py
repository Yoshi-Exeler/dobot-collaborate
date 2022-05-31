from typing import Any
from game.game import TicTacToe
import asyncio

# HumanPlayer models the human playing tic-tac-toe
class HumanPlayer:
    __game: TicTacToe

    # a human player may be initialized with a game reference
    def __init__(self, game: TicTacToe):
        self.__game = game
        print("[HumanPlayer] initialized")
        pass

    # the run coroutine will block until it is the turn of the human player.
    # when its the humanplayers turn, the humanplayer will query the user for
    # input until a valid move is entered and then execute the specified move and pass
    # the turn to the AI players coroutine.  
    async def run(self):
        print("[HumanPlayer] enter main loop")
        while True:
            # first, block until its our turn
            await self.__game.awaitTurn(True)

            # make sure to exit if the game is no longer in progress
            if self.__game.getGameState() != 0:
                print("[HumanPlayer] game state is not in progress, exiting")
                self.__game.passTurn()
                return

            print("[HumanPlayer] begin turn")
            # next, generate a turn and execute it
            self.__game.placeSymbol(self.__queryUserForTurn())

            # pass the turn to the ai players coroutine            
            print("[HumanPlayer] end turn")
            self.__game.passTurn()


    # queryUserForTurn will query the user for a valid input until the user enters a valid input
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

                field -= 1

                print(self.__game.getBoard()[field])
                if self.__game.getBoard()[field] != "":
                    raise ValueError

                return field
            except ValueError:
                print("\nOnly empty fields (from 1 to 9) allowed.\n")

