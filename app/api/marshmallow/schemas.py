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
    image = fields.String()
    star = fields.Float()


cafe_schema = CafeSchema()


class CoffeeSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    image = fields.String()
    cafe = fields.Nested(cafe_schema)


coffee_schema = CoffeeSchema()


class CoffeeForOrderSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    image = fields.String()
    cafe_id = fields.Integer()


coffee_for_order_schema = CoffeeForOrderSchema()


class OrderSchema(Schema):
    id = fields.Integer()
    status = fields.String()
    name = fields.String()
    coffee = fields.Nested(coffee_for_order_schema)
    user_id = fields.Integer()
    cafe = fields.Nested(cafe_schema)
    time_order_made = fields.DateTime()
    pick_up_time = fields.DateTime()


order_schema = OrderSchema()


class SubscriptionSchema(Schema):
    id = fields.Integer()
    start_date = fields.Date()
    end_date = fields.Date()
    quantity = fields.Integer()
    user_id = fields.Integer()


subscription_schema = SubscriptionSchema()


class FavoriteSchema(Schema):
    id = fields.Integer()
    cafe_id = fields.Integer()
    user_id = fields.Integer()


favorite_schema = FavoriteSchema()


class RatingSchema(Schema):
    id = fields.Integer()
    rating = fields.Float()
    cafe_id = fields.Integer()
    user_id = fields.Integer()


rating_schema = RatingSchema()
