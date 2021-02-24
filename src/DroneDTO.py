from Drone import Drone


class DroneDTO:
    droneId = ''
    battery = -1

    def  __init__(self, drone: Drone ):
        self.droneId = drone.getId()
        self.battery = drone.getChannel().getBatteryLevel()
