import pytest
import sys
import requests
import os
sys.path.append("..")
from App import *


def test_before_first_request_should_call_os_path_dirname(mocker):
    spy = mocker.spy(os.path, 'dirname')
    before_first_request()
    spy.assert_called_once_with(os.path.abspath('/root/backend/src/App.py'))

#PAS SUR DU TYPE D'INPUT POUR LA FCT
def test_get_latest_data_should_return_the_data_for_the_specified_type():
    expected_value = '0'
    actual_value = getLatestData("0s")
    assert expected_value == actual_value

def test_reset_should_set_is_sim_to_false_if_http_parameter_is_false():
    expected_value = False
    response = requests.get('http://0.0.0.0:5000/reset', params={'simulation': 'false'})
    assert expected_value == response.json()

def test_reset_should_set_is_sim_to_true_if_http_parameter_is_true():
    expected_value = True
    response = requests.get('http://0.0.0.0:5000/reset', params={'simulation': 'true'})
    assert expected_value == response.json()

# def test_connect_should_delete_sim_drone_list():
#     assert 1 == 1

def test_flash_should_return_the_request_to_the_firmware_server():
    #Le server n'est pas actif, alors la reponse contiendra une erreur
    expected_value = '<Response [500]>'
    response = requests.get('http://0.0.0.0:5000/flash', params={})
    assert expected_value == str(response)

# def test_logs_should_call_send_file(mocker):
#     expected_value = 0
#     mocker.patch('flask.send_file', return_value=0)
#     actual_value = logs()
#     assert expected_value == actual_value
 