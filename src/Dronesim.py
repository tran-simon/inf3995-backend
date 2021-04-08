class Dronesim:
    __id = ""
    __socket = None
    __battery = -1
    __speed = -1
    __state = -1
    __position = -1
    __sensors = -1
    _lastPos = -1
    _curDifference = 0

    def __init__(self, id, socket):
        self.__id = id
        self.__socket = socket
        self.__battery = -1
        self.__speed = -1
        self.__state = -1
        self.__position = [-1, -1]
        self.__sensors = [-1, -1, -1, -1]
        self._lastPos = -1
        self._curDifference = 0.0

    def getId(self):
        return self.__id

    def getSocket(self):
        return self.__socket

    def getBattery(self):
        return self.__battery

    def getSpeed(self):
        return self.__speed

    def getState(self):
        return self.__state

    def getPosition(self):
        return self.__position

    def getSensors(self):
        return self.__sensors

    def setBattery(self, battery):
        try:
            if battery is not None:
                self.__battery = round(float(battery.rstrip('\x00')) * 100)
        except:
            print("Error: Battery Not a number: ", battery)

    def setSpeed(self, speed):
        try:
            if speed is not None:
                self.__speed = round(float(speed.rstrip('\x00')), 3)
        except:
            print("Error: Speed Not a number: ", speed)

    def setState(self, state):
        try:
            if state is not None:
                self.__state = int(state.rstrip('\x00'))
        except:
            print("Error: State Not a number: ", state)

    def setPosition(self, position):
        try:
            if position is not None and len(position) >= 2:
                if(self._lastPos != -1):
                    difference = float(position[1]) - self._lastPos
                    if(difference > 2.0 or difference < -2.0):
                        self._curDifference -= difference
                self._lastPos = float(position[1])
                newPositions = []
                newPositions.append(str(float(position[0])*10.0))
                newPositions.append(str((float(position[1])*10.0) + (self._curDifference * 10.0)))
                self.__position = newPositions
        except:
            print("Error in setPosition: ", position)

    def setSensors(self, sensors_array):
        try:
            if sensors_array is not None:
                self.__sensors = [str(float(s)/10.0) for s in sensors_array]
        except:
            print("Error in setSensors: ", sensors_array)
