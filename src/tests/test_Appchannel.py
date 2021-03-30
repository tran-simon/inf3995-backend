import pytest
#from pytest-mock import mocker
import sys
sys.path.append("..")
from Appchannel import *
from Drone import *

#----------Les tests effectues sont pour les fonctions ajoutees au fichier originel fourni par Bitcraze----------#
channel = AppchannelCommunicate(0)

def test_set_get_battery_level():
    global channel
    expected_battery = 90.0
    channel.setBattery(90.0)
    actual_battery = channel.getBatteryLevel()
    assert expected_battery == actual_battery

def test_set_get_speed_more_than_threshold():
    global channel
    expected_speed = 10.0
    channel.setSpeed(10.0)
    actual_speed = channel.getSpeed()
    assert expected_speed == actual_speed

def test_set_get_speed_less_than_threshold():
    global channel
    expected_speed = 0
    channel.setSpeed(0.00001)
    actual_speed = channel.getSpeed()
    assert expected_speed == actual_speed

def test_set_get_state_in_mission():
    global channel
    expected_state = 'In mission'
    channel.setState(1)
    actual_state = channel.getState()
    assert expected_state == actual_state

def test_set_get_state_standby():
    global channel
    expected_state = 'Standby'
    channel.setState(0)
    actual_state = channel.getState()
    assert expected_state == actual_state

def test_that_udpate_drones_deletes_items_in_drone_list():
    drone_list = [Drone(0,AppchannelCommunicate(1)), Drone(1, AppchannelCommunicate(1))]
    expected_length = 0
    updateDrones(drone_list)
    actual_length = len(drone_list)
    assert expected_length == actual_length

def test_that_udpate_drones_add_new_drones_to_the_list(mocker):
    drone_list = [Drone(0,AppchannelCommunicate(1)), Drone(1, AppchannelCommunicate(1))]
    expected_list = ['2', '3']
    mocker.patch('Appchannel.connectToDrone', return_value=[('2',), ('3',)])
    updateDrones(drone_list)
    actual_list = [i.getId() for i in drone_list]
    assert expected_list == actual_list

def test_that_udpate_drones_doesnt_add_already_included_drones(mocker):
    drone_list = [Drone(0,AppchannelCommunicate(1)), Drone(1, AppchannelCommunicate(1))]
    expected_list = ["2", "3"]
    mocker.patch('Appchannel.connectToDrone', return_value=[("2",), ("3",), ("2",)])
    updateDrones(drone_list)
    actual_list = [i.getId() for i in drone_list]
    assert expected_list == actual_list

def test_that_connect_to_drone_returns_available_channels(mocker):
    expected_list = [("1",),("2",)]
    mocker.patch('cflib.crtp.scan_interfaces', return_value=[("1",), ("2",)])
    actual_list = connectToDrone()
    assert expected_list == actual_list