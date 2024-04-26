from flask_restx import fields
from app.api import api_namespace, user_namespace, login_namespace
from app.utils.time_utils import get_current_time

login_model = login_namespace.model('Login', {
    'email': fields.String(default='user@example.com', required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password', mask=True)
})

user_model = user_namespace.model('User', {
    'id': fields.Integer(readonly=True, description='The user identifier'),
    'email': fields.String(required=True, default='user@example.com', description='The user email'),
    'role': fields.String(default='user', description='The user role'),
    'cafe_id': fields.Integer(required=False, description='The cafe identifier')
})

user_post_model = user_namespace.model('UserPost', {
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
    'description': fields.String(required=True, description='The cafe description'),
    'image': fields.String(required=False, description='Cafe image'),
    'star': fields.Float(required=False, description="Cafe's rating"),
    'cafe_key': fields.String(readonly=True, description='Cafe key')
})

cafe_key_model = api_namespace.model('CafeKey', {
    'cafe_key': fields.String(description='The cafe key')
})

coffee_model = api_namespace.model('Coffee', {
    'id': fields.Integer(readonly=True, description='The coffee identifier'),
    'name': fields.String(description='The coffee name'),
    'description': fields.String(description='The coffee description'),
    'image': fields.String(required=False, description='Coffee image'),
    'cafe': fields.Nested(api_namespace.model('CafeCoffee', {
        'id': fields.Integer(readonly=True, description='The cafe identifier'),
        'name': fields.String(description='The cafe name'),
        'address': fields.String(readonly=True, description='The cafe address'),
        'description': fields.String(readonly=True, description='The cafe description')
    }))
})

order_model = api_namespace.model('Order', {
    'id': fields.Integer(readonly=True, description='The order identifier'),
    'status': fields.String(readonly=True, description='The order status', default='waiting'),
    'name': fields.String(description='The client name', default='Ivan Ivanov'),
    'cafe': fields.Nested(api_namespace.model('CafeOrder', {
        'id': fields.Integer(readonly=True, description='The cafe identifier'),
        'name': fields.String(description='The cafe name'),
        'address': fields.String(readonly=True, description='The cafe address'),
        'description': fields.String(readonly=True, description='The cafe description')
    })),
    'coffee': fields.Nested(api_namespace.model('CoffeeOrder', {
        'id': fields.Integer(readonly=True, description='The coffee identifier'),
        'name': fields.String(description='The coffee name'),
        'description': fields.String(readonly=True, description='The coffee description'),
        'cafe_id': fields.Integer(description='The ID of the cafe'),
        'image': fields.String(readonly=True, description='Coffee image')
    })),
    'pick_up_time': fields.DateTime(required=True, description='The pick up time', default=get_current_time()),
    'user': fields.Nested(api_namespace.model('UserOrder', {
        'id': fields.Integer(readonly=True, description='User identifier'),
        'email': fields.String(readonly=True, description='User email'),
        'smartphone_key': fields.String(description='User key for notifications')
    })),
    'time_order_made': fields.DateTime(readonly=True, description='The order time')
})

order_post_model = api_namespace.model('OrderPost', {
    'id': fields.Integer(readonly=True, description='The order identifier'),
    'status': fields.String(readonly=True, description='The order status', default='waiting'),
    'name': fields.String(description='The client name', default='Ivan Ivanov'),
    'cafe': fields.Nested(api_namespace.model('CafeOrder', {
        'id': fields.Integer(readonly=True, description='The cafe identifier'),
        'name': fields.String(description='The cafe name'),
        'address': fields.String(readonly=True, description='The cafe address'),
        'description': fields.String(readonly=True, description='The cafe description')
    })),
    'coffee': fields.Nested(api_namespace.model('CoffeeOrder', {
        'id': fields.Integer(readonly=True, description='The coffee identifier'),
        'name': fields.String(description='The coffee name'),
        'description': fields.String(readonly=True, description='The coffee description'),
        'cafe_id': fields.Integer(description='The ID of the cafe'),
        'image': fields.String(readonly=True, description='Coffee image')
    })),
    'pick_up_time': fields.DateTime(required=True, description='The pick up time', default=get_current_time()),
    'user_id': fields.Integer(readonly=True, description='User identifier'),
    'smartphone_key': fields.String(description='User phone key for notifications'),
    'time_order_made': fields.DateTime(readonly=True, description='The order time')
})

order_put_model = api_namespace.model('OrderPut', {
    'status': fields.String(description='The order status'),
})

subscription_model = api_namespace.model('Subscription', {
    'id': fields.Integer(readonly=True, description='The subscription identifier'),
    'start_date': fields.Date(readonly=True, description='The subscription start date'),
    'end_date': fields.Date(readonly=True, description='The subscription end date'),
    'quantity': fields.Integer(description='The subscription quantity'),
    'user_id': fields.Integer(readonly=True, description='The ID of the user')
})

favorite_model = api_namespace.model('Favorite', {
    'id': fields.Integer(readonly=True, description='The favorite identifier'),
    'cafe_id': fields.Integer(description='The ID of the cafe'),
    'user_id': fields.Integer(readonly=True, description='The ID of the user')
})

rating_model = api_namespace.model('Rating', {
    'id': fields.Integer(readonly=True, description='The rating identifier'),
    'rating': fields.Float(description='The rating value'),
    'cafe_id': fields.Integer(description='The ID of the cafe'),
    'user_id': fields.Integer(readonly=True, description='The ID of the user')
})
