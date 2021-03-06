from flask import Flask, jsonify, json
from flask_cors import CORS
from DroneDTO import DroneDTO

from Appchannel import updateDrones
import socket


s = socket.socket()
droneList = []
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
        buffer_array = buffer.decode("utf-8").rsplit(".")
        value = buffer_array.pop(len(buffer_array) - 1)
        value = value[:2] + '.' + value[2:]
        value = value[:4]
        value = value + "%"
        return value
    else: 
        for drone in droneList:
            try:

                drone.getChannel().sendPacket(b'b')
                drone.getChannel().sendPacket(b'v')
                drone.getChannel().sendPacket(b's')
            except:
                continue
    return getStats()


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
    return "Connected"

