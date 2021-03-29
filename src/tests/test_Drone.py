import pytest
import sys
import cflib
sys.path.append("..")
from Drone import *
from Appchannel import AppchannelCommunicate

channel = AppchannelCommunicate(0)
drone = Drone(0, channel)

def test_getId():
    global drone
    expected_id = 0
    actual_id = drone.getId()
    assert expected_id == actual_id

def test_getChannel():
    global drone
    global channel
    expected_channel = channel
    actual_channel = drone.getChannel()
    assert expected_channel == actual_channel