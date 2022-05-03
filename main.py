from time import sleep
from game.game import TicTacToe
from ai.ai import AIPlayer
from human.human import HumanPlayer
import asyncio

print("[Init] creating game instance")

# Create a game instance to be used
gameInstance = TicTacToe()

print("[Init] launching player coroutines")

# Create a HumanPlayer instance and run its entrypoint in a coroutine
playerOne = HumanPlayer(gameInstance)
asyncio.ensure_future(playerOne.run())

# Create an AIPlayer instance and run its entrypoint in a coroutine
playerTwo = AIPlayer(gameInstance)
asyncio.ensure_future(playerTwo.run())

loop = asyncio.get_event_loop()
loop.run_forever()

sleep(60)