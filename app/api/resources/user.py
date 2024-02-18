from flask import request
from flask_restx import Resource
from sqlalchemy.exc import IntegrityError

from app.api import user_namespace
from app.api.marshmallow.schemas import user_schema
from app.api.resources.orm_models import UserModel
from app.api.models import user_model, user_post_model
from app.database import db
from app.utils.password_utils import hash_password


@user_namespace.route('/')
class UserList(Resource):
    @user_namespace.doc('list_users')
    @user_namespace.marshal_list_with(user_model)
    def get(self):
        """Список всех пользователей"""
        users = UserModel.query.all()
        return users

    @user_namespace.doc('create_user')
    @user_namespace.expect(user_post_model)
    @user_namespace.marshal_with(user_model)
    def post(self):
        """Создание нового пользователя"""
        data = request.json
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            user_namespace.abort(400, "Passwords do not match")

        hashed_password = hash_password(password)
        data['password'] = hashed_password

        data.pop('confirm_password', None)

        user = UserModel(**data)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            user_namespace.abort(400, "Email already registered")
        return user_schema.dump(user), 201


@user_namespace.route('/<int:user_id>')
@user_namespace.param('user_id', 'The user identifier')
@user_namespace.response(404, 'User not found')
class User(Resource):
    @user_namespace.doc('get_user')
    @user_namespace.marshal_with(user_model)
    def get(self, user_id):
        """Получить информацию о пользователе"""
        user = UserModel.query.get(user_id)
        if not user:
            user_namespace.abort(404, "User not found")
        return user, 200

    @user_namespace.doc('update_user')
    @user_namespace.marshal_with(user_model)
    def put(self, user_id):
        """Обновить информацию о пользователе"""
        user = UserModel.query.get(user_id)
        if not user:
            user_namespace.abort(404, "User not found")
        data = request.json
        for key, value in data.items():
            setattr(user, key, value)
        db.commit()
        return user.serialize()

    @user_namespace.doc('delete_user')
    @user_namespace.marshal_with(user_model)
    def delete(self, user_id):
        """Удалить пользователя"""
        user = UserModel.query.get(user_id)
        if not user:
            user_namespace.abort(404, "User not found")
        db.delete(user)
        db.commit()
        return '', 204
