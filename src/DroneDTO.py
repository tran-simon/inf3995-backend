from Drone import Drone
from Dronesim import Dronesim



class DroneDTO:
    droneId = ''
    battery = -1
    speed = 0.0
    state = ""

    def  __init__(self, isSim, drone):
        if (isSim):
            self.droneId = drone.getId()
            self.battery = drone.getBattery()
            self.speed = drone.getSpeed()

            switcher = {
                -1 : "No State Received",
                0 : "Start",
                1 : "Take Off",
                2 : "Explore",
                3 : "Go To Base",
                4 : "Land"
            }
            self.state = switcher.get(drone.getState())

        else:
            self.droneId = drone.getId()
            self.battery = drone.getChannel().getBatteryLevel()
            self.speed = drone.getChannel().getSpeed()
            self.state = drone.getChannel().getState()

