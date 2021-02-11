from flask import Flask
from flask_cors import CORS
from pyrebase import pyrebase
from pyngrok import ngrok
from Appchannel import AppchannelCommunicate
import time
import cflib
from cflib.crazyflie import Crazyflie

app = Flask(__name__)
CORS(app)

activated = 0
battery = 100
comm = None

public_url = ngrok.connect(5000).public_url

config = {
    "apiKey": "AIzaSyAp9j7bZz1OXvO8ZJElH36pKarkLQdOg-o",
    "authDomain": "inf3995-100.firebase.com",
    "databaseURL": "https://inf3995-100-default-rtdb.firebaseio.com/",
    "storageBucket": "inf3995-100.appspot.com"
}

split_url = public_url.split(":")
privatize = split_url[0] + "s:" + split_url[1]

firebase = pyrebase.initialize_app(config).database()
firebase.update({"url": privatize})

@app.route('/')
def main():
    global battery
    global activated

    return 'Activated: {}, Battery: {}'.format(activated, battery)


@app.route('/scan')
def scan():
    global comm
    cflib.crtp.init_drivers(enable_debug_driver=False)
    print('Scanning interfaces for Crazyflies...')
    available = cflib.crtp.scan_interfaces()
    print('Crazyflies found:')
    if len(available) > 0:
        comm = AppchannelCommunicate(available[0][0])
        return 'Found a Crazyflie'
    else:
        print('No Crazyflies found, waiting 3 seconds')
        return 'No Crazyflies found', 500


@app.route("/changeState")
def changeState():
    global activated
    try:
        activated = activated ^ 1
        comm._sendPacket(b'l')
        return {'result': activated}
    except:
        print("Error")
        return 'Error', 500


@app.route("/getState")
def getState():
    global activated
    return {'result': activated}


@app.route("/getBatteryLevel")
def getBatteryLevel():
    global battery
    try:
        comm._sendPacket(b'b')
        battery = "{:.2f}".format(comm._getBatteryLevel())
        return {'result': battery}
    except:
        print("Error")
        return 'Error', 500
