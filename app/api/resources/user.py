from flask_restx import Resource
from app.api import api_namespace


@api_namespace.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
