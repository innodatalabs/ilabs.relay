import logging
from ilabs.api.util import standard_response, ilabs_standard
from ilabs.api.routes_builder import RoutesBuilder
from ilabs.api import req
from flask_restful import Api, Resource
from flask import Flask
import json

class Ping(Resource):
    def get(self):
        return { 'ping': 'pong' }


class Relay(Resource):
    @ilabs_standard
    def get(self, ip, path0=None, path1=None, path2=None):
        logging.debug('HackPing GET ip=%s, path0=%s, path1=%s', ip, path0, path1)

        q = f'http://{ip}'
        if path0 is not None:
            q += '/' + path0
        if path1 is not None:
            q += '/' + path1
        if path2 is not None:
            q += '/' + path2

        logging.debug('Relaying as HTTP GET: %s', q)
        response = req.get(q)
        return standard_response(response.data)

"""
Actual API routes
"""
def routes():
    routes = RoutesBuilder()

    return routes.add_resource(Ping,
        '/ping'  #GET
    ).add_resource(Relay,
        '/relay/<string:ip>',  #GET
        '/relay/<string:ip>/<string:path0>',  #GET
        '/relay/<string:ip>/<string:path0>/<string:path1>',  #GET
        '/relay/<string:ip>/<string:path0>/<string:path1>/<string:path2>',  #GET
    )





app = Flask(__name__)
api = Api(app)


api_routes = routes()

api_routes(api)


logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    # run Flask locally
    app.run(port=8088)
