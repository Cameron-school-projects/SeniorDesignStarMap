from wsgiref.simple_server import make_server
from flask import Flask
from dbHandler import *
from pyHandler import *
from dbHandler import *
from pyHandler import *
from flask_cors import CORS
from flask import request


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
# createDatabase()
# parseCSVStars()
# makeMap("1:30PM","05/08/2002","33-52-11.44S","151-12-29.82E")

       
