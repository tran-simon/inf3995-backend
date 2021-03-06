class Dronesim:
    __id = ""
    __battery = -1
    __speed = -1
    __state = -1

    def __init__(self, id):
        self.__id = id
        self.__battery = -1
        self.__speed = -1
        self.__state = -1

    def getId(self):
        return self.__id

    def getBattery(self):
        return self.__battery

    def getSpeed(self):
        return self.__speed

    def getState(self):
        return self.__state

    def setBattery(self, battery):
        if battery is not None:
            self.__battery = battery

    def setSpeed(self, speed):
        if speed is not None:
            self.__speed = speed

    def setState(self, state):
        if state is not None:
            self.__state = state
