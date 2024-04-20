import sqlalchemy
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
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
    @user_namespace.doc(security='jwt')
    @jwt_required()
    @user_namespace.marshal_list_with(user_model)
    def get(self):
        """Получение данных о пользователе"""
        current_user_id = get_jwt_identity()
        user_id = current_user_id['id']  # Extract the id value from the dictionary
        users = UserModel.query.filter_by(id=user_id).all()
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
            user_namespace.abort(400, "Аккаунт с таким email уже зарегистрирован")
        return user_schema.dump(user), 201


@user_namespace.route('/<int:user_id>')
class User(Resource):
    @user_namespace.doc(security='jwt')
    @user_namespace.marshal_with(user_model)
    @user_namespace.expect(user_post_model)
    def put(self, user_id):
        """Обновить информацию о пользователе"""
        user = UserModel.query.get(user_id)
        if not user:
            user_namespace.abort(404, "User not found")
        data = request.json
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    @user_namespace.doc(responses={
        200: 'Успешный DELETE-запрос, ресурс удален',
        401: 'Неавторизованный доступ',
        404: 'Ресурс не найден'
    })
    @user_namespace.doc(security='jwt')
    @jwt_required()
    def delete(self, user_id):
        """Delete user account"""
        user = UserModel.query.get(user_id)
        if not user:
            user_namespace.abort(404, message='Пользователь с id {} не найден'.format(user_id))
        try:
            db.session.delete(user)
            db.session.commit()
            return {'msg': 'Пользователь удален'}, 200
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return {'msg': 'Ошибка. У пользователя есть внешние ключи'}, 200

