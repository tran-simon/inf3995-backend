# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2014 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
"""
Simple example that connects to the first Crazyflie found, Sends and
receive appchannel packets
"""

import logging
import time
from threading import Thread

import struct

import cflib
from cflib.crazyflie import Crazyflie
from Drone import Drone

STATE_STANDBY = "Standby"
STATE_MISSION = "In mission"
STATE_CRASHED = "Crashed"

logging.basicConfig(level=logging.ERROR)
cflib.crtp.init_drivers(enable_debug_driver=False)



class AppchannelCommunicate:
    """Example that connects to a Crazyflie and ramps the motors up/down and
    the disconnects"""
    __batteryLevel = 0.0
    __speed = 0.0
    __state = 0.0

    def __init__(self, link_uri):
        """ Initialize and run the example with the specified link_uri """

        self._cf = Crazyflie()

        self._cf.connected.add_callback(self.connected)
        self._cf.disconnected.add_callback(self.disconnected)
        self._cf.connection_failed.add_callback(self.connectionFailed)
        self._cf.connection_lost.add_callback(self.connectionLost)

        self._cf.appchannel.packet_received.add_callback(self.appPacketReceived)

        self._cf.open_link(link_uri)

        print('Connecting to %s' % link_uri)

    def connected(self, link_uri):
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""


    def connectionFailed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the specified address)"""
        print('Connection to %s failed: %s' % (link_uri, msg))

    def connectionLost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        print('Connection to %s lost: %s' % (link_uri, msg))

    def disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        print('Disconnected from %s' % link_uri)


    def appPacketReceived(self, data):
        (value, infoType) = struct.unpack("<fc", data)

        if(infoType == b'b'):
            self.setBattery(value)

        elif(infoType == b'v'):
            self.setSpeed(value)

        elif(infoType == b's'):
            self.setState(value)

    def sendPacket(self, value):
        data = struct.pack("<c", value)
        self._cf.appchannel.send_packet(data)
        print(f"Sent command: {value}")

        time.sleep(0.01)

    def getBatteryLevel(self):
        return self.__batteryLevel

    def getSpeed(self):
        if(self.__speed < 0.001):
            return 0
        else:
            return self.__speed

    def getState(self):
        if(self.__state > 0.0):
            return "In mission"
        else:
            return "Standby"

    def setBattery(self, value):
        self.__batteryLevel = value

    def setSpeed(self, value):
        self.__speed = value
    
    def setState(self, value):
        self.__state = value



def connectToDrone():
    print('Scanning interfaces for Crazyflies...')
    available = cflib.crtp.scan_interfaces()
    if len(available) > 0:
        print('Crazyflies found:')
    else:
        print('No Crazyflies found')

    return available


def updateDrones(droneList):
    drones = []
    for i in droneList:
        i.destroy()
    del droneList[:]
    drones = connectToDrone()

    for d in drones:
        drone = Drone(d[0], AppchannelCommunicate(d[0]))
        if(len(droneList) > 0):
            for i in droneList:
                if (drone.getId() != i.getId()):
                    droneList.append(drone)
        else:
            droneList.append(drone)

