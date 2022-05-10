from telnetlib import COM_PORT_OPTION
from time import sleep
from game.game import Renderer, TicTacToe
from ai.ai import AIPlayer
from human.human import HumanPlayer
import asyncio

from wrapper.wrapper import DobotWrapper

print("[Init] connecting to dobots")

robotOne = DobotWrapper("COM3",False,False)

robotTwo = DobotWrapper("COM3",True,True)


if not (robotOne.connect()):
    print("[Init] connection with dobot one failed")
    exit(1337)


if not (robotTwo.connect()):
    print("[Init] connection with dobot two failed")
    exit(1337)

print("[Init] both dobots are homed and ready")

print("[Init] creating game instance")

# create our renderer instance
renderer = Renderer(robotOne,robotTwo)

# Create a game instance to be used
gameInstance = TicTacToe(renderer)

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