import pytest
import sys
import requests
import os
sys.path.append("..")
from App import *
import App


def test_before_first_request_should_call_os_path_dirname(mocker):
    spy = mocker.spy(os.path, 'dirname')
    before_first_request()
    spy.assert_called_once_with(os.path.abspath('/root/backend/src/App.py'))

def test_get_latest_data_should_return_the_data_for_the_specified_type():
    expected_value = '0'
    actual_value = getLatestData("0s")
    assert expected_value == actual_value

def test_reset_should_set_is_sim_to_false_if_http_parameter_is_false():
    expected_value = False
    droneList.append(Dronesim(str(1), "test"))
    response = requests.get('http://0.0.0.0:5000/reset', params={'simulation': 'false'})
    assert expected_value == response.json()

def test_reset_should_set_is_sim_to_true_if_http_parameter_is_true():
    expected_value = True
    simDroneList.append(Dronesim(str(1), "test"))
    response = requests.get('http://0.0.0.0:5000/reset', params={'simulation': 'true'})
    assert expected_value == response.json()

def test_flash_should_return_the_request_to_the_firmware_server():
    expected_value = 500
    response = requests.get('http://0.0.0.0:5000/flash', params={})
    assert expected_value == response.status_code

def test_update_stats_should_return_a_json():
    expected_value = []
    requests.get('http://0.0.0.0:5000/reset', params={'simulation': 'false'})
    response = requests.get('http://0.0.0.0:5000/updateStats')
    assert expected_value == response.json()
    requests.get('http://0.0.0.0:5000/reset', params={'simulation': 'true'})
    response = requests.get('http://0.0.0.0:5000/updateStats')
    assert expected_value == response.json()

def test_live_check_returns_sim_string():
    expected_value = {'simulation': True}
    response = requests.get('http://0.0.0.0:5000/liveCheck')
    assert expected_value == response.json()
    requests.get('http://0.0.0.0:5000/reset', params={'simulation': 'false'})
    expected_value = {'simulation': False}
    response = requests.get('http://0.0.0.0:5000/liveCheck')
    assert expected_value == response.json()

def test_logs_should_call_send_file():
    expected_value = 200
    response = requests.get('http://0.0.0.0:5000/logs')
    assert expected_value == response.status_code