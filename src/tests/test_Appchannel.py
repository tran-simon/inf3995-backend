import pytest
import sys
sys.path.append("..")
from Appchannel import *
from Drone import *

channel = AppchannelCommunicate(0)

def test_call_back_functions_should_not_crash():
    channel.connected(0)
    channel.connectionFailed(0,'test')
    channel.connectionLost(0, 'test')
    channel.disconnected(0)
    assert 1 == 1

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

def test_set_get_position_array():
    global channel
    expected_array = ['10.0', '10.0']
    channel.setPositonArray(['10.0', '10.0'])
    actual_array = channel.getPositionArray()
    assert expected_array == actual_array

def test_set_get_sensors_array():
    global channel
    expected_array = ['1.0', '1.0', '1.0', '1.0']
    channel.setSensorArray(['1.0', '1.0', '1.0', '1.0'])
    actual_array = channel.getSensorArray()
    assert expected_array == actual_array

def test_app_packet_received_with_state_command():
    expected_value = 'In mission'
    command = b's'
    value1 = 1.0
    value2 = 0.0
    value3 = 0.0
    value4 = 0.0
    value5 = 0.0
    value6 = 0.0
    data = struct.pack("<ffffffc", value1, value2, value3, value4, value5, value6, command)
    channel.appPacketReceived(data)
    actual_value = channel.getState()
    assert expected_value == actual_value

def test_app_packet_received_with_speed_command():
    expected_value = 10.0
    command = b'v'
    value1 = 10.0
    value2 = 0.0
    value3 = 0.0
    value4 = 0.0
    value5 = 0.0
    value6 = 0.0
    data = struct.pack("<ffffffc", value1, value2, value3, value4, value5, value6, command)
    channel.appPacketReceived(data)
    actual_value = channel.getSpeed()
    assert expected_value == actual_value

#A CHANGER
def test_app_packet_received_with_battery_command():
    expected_value = 10.0
    command = b'b'
    value1 = 10.0
    value2 = 0.0
    value3 = 0.0
    value4 = 0.0
    value5 = 0.0
    value6 = 0.0
    data = struct.pack("<ffffffc", value1, value2, value3, value4, value5, value6, command)
    channel.appPacketReceived(data)
    actual_value = channel.getBatteryLevel()
    assert None == actual_value

def test_app_packet_received_with_map_command():
    expected_value = [['-100.0', '-100.0'], ['1.0', '1.0', '1.0', '1.0']]
    command = b'm'
    value1 = 10.0
    value2 = 10.0
    value3 = 10.0
    value4 = 10.0
    value5 = 10.0
    value6 = 10.0
    data = struct.pack("<ffffffc", value1, value2, value3, value4, value5, value6, command)
    channel.appPacketReceived(data)
    actual_position = channel.getPositionArray()
    actual_sensors = channel.getSensorArray()
    actual_value = [actual_position, actual_sensors]
    assert expected_value == actual_value

def test_send_packet_calls_cf_appchannel_send_packet(mocker):
    global channel
    spy = mocker.spy(channel._cf.appchannel, 'send_packet')
    channel.sendPacket(b'b')
    spy.assert_called_once_with(b'b')

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

def test_vbat_to_pourcentage_first_interval():
    expected_battery = 100
    actual_battery = vbatToPourcentage(4.2)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_second_interval():
    expected_battery = 95
    actual_battery = vbatToPourcentage(4.15)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_third_interval():
    expected_battery = 90
    actual_battery = vbatToPourcentage(4.11)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_fourth_interval():
    expected_battery = 85
    actual_battery = vbatToPourcentage(4.08)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_fifth_interval():
    expected_battery = 80
    actual_battery = vbatToPourcentage(4.02)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_sixth_interval():
    expected_battery = 75
    actual_battery = vbatToPourcentage(3.98)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_seventh_interval():
    expected_battery = 70
    actual_battery = vbatToPourcentage(3.95)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_eight_interval():
    expected_battery = 65
    actual_battery = vbatToPourcentage(3.91)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_nineth_interval():
    expected_battery = 60
    actual_battery = vbatToPourcentage(3.87)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_tenth_interval():
    expected_battery = 55
    actual_battery = vbatToPourcentage(3.85)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_eleventh_interval():
    expected_battery = 50
    actual_battery = vbatToPourcentage(3.84)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_twelveth_interval():
    expected_battery = 45
    actual_battery = vbatToPourcentage(3.82)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_thirteenth_interval():
    expected_battery = 40
    actual_battery = vbatToPourcentage(3.8)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_fourteenth_interval():
    expected_battery = 35
    actual_battery = vbatToPourcentage(3.79)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_fiftheenth_interval():
    expected_battery = 30
    actual_battery = vbatToPourcentage(3.77)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_sixtheenth_interval():
    expected_battery = 25
    actual_battery = vbatToPourcentage(3.75)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_seventeenth_interval():
    expected_battery = 20
    actual_battery = vbatToPourcentage(3.73)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_eighteenth_interval():
    expected_battery = 15
    actual_battery = vbatToPourcentage(3.71)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_nineteenth_interval():
    expected_battery = 10
    actual_battery = vbatToPourcentage(3.69)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_twentyth_interval():
    expected_battery = 5
    actual_battery = vbatToPourcentage(3.61)
    assert expected_battery == actual_battery

def test_vbat_to_pourcentage_twentyfirst_interval():
    expected_battery = 0
    actual_battery = vbatToPourcentage(3.26)
    assert expected_battery == actual_battery