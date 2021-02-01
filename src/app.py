from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

activated = False
battery = 100

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