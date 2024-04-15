from pyramid.config import Configurator
from pyramid.response import Response
from dbHandler import *
from pyHandler import *
def getStarDataRoute(request):
    #get params from request
    lat = request.params['lat']
    lon = request.params['lon']
    date = request.params['date']
    time = request.params['time']
    bufToReturn = makeMap(time,date,lat,lon)
    return Response(bufToReturn)
    