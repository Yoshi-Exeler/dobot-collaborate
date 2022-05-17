from time import sleep
from wrapper.wrapper import DobotWrapper, Position
import asyncio

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

# finally, we will run two movements at the same time

# grab the current position
pos = robot_one.getPosition()
pos.X += 5
robot_one.move(pos)
pos_two = robot_two.getPosition()
pos_two.X += 5
robot_two.move(pos_two)
sleep(10)