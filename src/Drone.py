class Drone:
    __id = ""
    __channel = ""

    def __init__(self, id, channel):
        self.__id = id
        self.__channel = channel

    def getId(self):
        return self.__id

    def getChannel(self):
        return self.__channel

    def destroy(self):
        self.__channel._cf.close_link()
