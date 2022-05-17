from time import sleep
from wrapper.wrapper import DobotWrapper, Position
import asyncio

DOBOT_ONE_PORT = "COM3"
DOBOT_TWO_PORT = "COM5"

robot_one = DobotWrapper(DOBOT_ONE_PORT,False,False)
robot_two = DobotWrapper(DOBOT_TWO_PORT,True,True)

if not (robot_one.connect()):
    print("connection with dobot one failed")
    exit(1337)


if not (robot_two.connect()):
    print("connection with dobot two failed")
    exit(1337)

# finally, we will run two movements at the same time
robot_one.move(Position(30, 30, 30, 0))
robot_two.move(Position(-30, -30, -30, 0))

sleep(10)