from flask import Flask
from flask_cors import CORS
from pyrebase import pyrebase
from pyngrok import ngrok
from Appchannel import AppchannelCommunicate, updateDrones
from Drone import Drone

droneList = []


app = Flask(__name__)
CORS(app)

#Connection to Ngrok tunnel
public_url = ngrok.connect(5000).public_url

#Initialisation of the database
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


#Connection to drones
droneList = updateDrones(droneList)

@app.route("/getStats")
def getStats():
    for i,d in enumerate(droneList):
        #d.getChannel().sendPacket(b's')
        #d.getChannel().sendPacket(b'v')
        d.getChannel().sendPacket(b'b')
        battery = "{:.2f}".format(d.getChannel().getBatteryLevel())
        route = "battery" + str(i)
        firebase.update({route: battery})

    firebase.update({"number": len(droneList)})
    return {'result': True}
    


