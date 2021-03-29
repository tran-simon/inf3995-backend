import pytest
import sys
import cflib
sys.path.append("..")
from Dronesim import *

droneSim = Dronesim(0, 1)

def test_getId():
    global droneSim
    expected_id = 0
    actual_id = droneSim.getId()
    assert expected_id == actual_id

def test_getSocket():
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