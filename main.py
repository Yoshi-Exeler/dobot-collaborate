from wrapper.wrapper import DobotWrapper, Position
import platform

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

# robot_one.move(Position(0,0,0,0)), moves the robot to the specifiec X,Y,Z coordinated and applies the specified Rotation

# robot_one.getPosition(), returns the current position of the dobot

# await robot_one.awaitMotionFinish() will block until the robot has finished its current movement