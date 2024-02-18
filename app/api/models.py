from flask_restx import fields
from app.api import api_namespace, user_namespace, login_namespace

login_model = login_namespace.model('Login', {
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password', mask=True)
})

user_model = user_namespace.model('User', {
    'id': fields.Integer(readonly=True, description='The user identifier'),
    'email': fields.String(required=True, default='user@example.com', description='The user email'),
    'role': fields.String(default='user', description='The user role')
})

user_post_model = user_namespace.model('User', {
    'id': fields.Integer(readonly=True),
    'email': fields.String(default='string@gmail.com', required=True),
    'password': fields.String(required=True, mask=True),
    'confirm_password': fields.String(required=True, mask=True),
    'role': fields.String(default='user'),
})

cafe_model = api_namespace.model('Cafe', {
    'id': fields.Integer(description='The cafe identifier'),
    'name': fields.String(description='The cafe name'),
    'address': fields.String(description='The cafe address'),
    'description': fields.String(description='The cafe description')
})

coffee_model = api_namespace.model('Coffee', {
    'id': fields.Integer(description='The coffee identifier'),
    'name': fields.String(description='The coffee name'),
    'description': fields.String(description='The coffee description'),
    'location': fields.String(description='The coffee location')
})

drinks_model = api_namespace.model('Drinks', {
    'id': fields.Integer(description='The drinks identifier'),
    'name': fields.String(description='The drinks name'),
    'description': fields.String(description='The drinks description'),
    'cafe_id': fields.Integer(description='The ID of the cafe')
})

dessert_model = api_namespace.model('Dessert', {
    'id': fields.Integer(description='The dessert identifier'),
    'products': fields.String(description='The dessert products')
})

weight_model = api_namespace.model('Weight', {
    'id': fields.Integer(description='The weight identifier'),
    'weight': fields.String(description='The weight value'),
    'price': fields.Integer(description='The weight price'),
    'coffee_id': fields.Integer(description='The ID of the coffee'),
    'drinks_id': fields.Integer(description='The ID of the drink')
})

order_model = api_namespace.model('Order', {
    'id': fields.Integer(description='The order identifier'),
    'status': fields.String(description='The order status'),
    'total_price': fields.Float(description='The order total price'),
    'count': fields.Integer(description='The order count'),
    'drink_type': fields.String(description='The order drink type'),
    'cafe_id': fields.Integer(description='The ID of the cafe'),
    'drinks_id': fields.Integer(description='The ID of the drink'),
    'coffee_id': fields.Integer(description='The ID of the coffee'),
    'weight_id': fields.Integer(description='The ID of the weight')
})

products_model = api_namespace.model('Products', {
    'id': fields.Integer(description='The products identifier'),
    'cafe_id': fields.Integer(description='The ID of the cafe'),
    'drinks_id': fields.Integer(description='The ID of the drink'),
    'coffee_id': fields.Integer(description='The ID of the coffee'),
    'dessert_id': fields.Integer(description='The ID of the dessert')
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