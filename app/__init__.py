from flask import Flask

from app.api import api
from app.utils import jwt
from app.database import db
from app.api.resources.user import UserList, User
from app.api.resources.cafe import CafeList, Cafe
from app.api.resources.coffee import CoffeeList, Coffee
from app.api.resources.login import UserLogin, RefreshToken


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

    # Регистрация ресурсов API для кофе
    api.add_resource(CoffeeList, '/coffee')
    api.add_resource(Coffee, '/coffee/<int:coffee_id>')

    # Регистрация ресурсов API для кафе
    api.add_resource(CafeList, '/cafe')
    api.add_resource(Cafe, '/cafe/<int:cafe_id>')

    return app
