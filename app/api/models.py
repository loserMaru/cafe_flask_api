from flask_restx import fields
from app.api import api_namespace, user_namespace, login_namespace

login_model = login_namespace.model('Login', {
    'email': fields.String(default='user@example.com', required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password', mask=True)
})

user_model = user_namespace.model('User', {
    'id': fields.Integer(readonly=True, description='The user identifier'),
    'email': fields.String(required=True, default='user@example.com', description='The user email'),
    'role': fields.String(default='user', description='The user role')
})

user_post_model = user_namespace.model('User', {
    'id': fields.Integer(readonly=True),
    'email': fields.String(default='user@example.com', required=True),
    'password': fields.String(required=True, mask=True),
    'confirm_password': fields.String(required=True, mask=True),
    'role': fields.String(default='user'),
})

cafe_model = api_namespace.model('Cafe', {
    'id': fields.Integer(readonly=True, description='The cafe identifier'),
    'name': fields.String(required=True, description='The cafe name'),
    'address': fields.String(required=True, description='The cafe address'),
    'description': fields.String(required=True, description='The cafe description')
})

coffee_model = api_namespace.model('Coffee', {
    'id': fields.Integer(readonly=True, description='The coffee identifier'),
    'name': fields.String(description='The coffee name'),
    'description': fields.String(description='The coffee description'),
    'cafe_id': fields.Integer(description='The ID of the cafe')
})

order_model = api_namespace.model('Order', {
    'id': fields.Integer(description='The order identifier'),
    'status': fields.String(description='The order status'),
    'total_price': fields.Float(description='The order total price'),
    'cafe_id': fields.Integer(description='The ID of the cafe'),
    'coffee_id': fields.Integer(description='The ID of the coffee'),
    'user_id': fields.Integer(description='The ID of the user')
})

favorite_model = api_namespace.model('Favorite', {
    'id': fields.Integer(description='The favorite identifier'),
    'cafe_id': fields.Integer(description='The ID of the cafe'),
    'user_id': fields.Integer(description='The ID of the user')
})

rating_model = api_namespace.model('Rating', {
    'id': fields.Integer(description='The rating identifier'),
    'rating': fields.Float(description='The rating value'),
    'cafe_id': fields.Integer(description='The ID of the cafe'),
    'user_id': fields.Integer(description='The ID of the user')
})
