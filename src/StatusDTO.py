"""Satus Data Transfert Object allowing other processess to know if we are in simulation or real drones"""
class StatusDTO:
    simulation = False
    def __init__(self, sim):
        self.simulation = sim

