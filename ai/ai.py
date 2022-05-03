from game.game import TicTacToe
import game
import asyncio


class AIPlayer:
    __game: TicTacToe

    def __init__(self, game: TicTacToe):
        self.__game = game
        print("[AIPlayer] initialized")
        pass

    async def run(self):
        print("[AIPlayer] enter main loop")
        while True:
            # first, block until its our turn
            await self.__game.awaitTurn(False)

            print("[AIPlayer] begin turn")
            # next, generate a turn and execute it
            self.__game.placeSymbol(self.__computeTurn())

            # finally, check the game state and process it
            state = self.__game.getGameState()
            # ... react to the state here
            print("[AIPlayer] end turn")
            self.__game.passTurn()
        pass

    def __computeTurn() -> int:
        # returns the index of the cell that the AI wants to place a symbol in
        pass
