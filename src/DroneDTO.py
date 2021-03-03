from Drone import Drone


class DroneDTO:
    droneId = ''
    battery = -1
    speed = 0.0
    state = ""

    def  __init__(self, drone: Drone ):
        self.droneId = drone.getId()
        self.battery = "{:.2f}".format(drone.getChannel().getBatteryLevel())
        self.speed = drone.getChannel().getSpeed()
        self.state = drone.getChannel().getState()
