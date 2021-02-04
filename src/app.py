from flask import Flask
from flask_cors import CORS
from pyrebase import pyrebase
from pyngrok import ngrok

app = Flask(__name__)
CORS(app)

activated = False
battery = 100

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


@app.route("/changeState")
def changeState():
    global activated
    activated = not activated
    return {'result': activated}


@app.route("/getState")
def getState():
    global activated
    return {'result': activated}


@app.route("/getBatteryLevel")
def getBatteryLevel():
    global battery
    battery -= 1
    return {'result': battery}


