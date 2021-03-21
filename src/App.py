import socket
import threading
import selectors
import types

from flask import Flask, jsonify, request
from flask_cors import CORS

from Appchannel import updateDrones
from DroneDTO import DroneDTO
from Dronesim import Dronesim

s = socket.socket()
droneList = []
simDroneList = []
isSim = False
droneCount = 0
sel = selectors.DefaultSelector()

app = Flask(__name__)
CORS(app)


# Connection to drones
updateDrones(droneList)


# Met a jour le statut des crazyflies. Retourne le statut
@app.route("/updateStats")
def updateStats():
    if(isSim):
        global s
        check_sim()

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
    global simDroneList
    try:
        for drone in simDroneList:
            drone.getSocket().send(b's')
    except socket.error as e:
        return str(e)

    if(isSim):
        try:
            global s
            for drone in simDroneList:
                return drone.getSocket().jsonify()
                drone.getSocket().send(b's')
                drone.getSocket().flush()

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
            global simDroneList
            for drone in simDroneList:
                drone.getSocket().send(b'l')
                drone.getSocket().flush()

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
    global simDroneList
    for i in droneList:
        i.destroy()
    del droneList[:]
    if request.args.get("simulation") == 'true':
        simDroneList = []
        connect()
        isSim = True
    else:
        isSim = False
    return jsonify(isSim)


def check_sim():
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)


def accept_wrapper(sock):
    global droneCount
    conn, addr = sock.accept()  # Should be ready to read
    simDroneList.append(Dronesim(droneCount, conn))
    droneCount += 1



def connect():
    global s
    HOST = '0.0.0.0'  # The server's hostname or IP address
    PORT = 80   # The port used by the server
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen()
        print('listening on', (HOST, PORT))
        s.setblocking(False)
        sel.register(s, selectors.EVENT_READ, data=None)  
        check_sim()      
        
    except socket.error as e:
        return str(e)


