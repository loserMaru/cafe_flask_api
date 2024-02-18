from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    email = fields.String()
    password = fields.String()
    role = fields.String()


user_schema = UserSchema()
