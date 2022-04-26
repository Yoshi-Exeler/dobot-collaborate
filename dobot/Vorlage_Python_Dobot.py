# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 07:36:39 2020
@author: Digital Hub
"""

#Bibliothek importieren
import DobotDllType as dType #impotieren der Ausführbefehle in "DobotD11Type"

#Dobot konfigurieren
CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

api = dType.load() #Dll laden und Verwendung des CDLL Objekts

#Verbindung zu Dobot herstellen
state = dType.ConnectDobot(api, "COM3", 115200)[0] #!Achten Sie bei dem Betrieb mehrerer DOBOT auf den richtigen seriellen Port!
print("Connect status:",CON_STR[state])

if (state == dType.DobotConnect.DobotConnect_NoError):
    print("Setting up Command Queue")
    dType.SetQueuedCmdClear(api)                        #Clean Command Queued
    dType.SetQueuedCmdStartExec(api)                    #Befehlswarteschlange starten
    dType.SetPTPCmdEx(api, 0, 193,  0,  23, -0.264, 1)      #optional Jump-Befehl zur absoluten Koordinate zu Beginn
    dType.dSleep(100)                                   #Verzögerungszeit wird benötigt, um Befehl auszuführen
    
    print("Homing")
    dType.SetHOMEParams(api, 250, 0, 50, 0, isQueued = 1)
    dType.SetHOMECmd(api, 0, isQueued = 1)
    
    while (not dType.GetQueuedCmdMotionFinish(api)[0]):
        print("Waiting... Current: ", dType.GetQueuedCmdCurrentIndex(api))
        dType.dSleep(200)


    #HIER WIRD DER PYTHON CODE AUS BLOCKLY EINGEFÜGT
    print("Move")
    current_pose = dType.GetPose(api)
    dType.SetPTPCmdEx(api, 2, 200,  0,  50, current_pose[3], 1)
    dType.SetEndEffectorSuctionCupEx(api, 1, 1)
    current_pose = dType.GetPose(api)
    dType.SetPTPCmdEx(api, 2, 200,  0,  100, current_pose[3], 1)
    dType.SetEndEffectorSuctionCupEx(api, 0, 1)
    print("Sleep")
    dType.dSleep(100)

    #Abschlusskommandos
    print("Stop Queues")
    dType.SetQueuedCmdStopExec(api) #Warten auf Befehle stoppen
    
    dType.SetQueuedCmdForceStopExec(api)
    print("Stop all queues")
dType.DisconnectDobot(api)      #Verbindung zum Roboter trennen
print("Disconnectet - Dobot programm stopped")

