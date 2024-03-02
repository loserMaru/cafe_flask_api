from flask import request
from flask_restx import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database import db
from app.api import favorite_namespace
from app.api.models import favorite_model
from app.api.marshmallow.schemas import favorite_schema
from app.api.resources.orm_models import FavoriteModel


@favorite_namespace.route('/')
class FavoriteList(Resource):
    @favorite_namespace.doc(security='jwt')
    @jwt_required()
    @favorite_namespace.marshal_list_with(favorite_model)
    def get(self):
        """Get list of favorite cafes"""
        user_id = get_jwt_identity().get('id')
        favorites = FavoriteModel.query.filter_by(user_id=user_id).all()
        return favorites, 200

    @favorite_namespace.doc(security='jwt')
    @jwt_required()
    @favorite_namespace.expect(favorite_model)
    def post(self):
        """Create new favorite cafe"""
        data = request.json
        user_id = get_jwt_identity().get('id')
        cafe_id = data.get('cafe_id')

        # Проверяем, существует ли уже запись об избранном ресторане для данного пользователя
        existing_favorite = FavoriteModel.query.filter_by(user_id=user_id, cafe_id=cafe_id).first()

        if existing_favorite:
            # Если запись уже существует, возвращаем ошибку
            return {'msg': 'Ресторан уже в избранном'}, 400

        # Создаем новую запись об избранном ресторане
        favorite = FavoriteModel(user_id=user_id, cafe_id=cafe_id)

        try:
            db.session.add(favorite)
            db.session.commit()
            return favorite_schema.dump(favorite), 201
        except IntegrityError as e:
            db.session.rollback()
            return {'msg': 'Ошибка сохранения в базу данных. Неверные внешние ключи'}, 400


@favorite_namespace.route('/<int:favorite_id>')
class Favorite(Resource):
    @favorite_namespace.doc(security='jwt')
    @jwt_required()
    @favorite_namespace.marshal_with(favorite_model)
    def get(self, id):
        """Get favorite cafe by id"""
        favorite = FavoriteModel.query.get(id)
        if not favorite:
            favorite_namespace.abort(404, 'Избранное не найдено')
        return favorite, 200

    @favorite_namespace.doc(security='jwt')
    @jwt_required()
    @favorite_namespace.expect(favorite_model)
    def put(self, id):
        """Edit favorite cafe by id"""
        favorite = FavoriteModel.query.filter_by(id=id).first()
        if not favorite:
            favorite_namespace.abort(404, 'Избранное не найдено')
        favorite.user_id = favorite_namespace.payload['user_id']
        favorite.cafe_id = favorite_namespace.payload['cafe_id']
        try:
            db.session.commit()
            return favorite_schema.dump(favorite), 200
        except IntegrityError as e:
            db.session.rollback()
            return {'msg': 'Ошибка сохранения в базу данных. Неверные внешние ключи'}, 400

    @favorite_namespace.doc(security='jwt')
    @jwt_required()
    def delete(self, id):
        """Delete favorite cafe by cafe_id"""
        current_user_id = get_jwt_identity().get('id')

        # Поиск избранного по cafe_id и user_id
        favorite = FavoriteModel.query.filter_by(cafe_id=id, user_id=current_user_id).first()

        if not favorite:
            favorite_namespace.abort(404, 'Избранное не найдено')

        # Проверка, что пользователь удаляет свой собственный ресурс
        if favorite.user_id != current_user_id:
            favorite_namespace.abort(403, 'Доступ запрещен')

        db.session.delete(favorite)
        db.session.commit()

        return {'msg': 'Удален из избранного'}, 200
