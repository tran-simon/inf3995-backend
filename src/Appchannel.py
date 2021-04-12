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
from cflib.crazyflie.mem import MemoryElement, I2CElement
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
    __position_array = [-1, -1]
    __sensor_array = [-1, -1, -1, -1]

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
        (value1, value2, value3, value4, value5, value6, infoType) = struct.unpack("<ffffffc", data)

        if(infoType == b'b'):
            batPercentage = vbatToPourcentage(value1)
            self.setBattery(batPercentage)

        elif(infoType == b'v'):
            self.setSpeed(value1)

        elif(infoType == b's'):
            self.setState(value1)

        elif(infoType == b'm'):
            print("x value is: ",value1)
            print("y value is: ", value2)
            print("front distance value is: ", value3)
            print("back distance value is: ", value4)
            print("left distance value is: ", value5)
            print("right distance value is: ", value6)
            position_array = [str(value2*-10.0), str(value1*-10.0)]
            sensor_array = [str(value4/10.0), str(value3/10.0), str(value6/10.0), str(value5/10.0)]
            self.setPositonArray(position_array)
            self.setSensorArray(sensor_array)



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

    def getPositionArray(self):
        return self.__position_array

    def getSensorArray(self):
        return self.__sensor_array

    def setBattery(self, value):
        self.__batteryLevel = value

    def setSpeed(self, value):
        self.__speed = value
    
    def setState(self, value):
        self.__state = value

    def setPositonArray(self, value):
        self.__position_array = value
    
    def setSensorArray(self, value):
        self.__sensor_array = value
        
        


def vbatToPourcentage(voltage):
        if 4.2 >= voltage > 4.15:
            return 100
        if 4.15 >= voltage > 4.11:
            return 95
        if 4.11 >= voltage > 4.08:
            return 90
        if 4.08 >= voltage > 4.02:
            return 85
        if 4.02 >= voltage > 3.98:
            return 80
        if 3.98 >= voltage > 3.95:
            return 75
        if 3.95 >= voltage > 3.91:
            return 70
        if 3.91 >= voltage > 3.87:
            return 65
        if 3.87 >= voltage > 3.85:
            return 60
        if 3.85 >= voltage > 3.84:
            return 55
        if 3.84 >= voltage > 3.82:
            return 50
        if 3.82 >= voltage > 3.8:
            return 45
        if 3.8 >= voltage > 3.79:
            return 40
        if 3.79 >= voltage > 3.77:
            return 35
        if 3.77 >= voltage > 3.75:
            return 30
        if 3.75 >= voltage > 3.73:
            return 25
        if 3.73 >= voltage > 3.71:
            return 20
        if 3.71 >= voltage > 3.69:
            return 15
        if 3.69 >= voltage > 3.61:
            return 10
        if 3.61 >= voltage > 3.27:
            return 5
        if voltage < 3.27:
            return 0



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
    drones = connectToDrone() #Returns amount of drones 
    print(drones)

    #if(len(drones) > 0):
            #for i in drones:
                #drone = Drone(drones[i], AppchannelCommunicate(drones[i]))
                #droneList.append(drone)
   # else:
        #drone = Drone(drones[0], AppchannelCommunicate(drones[0]))
        #droneList.append(drone)

    for d in drones:
        drone = Drone(d[0], AppchannelCommunicate(d[0]))
        if(len(droneList) > 0):
            if (drone.getId() not in [i.getId() for i in droneList]):
                droneList.append(drone)
        else:
            droneList.append(drone)

