"""
Main file in which most communications to the backend pass through  
"""
import socket
import socketserver
import requests
import os
import logging
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from Appchannel import updateDrones
from DroneDTO import DroneDTO
from Dronesim import Dronesim
from StatusDTO import StatusDTO

initialPositionList = []
droneList = []
simDroneList = []
isSim = False
numberOfDrones = 2
data = ''

app = Flask(__name__)
CORS(app)

# Connection to drones
updateDrones(droneList)

#https://code-maven.com/python-flask-logging
#https://docs.python.org/3/howto/logging-cookbook.html
@app.before_first_request
def before_first_request():
    log_level = logging.INFO
    root = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(root, 'app.log')
    handler = logging.FileHandler(log_file)
    handler.setFormatter( logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s'))
    handler.setLevel(log_level)
    app.logger.addHandler(handler)
    app.logger.setLevel(log_level)

@app.route("/updateStats")
def updateStats():
    """Updates the status of the crazyflies and returns the status"""
    if(isSim):
        for drone in simDroneList:
            buffer = drone.getSocket().recv(64000)

            state_array = buffer.decode("utf-8").rsplit('s')
            battery_array = buffer.decode("utf-8").rsplit('b')
            speed_array = buffer.decode("utf-8").rsplit('v')
            pos_array = buffer.decode("utf-8").rsplit('l')
            point_array = buffer.decode("utf-8").rsplit('p')

            state = getLatestData(state_array.pop(len(state_array) - 2))
            battery = getLatestData(battery_array.pop(len(battery_array) - 2))
            speed = getLatestData(speed_array.pop(len(speed_array) - 2))
            pos = getLatestData(pos_array.pop(len(pos_array) - 2))
            position = pos.rsplit(';')

            points = getLatestData(point_array.pop(len(point_array) - 2))
            sensors_array = points.rsplit(';')

            drone.setState(state)
            drone.setBattery(battery)
            drone.setSpeed(speed)
            drone.setPosition(position)
            drone.setSensors(sensors_array)
    else:
        for drone in droneList:
            try:
                #Sendings commands to the crazyflie requesting information
                drone.getChannel().sendPacket(b'b')
                drone.getChannel().sendPacket(b'v')
                drone.getChannel().sendPacket(b's')
                drone.getChannel().sendPacket(b'p')
                drone.getChannel().sendPacket(b'm')
            except:
                continue
    return getStats()

def getLatestData(data):
    """String manipulation for information provided from the ARGos simulation"""
    i = 0
    while i < len(data):
        if (data[i] == 's' or data[i] == 'b' or data[i] == 'v' or data[i] == 'l' or data[i] == 'p'):
            return data[:i]
        i += 1

def getStats():
    """Returns the status of the crazyflie"""
    if (isSim):
        return jsonify([DroneDTO(True, drone).__dict__ for drone in simDroneList])
    return jsonify([DroneDTO(False, drone).__dict__ for drone in droneList])

@app.route('/scan')
def scan():
    """Function that allows to scan for crazyflie drones. Returns the status of the crazyflie"""
    global droneList
    if(isSim):
        connect()
    else:
        app.logger.info("scanning crazyflies")
        updateDrones(droneList)
    return updateStats()

@app.route('/liveCheck')
def liveCheck():
    """Verifies if the backend is correctly connected"""
    app.logger.info("liveCheck from " + request.remote_addr + " - simulation: " + str(isSim))
    return jsonify(StatusDTO(isSim).__dict__), 200


@app.route("/takeOff", methods = ['POST', 'GET'])
def takeOff():
    """Sends Take Off command to the drones"""
    global simDroneList
    global initialPositionList

    if request.method == 'POST':
        initialPositionList = request.json

    if(isSim):
        try:
            for drone in simDroneList:
                drone.getSocket().send(b's')
            app.logger.info("simulation takeOff")

            return {'result': True}
        except Exception:
            app.logger.error("Exception during simulation takeoff: " + str(Exception))
            return 'Error', 500
    else:
        try:
            for d in droneList:
                d.getChannel().sendPacket(b't')

            app.logger.info("crazyflie takeOff")
            return {'result': True}
        except:
            app.logger.error("Exception during takeoff: " + str(Exception))
            return 'Error', 500

@app.route("/land")
def land():
    """Sends Land command to the drones"""
    packet = b'r' if request.args.get("return") == 'true' else b'l'
    if(isSim):
        try:
            global simDroneList
            for drone in simDroneList:
                drone.getSocket().send(packet)

            app.logger.info("crazyflie land")

            return {'result': True}
        except Exception:
            app.logger.error("Exception during simulation land: " + str(Exception))
            return 'Error', 500
    else:
        try:
            for d in droneList:
                d.getChannel().sendPacket(packet)

            app.logger.info("crazyflie land")
            return {'result': True}
        except Exception:
            app.logger.error("Exception during land: " + str(Exception))
            return 'Error', 500

@app.route("/reset")
def reset():
    """Resets drone list"""
    global isSim
    global simDroneList
    for i in droneList:
        i.destroy()
    del droneList[:]
    if request.args.get("simulation") == 'true':
        for d in simDroneList:
            (d.getSocket()).close()
        del simDroneList[:]
        isSim = True
    else:
        isSim = False

    app.logger.info("resetting to simulation=" + str(isSim))
    return jsonify(isSim)

@app.route("/connect")
def connect():
    """Initializes a socket connection between simulation and backend"""
    global numberOfDrones
    global data
    global simDroneList
    socketserver.TCPServer.allow_reuse_address = True
    HOST = '0.0.0.0'  # The server's hostname or IP address
    PORT = 80   # The port used by the server
    app.logger.info("Connecting to simulation")
    try:
        for d in simDroneList:
            (d.getSocket()).close()
        del simDroneList[:]

        for i in range(numberOfDrones):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, (PORT + i)))
            s.listen(1)
            conn, addr = s.accept()
            simDroneList.append(Dronesim(str(i), conn))
            conn.send(b't')
            s.close()
        return data

    except socket.error as e:
        app.logger.error("socket error during connection to simulation: " + str(e))
        s.close()
        return str(e)

@app.route("/flash")
def flash():
    """Connects to server in crazyflie firmware to flash drones froms a distance"""
    req = requests.get(os.environ.get("SERVER_URL") + "/flash")

    app.logger.info("flashing crazyflies: " + req.text)
    return req.content

@app.route("/logs")
def logs():
    """Sends Log information to the Frontend"""
    return send_file('app.log', mimetype='text/plain')
