import socket

from flask import Flask, jsonify, request
from flask_cors import CORS

from Appchannel import updateDrones
from DroneDTO import DroneDTO
from Dronesim import Dronesim

simulation_is_connected = False
s = socket.socket()
droneList = []
simDroneList = []
isSim = True


app = Flask(__name__)
CORS(app)


# Connection to drones
updateDrones(droneList)


# Met a jour le statut des crazyflies. Retourne le statut
@app.route("/updateStats")
def updateStats():
    if(isSim):
        global s

        buffer = s.recv(1024)
        state_array = buffer.decode("utf-8").rsplit('s')
        battery_array = buffer.decode("utf-8").rsplit('b')
        speed_array = buffer.decode("utf-8").rsplit('v')

        state = getLatestData(state_array.pop(len(state_array) - 1))
        battery = getLatestData(battery_array.pop(len(battery_array) - 1))
        speed = getLatestData(speed_array.pop(len(speed_array) - 1))

        for drone in simDroneList:
            drone.setState(state)
            drone.setBattery(battery)
            drone.setSpeed(speed)
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
    if (isSim):
        return jsonify([DroneDTO(True, drone).__dict__ for drone in simDroneList])
    return jsonify([DroneDTO(False, drone).__dict__ for drone in droneList])


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
    global isSim
    global simulation_is_connected
    for i in droneList:
        i.destroy()
    del droneList[:]
    isSim = request.args.get("simulation")
    if(isSim and not simulation_is_connected):
        connect()


@app.route("/connect")
def connect():
    global s
    global simDroneList
    HOST = '172.17.0.1'  # The server's hostname or IP address
    PORT = 80        # The port used by the server
    try:
        simDroneList = []
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        numberOfDrones = s.recv(1024)
        i = 0
        while i < int(numberOfDrones):
            simDroneList.append(Dronesim(i))
            i += 1
        return numberOfDrones
    except:
        print("Error")
        return 'Error', 500


