from flask import Flask, jsonify, json
from flask_cors import CORS
from DroneDTO import DroneDTO

from Appchannel import updateDrones
import socket

s = socket.socket()
droneList = []
isSim = True

state = -1
battery = -1
velocity = -1

app = Flask(__name__)
CORS(app)


# Connection to drones
updateDrones(droneList)


# Met a jour le statut des crazyflies. Retourne le statut
@app.route("/updateStats")
def updateStats():
    if(isSim):
        global s
        global state
        global battery
        global velocity

        buffer = s.recv(1024)
        state_array = buffer.decode("utf-8").rsplit('s')
        battery_array = buffer.decode("utf-8").rsplit('b')
        velocity_array = buffer.decode("utf-8").rsplit('v')

        state = getLatestData(state_array.pop(len(state_array) - 1)) or state
        battery = getLatestData(battery_array.pop(len(battery_array) - 1)) or battery
        velocity = getLatestData(velocity_array.pop(len(velocity_array) - 1)) or velocity

        return state
    else: 
        for drone in droneList:
            try:

                drone.getChannel().sendPacket(b'b')
                drone.getChannel().sendPacket(b'v')
                drone.getChannel().sendPacket(b's')
            except:
                continue
    return getStats()


def getLatestData(data):
    i = 0
    while i < len(data):
        if (data[i] == 's' or data[i] == 'b' or data[i] == 'v'):
            return data[:i]
        i += 1

# Retourne le statuts des crazyflies
def getStats():
    return jsonify([DroneDTO(drone).__dict__ for drone in droneList])

# Permet de scanner pour des nouveaux crazyflies. Retourne les stats à jours
@app.route('/scan')
def scan():
    global droneList
    if(isSim):
        pass
    else:
        updateDrones(droneList)
    return updateStats()

# Permet de verifier que le backend est bien connecte
@app.route('/liveCheck')
def liveCheck():
    return 'OK', 200


@app.route("/takeOff")
def takeOff():
    if(isSim):
        try:
            global s
            s.send(b's')
            s.flush()
            mess = s.recv(1024)

            return {'result': True}
        except:
            print("Error")
            return 'Error', 500
        
    else:
        try:
            for d in droneList:
                d.getChannel().sendPacket(b't')

            return {'result': True}
        except:
            print("Error")
            return 'Error', 500


@app.route("/land")
def land():
    if(isSim):
        try:
            global s
            s.send(b'l')
            s.flush()
            mess = s.recv(1024)

            return {'result': True}
        except:
            print("Error")
            return 'Error', 500
    else:
        try:
            for d in droneList:
                d.getChannel().sendPacket(b'l')

            return {'result': True}
        except:
            print("Error")
            return 'Error', 500

@app.route("/reset")
def reset():
    for i in droneList:
        i.destroy()
    del droneList[:]
    isSim = True


@app.route("/connect")
def connect():
    global s
    HOST = '172.17.0.1'  # The server's hostname or IP address
    PORT = 80        # The port used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    numberOfDrones = s.recv(1024)
    return numberOfDrones

