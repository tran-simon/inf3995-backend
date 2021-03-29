import pytest
import sys
import cflib
sys.path.append("..")
from DroneDTO import *
from Appchannel import AppchannelCommunicate
from Drone import *
from Dronesim import *

drone = Drone(0, AppchannelCommunicate(0))
drone.getChannel().setBattery(90.0)
drone.getChannel().setSpeed(10.0)
drone.getChannel().setState(1)

droneSim = Dronesim(0, 1)
droneSim.setBattery("0.90")
droneSim.setSpeed("10.0")
droneSim.setState("1")

def test_init_sim_in_mission():
    global droneSim
    expected_attributes = [0, 90.0, 10.0, "In mission"]
    actual_attributes = []

    droneDTO = DroneDTO(True, droneSim)

    actual_attributes.append(droneDTO.droneId)
    actual_attributes.append(droneDTO.battery)
    actual_attributes.append(droneDTO.speed)
    actual_attributes.append(droneDTO.state)

    assert expected_attributes == actual_attributes

def test_init_sim_standby():
    global droneSim
    droneSim.setState("0")
    expected_attributes = [0, 90.0, 10.0, "Standby"]
    actual_attributes = []

    droneDTO = DroneDTO(True, droneSim)

    actual_attributes.append(droneDTO.droneId)
    actual_attributes.append(droneDTO.battery)
    actual_attributes.append(droneDTO.speed)
    actual_attributes.append(droneDTO.state)

    assert expected_attributes == actual_attributes

def test_init_sim_not_received():
    global droneSim
    droneSim.setState("-1")
    expected_attributes = [0, 90.0, 10.0, "No State Received"]
    actual_attributes = []

    droneDTO = DroneDTO(True, droneSim)

    actual_attributes.append(droneDTO.droneId)
    actual_attributes.append(droneDTO.battery)
    actual_attributes.append(droneDTO.speed)
    actual_attributes.append(droneDTO.state)

    assert expected_attributes == actual_attributes

def test_init_real_in_mission():
    global drone
    expected_attributes = [0, 90.0, 10.0, "In mission"]
    actual_attributes = []

    droneDTO = DroneDTO(False, drone)

    actual_attributes.append(droneDTO.droneId)
    actual_attributes.append(droneDTO.battery)
    actual_attributes.append(droneDTO.speed)
    actual_attributes.append(droneDTO.state)

    assert expected_attributes == actual_attributes

def test_init_real_standby():
    global drone
    drone.getChannel().setState(0)
    expected_attributes = [0, 90.0, 10.0, "Standby"]
    actual_attributes = []

    droneDTO = DroneDTO(False, drone)

    actual_attributes.append(droneDTO.droneId)
    actual_attributes.append(droneDTO.battery)
    actual_attributes.append(droneDTO.speed)
    actual_attributes.append(droneDTO.state)

    assert expected_attributes == actual_attributes
