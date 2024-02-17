from flask import Flask
from flask_restx import Api

from app.api.resources.user import UserList, User
from app.database import db

# Инициализация расширения Flask-RESTX
api = Api(version='1.0', title='Cafe Flask Api', description='Swagger documentation for cafe app',
          doc='/docs/', authorizations=
          {'jwt': {
              'type': 'apiKey',
              'in': 'header',
              'name': 'Authorization',
              'description': 'JWT authorization, e.g. "token"'
          }
          })


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    api.init_app(app)

    # Регистрация ресурсов API
    api.add_resource(UserList, '/users')
    api.add_resource(User, '/users/<int:user_id>')

    return app
