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
#run server if we run the webservice directly 
# if __name__ == '__main__':
    with Configurator() as config:
        config.set_request_factory(request_factory)
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
     #route for getting star data and generating map
        config.add_route('/getStarData', '/getStarData')
        config.add_view(getStarDataRoute, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    # createDatabase()
    # parseCSVStars()
    # addPlanets()
    print("serving")
    makeMap("1:30PM","05/08/2002","33-52-11.44S","151-12-29.82E")
    server.serve_forever()
       
