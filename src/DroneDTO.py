from Drone import Drone
from Dronesim import Dronesim



class DroneDTO:
    droneId = ''
    battery = -1
    speed = 0
    state = ""
    sensors = {-1, -1, -1, -1}

    def  __init__(self, isSim, drone):
        if (isSim):
            self.droneId = drone.getId()
            self.battery = drone.getBattery()
            self.speed = drone.getSpeed()
            self.sensors = drone.getSensors()

            switcher = {
                -1 : "No State Received",
                0 : "Standby",
                1 : "In mission",
                2 : "In mission",
                3 : "In mission",
                4 : "Standby"
            }
            self.state = switcher.get(drone.getState())

        else:
            self.droneId = drone.getId()
            self.battery = drone.getChannel().getBatteryLevel()
            self.speed = drone.getChannel().getSpeed()
            self.state = drone.getChannel().getState()

