from game.game import TicTacToe
from ai.ai import AIPlayer
from human.human import HumanPlayer
import asyncio

# Create a game instance to be used
gameInstance = TicTacToe()

# Create a HumanPlayer instance and run its entrypoint in a coroutine
playerOne = HumanPlayer(gameInstance)
asyncio.run(playerOne.run())

# Create an AIPlayer instance and run its entrypoint in a coroutine
playerTwo = AIPlayer(gameInstance)
asyncio.run(playerTwo.run())