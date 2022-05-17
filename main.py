from telnetlib import COM_PORT_OPTION
from time import sleep
from game.game import Renderer, TicTacToe
from ai.ai import AIPlayer
from human.human import HumanPlayer
import asyncio

from wrapper.wrapper import DobotWrapper, Position

print("[Init] connecting to dobots")

DOBOT_ONE_PORT = "COM6"
DOBOT_TWO_PORT = "COM5"

robot_one = DobotWrapper(DOBOT_ONE_PORT,False,False,False)
robot_two = DobotWrapper(DOBOT_TWO_PORT,True,True,True)

rest_pos_one = Position(85,-160,42,-65)

rest_pos_two = Position(130,146,36,48)

if not (robot_one.connect()):
    print("connection with dobot one failed")
    exit(1337)

robot_one.move(rest_pos_one)


if not (robot_two.connect()):
    print("connection with dobot two failed")
    exit(1337)

robot_two.move(rest_pos_two)

print("[Init] both dobots are homed and ready")

print("[Init] creating game instance")

# create our renderer instance
renderer = Renderer(robot_one, robot_two)

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
