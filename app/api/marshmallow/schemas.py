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
