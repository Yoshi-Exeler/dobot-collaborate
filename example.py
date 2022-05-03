from wrapper.wrapper import DobotWrapper, Position
import asyncio

DOBOT_ONE_PORT = "COM3"
DOBOT_TWO_PORT = "COM5"

robot_one = DobotWrapper(DOBOT_ONE_PORT)
robot_two = DobotWrapper(DOBOT_TWO_PORT)

if not (robot_one.connect()):
    print("connection with dobot one failed")
    exit(1337)


if not (robot_two.connect()):
    print("connection with dobot two failed")
    exit(1337)

print("both dobots are homed and ready")

# robot_one.move(Position(0,0,0,0)), moves the robot to the specified X,Y,Z coordinated and applies the specified Rotation, the command is queued but the method does not block

# await robot_one.move(Position(0,0,0,0)), moves the robot to the specified Position and blocks until the motion completes

# robot_one.getPosition(), returns the current position of the dobot

# robot_one.awaitMotionFinish() will block until the robot has finished its current movement

# now lets do some practical examples
async def main():
    # first we will run two movements in sequence
    await robot_one.move(Position(0,0,0,0))
    await robot_two.move(Position(0,0,0,0))

    # now sleep for 3s
    asyncio.sleep(3000)

    # finally, we will run two movements at the same time
    robot_one.move(Position(30,30,30,0))
    robot_two.move(Position(-30,-30,-30,0))

    # now sleep for 3s
    asyncio.sleep(3000)

main()