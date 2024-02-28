from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from dbHandler import *
from pyHandler import *

def hello_world(request):
    return Response('Hello World!')

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        config.add_route('getStarData', '/getStarData')
        config.add_view(makeMap, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('127.0.0.1', 6543, app)
    server.serve_forever()
