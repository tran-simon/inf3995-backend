from flask import Flask, jsonify
from flask_cors import CORS

from Appchannel import updateDrones

droneList = []


app = Flask(__name__)
CORS(app)

# Connection to drones
updateDrones(droneList)

@app.route("/getStats")
def getStats():
    res = {}
    for drone in droneList:
        try:
            drone.getChannel().sendPacket(b'b')
            battery = drone.getChannel().getBatteryLevel()
            res[drone.getId()] = battery
        except:
            continue
    return jsonify(res)

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


@app.route('/scan')
def scan():
    global droneList
    updateDrones(droneList)
    if len(droneList) > 0:
        return jsonify([drone.getId() for drone in droneList])
    else:
        return 'No Crazyflies found', 500




