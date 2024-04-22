from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from dbHandler import *
from pyHandler import *
from serverRoutes import *

def hello_world(request):
    return Response('Hello World!')
#run server if we run the webservice directly 
if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
     #route for getting star data and generating map
        config.add_route('getStarData', '/getStarData')
        config.add_view(getStarDataRoute, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('127.0.0.1', 6543, app)
    # createDatabase()
    # parseCSVStars()
    # addPlanets()
    print("serving")
    makeMap("1:30PM","05/08/2002","33-52-11.44S","151-12-29.82E")
    server.serve_forever()
       
