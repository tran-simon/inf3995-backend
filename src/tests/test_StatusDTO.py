import pytest
import sys
sys.path.append("..")
from StatusDTO import *

def test_init_set_simulation_value_true():
    expected_sim_value = True
    status = StatusDTO(True)
    actual_sim_value = status.simulation
    assert expected_sim_value == actual_sim_value

def test_init_set_simulation_value_false():
    expected_sim_value = False
    status = StatusDTO(False)
    actual_sim_value = status.simulation
    assert expected_sim_value == actual_sim_value