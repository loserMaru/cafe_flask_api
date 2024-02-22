from flask import Flask

from app.api import api
from app.api.resources.login import UserLogin, RefreshToken
from app.api.resources.user import UserList, User
from app.database import db
from app.utils import jwt


# Инициализация расширения Flask-RESTX

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    api.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Регистрация ресурсов API
    api.add_resource(UserLogin, '/login')
    api.add_resource(RefreshToken, '/refresh')

    # Регистрация ресурсов API
    api.add_resource(UserList, '/users')
    api.add_resource(User, '/users/<int:user_id>')

    return app
