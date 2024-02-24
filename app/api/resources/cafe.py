import sqlalchemy
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource
from sqlalchemy.exc import IntegrityError

from app.api.marshmallow.schemas import cafe_schema
from app.database import db
from app.api import cafe_namespace
from app.api.models import cafe_model
from app.api.resources.orm_models import CafeModel


@cafe_namespace.route('/')
class CafeList(Resource):
    @cafe_namespace.doc(security='jwt')
    @jwt_required()
    @cafe_namespace.marshal_list_with(cafe_model)
    def get(self):
        """Получение данных о кафе"""
        cafes = CafeModel.query.all()
        return cafes

    @cafe_namespace.doc(security='jwt')
    @jwt_required()
    @cafe_namespace.expect(cafe_model)
    @cafe_namespace.marshal_with(cafe_model)
    def post(self):
        """Создание нового кафе"""
        data = request.json
        cafe = CafeModel(**data)
        db.session.add(cafe)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            cafe_namespace.abort(400, "Кафе с таким именем уже существует")
        return cafe_schema.dump(cafe), 201


@cafe_namespace.route('/<int:cafe_id>')
class Cafe(Resource):
    @cafe_namespace.doc('get_cafe')
    @cafe_namespace.marshal_with(cafe_model)
    def get(self, cafe_id):
        """Получение данных о конкретном кафе"""
        cafe = CafeModel.query.get(cafe_id)
        if not cafe:
            cafe_namespace.abort(404, "Кафе не найдено")
        return cafe

    @cafe_namespace.doc(security='jwt')
    @jwt_required()
    @cafe_namespace.marshal_with(cafe_model)
    @cafe_namespace.expect(cafe_model)
    def put(self, cafe_id):
        """Обновление информации о кафе"""
        cafe = CafeModel.query.get(cafe_id)
        if not cafe:
            cafe_namespace.abort(404, "Кафе не найдено")
        data = request.json
        for key, value in data.items():
            setattr(cafe, key, value)
        db.session.commit()
        return cafe

    @cafe_namespace.doc(responses={
        200: 'Успешный DELETE-запрос, ресурс удален',
        401: 'Неавторизованный доступ',
        404: 'Ресурс не найден'
    })
    @cafe_namespace.doc(security='jwt')
    @jwt_required()
    def delete(self, cafe_id):
        """Удаление кафе"""
        cafe = CafeModel.query.get(cafe_id)
        if not cafe:
            cafe_namespace.abort(404, message='Кафе с id {} не найдено'.format(cafe_id))
        try:
            db.session.delete(cafe)
            db.session.commit()
            return {'msg': 'Кафе удалено'}, 200
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return {'msg': 'Ошибка. У кафе есть связанные объекты'}, 200
