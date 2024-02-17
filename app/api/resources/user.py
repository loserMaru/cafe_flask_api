from flask import request
from flask_restx import Resource, Namespace, fields

from app.api.resources.models import UserModel
from app.database import db

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.Integer(description='The user identifier'),
    'email': fields.String(description='The user email'),
    'password': fields.String(description='The user password'),
    'role': fields.String(description='The user role')
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    def get(self):
        """Список всех пользователей"""
        users = UserModel.query.all()
        return [user.serialize() for user in users]

    @api.doc('create_user')
    @api.expect(user_model)
    def post(self):
        """Создание нового пользователя"""
        data = request.json
        user = UserModel(**data)
        db.add(user)
        db.commit()
        return user.serialize(), 201


@api.route('/<int:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class User(Resource):
    @api.doc('get_user')
    def get(self, user_id):
        """Получить информацию о пользователе"""
        user = UserModel.query.get(user_id)
        if not user:
            api.abort(404, "User not found")
        return user.serialize()

    @api.doc('update_user')
    @api.expect(user_model)
    def put(self, user_id):
        """Обновить информацию о пользователе"""
        user = UserModel.query.get(user_id)
        if not user:
            api.abort(404, "User not found")
        data = request.json
        for key, value in data.items():
            setattr(user, key, value)
        db.commit()
        return user.serialize()

    @api.doc('delete_user')
    def delete(self, user_id):
        """Удалить пользователя"""
        user = UserModel.query.get(user_id)
        if not user:
            api.abort(404, "User not found")
        db.delete(user)
        db.commit()
        return '', 204
