from flask import Flask, jsonify
from flask_jwt_extended.exceptions import NoAuthorizationError

from app.api import api
from app.utils import jwt
from app.database import db
from app.api.resources.cafe import CafeList, Cafe
from app.api.resources.user import UserList, User
from app.api.resources.order import OrderList, Order
from app.api.resources.coffee import CoffeeList, Coffee
from app.api.resources.login import UserLogin, RefreshToken


# Инициализация расширения Flask-RESTX

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)

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

    # Регистрация ресурсов API для заказов
    api.add_resource(OrderList, '/orders')
    api.add_resource(Order, '/orders/<int:order_id>')

    @app.errorhandler(NoAuthorizationError)
    def handle_missing_authorization_header_error(error):
        return jsonify({'message': 'Вы не авторизованы'}), 401
    return app


app = create_app()
