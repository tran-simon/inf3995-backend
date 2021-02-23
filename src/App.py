from flask import Flask, jsonify, json
from flask_cors import CORS
from DroneDTO import DroneDTO

from Appchannel import updateDrones

droneList = []


app = Flask(__name__)
CORS(app)

# Connection to drones
updateDrones(droneList)


# Met a jour le statut des crazyflies. Retourne le statut
@app.route("/updateStats")
def updateStats():
    for drone in droneList:
        try:
            drone.getChannel().sendPacket(b'b')
            drone.getChannel().sendPacket(b'v')
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
    updateDrones(droneList)
    return updateStats()

# Permet de verifier que le backend est bien connecte
@app.route('/liveCheck')
def liveCheck():
    return 'OK', 200


@app.route("/takeOff")
def takeOff():
    try:
        for d in droneList:
            d.getChannel().sendPacket(b't')

        return {'result': True}
    except:
        print("Error")
        return 'Error', 500


@app.route("/land")
def land():
    try:
        for d in droneList:
            d.getChannel().sendPacket(b'l')

        return {'result': True}
    except:
        print("Error")
        return 'Error', 500
