from dobot import DobotDllType as dType

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

# DobotWrapper is a simple wrapper class for the dobot c bindings, that aims to improve usability by provising a simpler interface


class DobotWrapper:
    __comport: str
    __state: any
    __conn: any
    __cmdIndex: int

    def __init__(self, comport: str) -> None:
        self.__conn = dType.load()
        self.__comport = comport
        pass

    # connect will open a connection with the robot on the specified comport
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
                dType.GetQueuedCmdMotionFinish(self.__conn), " awaiting homing completion"))
            self.awaitMotionCompleted()  # block until homing has completed
            return True
        else:
            return False

        pass

    # move will add a move command to the desired target state to the command queue and then block until the move has been executed by the robot.
    # You can either run this with await 'await robot.move(mytarget)' to run the move synchronously or without await to run it asynchronously.
    async def move(self, target: Position) -> None:
        # add our command to the command queue
        dType.SetPTPCmdEx(self.__conn, 2, target.X,
                          target.Y,  target.Z, target.R, 1)
        self.awaitMotionCompleted()  # block until the move has completed
        pass

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
        ret = Position(pos[0], pos[1], pos[2], pos[3])
        pass

    # getConnectionState returns the current state of the connection with the robot
    def getConnectionState(self) -> str:
        return CON_STR[self.__state]

    # disconnect will close the connection with the robot
    def disconnect(self) -> None:
        dType.DisconnectDobot(self.__conn)
        pass
