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

    def __init__(self,x: float, y: float, z: float, r: float) -> None:
        self.X = x
        self.Y = y
        self.Z = z
        self.R = r
        pass


class DobotWrapper:
    __comport: str
    __conn: any
    __api: any

    def __init__(self, comport: str) -> None:
        self.__api = dType.load()
        self.__comport = comport
        pass

    def connect(self) -> bool:
        self.__conn = dType.ConnectDobot(self.__api, self.__comport, 115200)[0]
        if (self.__conn == dType.DobotConnect.DobotConnect_NoError):
            print("[Wrapper] connection to dobot on port ",self.__comport, " successfull, setting up...")
            dType.SetQueuedCmdClear(self.__api)
            dType.SetQueuedCmdStartExec(self.__api)
            dType.SetPTPCmdEx(self.__api, 0, 193,  0,  23, -0.264, 1)
            dType.dSleep(100)
            print("[Wrapper] dobot on port ",self.__comport," now homing")
            dType.SetHOMEParams(self.__api, 250, 0, 50, 0, isQueued=1)
            dType.SetHOMECmd(self.__api, 0, isQueued=1)
            return True
        else:
            return False

    pass

    def move(self, target: Position, queued = 1) -> None:
        dType.SetPTPCmdEx(self.__api, 2, target.X,  target.Y,  target.Z, target.R, queued)
        pass

    def setSuckState(self, state: bool) -> None:
        conv_state = 0
        if (state):
            conv_state = 1
        dType.SetEndEffectorSuctionCupEx(self.__api, 1, conv_state)
        

    async def awaitMotionFinish(self) -> None:
        while (not dType.GetQueuedCmdMotionFinish(self.__api)[0]):
            dType.dSleep(25)
        pass

    def getPosition(self) -> Position:
        print(dType.GetPose(self.__api))
        return 

    def getConnectionState(self) -> str:
        return CON_STR[self.__conn]

    def disconnect(self) -> None:
        dType.DisconnectDobot(self.__api)