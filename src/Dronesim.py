class Dronesim:
    __id = ""
    __socket = None
    __battery = -1
    __speed = -1
    __state = -1
    __position = -1
    __sensors = -1

    def __init__(self, id, socket):
        self.__id = id
        self.__socket = socket
        self.__battery = -1
        self.__speed = -1
        self.__state = -1
        self.__position = {-1, -1}
        self.__sensors = {-1, -1, -1, -1}

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
        if battery is not None:
            self.__battery = round(float(battery.rstrip('\x00')) * 100)

    def setSpeed(self, speed):
        if speed is not None:
            self.__speed = round(float(speed.rstrip('\x00')), 3)

    def setState(self, state):
        if state is not None:
            self.__state = int(state.rstrip('\x00'))

    def setPosition(self, position):
        if position is not None:
            self.__position = position

    def setSensors(self, sensors_array):
        if sensors_array is not None:
            self.__sensors = sensors_array
