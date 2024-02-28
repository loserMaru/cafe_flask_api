from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    email = fields.String()
    password = fields.String()
    role = fields.String()


user_schema = UserSchema()


class CafeSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    address = fields.String()
    description = fields.String()


cafe_schema = CafeSchema()


class CoffeeSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    cafe_id = fields.Integer()


coffee_schema = CoffeeSchema()


class OrderSchema(Schema):
    id = fields.Integer()
    status = fields.String()
    total_price = fields.Float()
    cafe_id = fields.Integer()
    coffee_id = fields.Integer()
    user_id = fields.Integer()


order_schema = OrderSchema()


class SubscriptionSchema(Schema):
    id = fields.Integer()
    start_date = fields.Date()
    end_date = fields.Date()
    quantity = fields.Integer()
    user_id = fields.Integer()


subscription_schema = SubscriptionSchema()
