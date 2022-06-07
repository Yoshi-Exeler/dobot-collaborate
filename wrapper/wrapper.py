'''
MIT License

Copyright (c) 2022 Yoshi Noah Exeler

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from dobot import DobotDllType as dType
from dobot2 import DobotDllType2 as dType2


CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}


class Position:
    X: float
    Y: float
    Z: float
    R: float

    def __init__(self, x: float, y: float, z: float, r: float) -> None:
        self.X = x
        self.Y = y
        self.Z = z
        self.R = r
        pass


# DobotWrapper is a simple wrapper class for the dobot c bindings, that aims to improve usability by providing a simpler interface
class DobotWrapper:
    __comport: str
    __state: any
    __conn: any
    __xinverted: bool
    __yinverted: bool

    # Creates a wrapper for the dobot reachable on the specified comport.
    # xinverted and yinverted specify wether the directional moves will be inverted on that axis
    # dobot2 specifies wether to use the duplicate dobot interface, use this if you want to interact with a second dobot
    def __init__(self, comport: str,xinverted: bool, yinverted: bool, dobot2: bool) -> None:
        self.__xinverted = xinverted
        self.__yinverted = yinverted
        if dobot2:
            self.__conn = dType2.load()
        else:
            self.__conn = dType.load()
        self.__comport = comport
        pass

    # connect will open a connection with the robot on the specified comport and home it
    def connect(self) -> bool:
        self.__state = dType.ConnectDobot(
            self.__conn, self.__comport, 115200)[0]
        if (self.__state == dType.DobotConnect.DobotConnect_NoError):
            print("[Wrapper] connection to dobot on port ",
                  self.__comport, " successfull, setting up...")
            dType.SetQueuedCmdClear(self.__conn)
            dType.SetQueuedCmdStartExec(self.__conn)
            dType.SetPTPCmdEx(self.__conn, 0, 193,  0,  23, -
                              0.264, 1)  # why do we do this?
            dType.dSleep(100)
            print("[Wrapper] dobot on port ", self.__comport, " now homing")
            dType.SetHOMEParams(self.__conn, 250, 0, 50, 0, isQueued=1)
            dType.SetHOMECmd(self.__conn, 0, isQueued=1)
            print("[Wrapper] command queue length: ", len(
                dType.GetQueuedCmdMotionFinish(self.__conn)), " awaiting homing completion")
            self.awaitMotionCompleted()  # block until homing has completed
            return True
        else:
            return False

        pass

    # move will add a move command to the desired target state to the command queue
    def move(self, target: Position) -> None:
        dType.SetQueuedCmdClear(self.__conn)
        dType.SetQueuedCmdStartExec(self.__conn)
        # add our command to the command queue
        dType.SetPTPCmdEx(self.__conn, 2, target.X,
                          target.Y,  target.Z, target.R, 1)
        pass

    # moveLeft will move the robot left, respecting the configured inverts.
    def moveLeft(self, amount: float) -> None:
        # get the current position
        position = self.getPosition()
        # apply the delta, respecting inverts
        if self.__yinverted:
            position.Y = position.Y + amount
        else:
            position.Y = position.Y - amount
        # run the move
        self.move(position)


    # moveRight will move the robot right, respecting the configured inverts.
    def moveRight(self, amount: float) -> None:
        # get the current position
        position = self.getPosition()
        # apply the delta, respecting inverts
        if self.__yinverted:
            position.Y = position.Y - amount
        else:
            position.Y = position.Y + amount
        # run the move
        self.move(position)


    # moveForward will move the robot forwards, respecting the configured inverts.
    def moveForward(self, amount: float) -> None:
        # get the current position
        position = self.getPosition()
        # apply the delta, respecting inverts
        if self.__xinverted:
            position.X = position.X - amount
        else:
            position.X = position.X + amount
        # run the move
        self.move(position)


    # moveBackward will move the robot backwards, respecting the configured inverts.
    def moveBackward(self, amount: float) -> None:
        # get the current position
        position = self.getPosition()
        # apply the delta, respecting inverts
        if self.__xinverted:
            position.X = position.X + amount
        else:
            position.X = position.X - amount
        # run the move
        self.move(position)


    # moveUp will move the robot up.
    def moveUp(self, amount: float) -> None:
        # get the current position
        position = self.getPosition()
        # apply the delta
        position.Z = position.Z + amount
        # run the move
        self.move(position)



    # moveDown will move the robot down.
    def moveDown(self, amount: float) -> None:
        # get the current position
        position = self.getPosition()
        # apply the delta
        position.Z = position.Z - amount
        # run the move
        self.move(position)

    # setSuckState sets the state of the sucktion cup on the dobot magician
    def setSuckState(self, state: bool) -> None:
        conv_state = 0
        if (state):
            conv_state = 1
        dType.SetEndEffectorSuctionCupEx(self.__conn, 1, conv_state)
        pass

    # awaitMotionComplated blocks until all queued commands have been executed
    def awaitMotionCompleted(self) -> None:
        # why does dType.GetQueuedCmdCurrentIndex() return a list of ints???
        # check that the queue entries are actually removed once the motion is finisheds
        while (not dType.GetQueuedCmdMotionFinish(self.__conn)[0]):
            dType.dSleep(25)
        pass

    # getPosition returns the current position of the dobot
    def getPosition(self) -> Position:
        pos = dType.GetPose(self.__conn)
        return Position(pos[0], pos[1], pos[2], pos[3])

    # getConnectionState returns the current state of the connection with the robot
    def getConnectionState(self) -> str:
        return CON_STR[self.__state]

    # disconnect will close the connection with the robot
    def disconnect(self) -> None:
        dType.DisconnectDobot(self.__conn)
        pass
