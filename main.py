from wrapper.wrapper import DobotWrapper
import platform

print(platform.architecture())

robot = DobotWrapper("COM3")
ok = robot.connect()
print(ok)