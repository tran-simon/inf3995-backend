from flask import Flask
from flask_cors import CORS
from pyrebase import pyrebase
from Appchannel import AppchannelCommunicate, updateDrones
from Drone import Drone

droneList = []


app = Flask(__name__)
CORS(app)


#Initialisation of the database
config = {
    "apiKey": "AIzaSyAp9j7bZz1OXvO8ZJElH36pKarkLQdOg-o",
    "authDomain": "inf3995-100.firebase.com",
    "databaseURL": "https://inf3995-100-default-rtdb.firebaseio.com/",
    "storageBucket": "inf3995-100.appspot.com"
}
firebase = pyrebase.initialize_app(config).database()


#Connection to drones
updateDrones(droneList)

@app.route("/getStats")
def getStats():
    #try:
    for i,d in enumerate(droneList):
        #d.getChannel().sendPacket(b's')
        #d.getChannel().sendPacket(b'v')
        d.getChannel().sendPacket(b'b')
        battery = "{:.2f}".format(d.getChannel().getBatteryLevel())
        route = "battery" + str(i)
        firebase.update({route: battery})

    firebase.update({"number": len(droneList)})
    return {'result': True}
    #except:
        #print("Error")
        #return 'Error', 500

@app.route("/takeOff")
def takeOff():
    try:
        for i,d in enumerate(droneList):
            d.getChannel().sendPacket(b't')
        
        return {'result': True}
    except:
        print("Error")
        return 'Error', 500


@app.route("/land")
def land():
    try:
        for i,d in enumerate(droneList):
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
        return 'Found a Crazyflie'
    else:
        return 'No Crazyflies found', 500




