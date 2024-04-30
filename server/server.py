from wsgiref.simple_server import make_server
from flask import Flask
from dbHandler import *
from server.mapHandler import *
from dbHandler import *
from server.mapHandler import *
from flask_cors import CORS
from flask import request
import os.path
#set up CORS
app = Flask(__name__)
cors = CORS(app)
@app.route("/getStarData",methods=['POST'])
def server():
    #check if db exists
    if(not(os.path.isfile('stars.db'))):
        createDatabase()
        parseCSVStars()
        addPlanets()
    # get params from request
    lat = request.json['lat']
    lon = request.json['lon']
    date = request.json['date']
    time = request.json['time']
    bufToReturn = makeMap(time,date,lat,lon)
    return bufToReturn



       
