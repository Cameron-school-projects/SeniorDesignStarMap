from wsgiref.simple_server import make_server
from flask import Flask
from dbHandler import *
from pyHandler import *
from dbHandler import *
from pyHandler import *
from flask_cors import CORS
from flask import request
import os.path

app = Flask(__name__)
cors = CORS(app)
@app.route("/getStarData",methods=['POST'])
def server():
    # get params from request
    lat = request.json['lat']
    lon = request.json['lon']
    date = request.json['date']
    time = request.json['time']
    bufToReturn = makeMap(time,date,lat,lon)
    return bufToReturn

if(not(os.path.isfile('stars.db'))):
    createDatabase()
    parseCSVStars()
    addPlanets()

# makeMap("10:00PM","01/05/2008","34-52-11.44N","86-58-29.82E")

       
