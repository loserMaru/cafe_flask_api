from flask import Flask
from flask_restx import Api
from app.api.resources.user import HelloWorld as UserResource


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # Инициализация расширения Flask-RESTX
    api = Api(app, version='1.0', title='Cafe Flask Api', description='Swagger documentation for cafe app',
              doc='/docs/')

    # Регистрация ресурсов API
    api.add_resource(UserResource, '/hello')

    return app
