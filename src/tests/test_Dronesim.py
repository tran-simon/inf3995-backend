import pytest
import sys
import cflib
sys.path.append("..")
from Dronesim import *

droneSim = Dronesim(0, 1)

def test_get_id():
    global droneSim
    expected_id = 0
    actual_id = droneSim.getId()
    assert expected_id == actual_id

def test_get_socket():
    global droneSim
    expected_socket = 1
    actual_socket = droneSim.getSocket()
    assert expected_socket == actual_socket

def test_set_get_battery():
    global droneSim
    expected_battery = 50.0
    droneSim.setBattery("0.50")
    actual_battery = droneSim.getBattery()
    assert expected_battery == actual_battery

def test_set_get_battery_should_not_change_value_if_battery_is_none():
    global droneSim
    expected_battery = 50.0
    droneSim.setBattery("0.50")
    droneSim.setBattery(None)
    actual_battery = droneSim.getBattery()
    assert expected_battery == actual_battery

def test_set_get_battery_should_not_change_value_if_battery_is_not_a_string_of_an_int():
    global droneSim
    expected_battery = 50.0
    droneSim.setBattery("0.50")
    droneSim.setBattery("test")
    actual_battery = droneSim.getBattery()
    assert expected_battery == actual_battery

def test_set_get_speed():
    global droneSim
    expected_speed = 10.0
    droneSim.setSpeed("10.0")
    actual_speed = droneSim.getSpeed()
    assert expected_speed == actual_speed

def test_set_get_speed_should_not_change_value_if_speed_is_none():
    global droneSim
    expected_speed = 10.0
    droneSim.setSpeed("10.0")
    droneSim.setSpeed(None)
    actual_speed = droneSim.getSpeed()
    assert expected_speed == actual_speed

def test_set_get_speed_should_not_change_value_if_speed_is_not_a_string_of_an_int():
    global droneSim
    expected_speed = 10.0
    droneSim.setSpeed("10.0")
    droneSim.setSpeed("test")
    actual_speed = droneSim.getSpeed()
    assert expected_speed == actual_speed

def test_set_get_state():
    global droneSim
    expected_state = 1
    droneSim.setState('1')
    actual_state = droneSim.getState()
    assert expected_state == actual_state

def test_set_get_state_should_not_change_value_if_state_is_none():
    global droneSim
    expected_state = 1
    droneSim.setState('1')
    droneSim.setState(None)
    actual_state = droneSim.getState()
    assert expected_state == actual_state

def test_set_get_state_should_not_change_value_if_state_is_not_a_string_of_an_int():
    global droneSim
    expected_state = 1
    droneSim.setState('1')
    droneSim.setState('test')
    actual_state = droneSim.getState()
    assert expected_state == actual_state

# def test_set_get_position():
#     global droneSim
#     expected_pos = (10.0,10.0)
#     droneSim.setPosition((10.0,10.0))
#     actual_pos = droneSim.getPosition()
#     assert expected_pos == actual_pos

# def test_set_get_position_should_not_change_value_if_pos_is_none():
#     global droneSim
#     expected_pos = (10.0,10.0)
#     droneSim.setPosition((10.0,10.0))
#     droneSim.setPosition(None)
#     actual_pos = droneSim.getPosition()
#     assert expected_pos == actual_pos

# def test_set_get_sensors():
#     global droneSim
#     expected_sensors = [10.0,5.0,10.0,5.0]
#     droneSim.setSensors([10.0,5.0,10.0,5.0])
#     actual_sensors = droneSim.getSensors()
#     assert expected_sensors == actual_sensors

# def test_set_get_sensors_should_not_change_value_if_array_is_none():
#     global droneSim
#     expected_sensors = [0.0,0.0,0.0,0.0]
#     droneSim.setSensors([0.0,0.0,0.0,0.0])
#     droneSim.setSensors(None)
#     actual_sensors = droneSim.getSensors()
#     assert expected_sensors == actual_sensors

def test_set_get_position():
    global droneSim
    expected_pos = ['100.0','100.0']
    droneSim.setPosition((10.0,10.0))
    actual_pos = droneSim.getPosition()
    assert expected_pos == actual_pos

# def test_set_get_position_2():
#     global droneSim
#     expected_pos = ['100.0','100.0']
#     droneSim._lastPos = 110
#     pos = droneSim.setPosition(('10.0','10.0'))
#     actual_pos = droneSim.getPosition()
#     assert droneSim._curDifference == -100.0
