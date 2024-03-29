import sqlalchemy
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource
from sqlalchemy.exc import IntegrityError

from app.api import coffee_namespace
from app.api.marshmallow.schemas import coffee_schema
from app.api.models import coffee_model
from app.api.resources.orm_models import CoffeeModel
from app.database import db


@coffee_namespace.route('/')
class CoffeeList(Resource):
    @coffee_namespace.doc(security='jwt')
    @jwt_required()
    @coffee_namespace.marshal_list_with(coffee_model)
    def get(self):
        """Получение данных о кофе"""
        coffees = CoffeeModel.query.all()
        return coffees

    @coffee_namespace.doc('create_coffee')
    @coffee_namespace.expect(coffee_model)
    @coffee_namespace.marshal_with(coffee_model)
    def post(self):
        """Создание нового вида кофе"""
        data = request.json
        coffee = CoffeeModel(**data)
        db.session.add(coffee)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            coffee_namespace.abort(400, "Ошибка. Такой вид кофе уже существует")
        return coffee_schema.dump(coffee), 201


@coffee_namespace.route('/<int:coffee_id>')
class Coffee(Resource):
    @coffee_namespace.doc(security='jwt')
    @jwt_required()
    @coffee_namespace.marshal_with(coffee_model)
    def get(self, coffee_id):
        """Получение данных о конкретном виде кофе"""
        coffee = CoffeeModel.query.get(coffee_id)
        if not coffee:
            coffee_namespace.abort(404, "Вид кофе не найден")
        return coffee

    @coffee_namespace.doc(security='jwt')
    @jwt_required()
    @coffee_namespace.marshal_with(coffee_model)
    @coffee_namespace.expect(coffee_model)
    def put(self, coffee_id):
        """Обновление информации о виде кофе"""
        coffee = CoffeeModel.query.get(coffee_id)
        if not coffee:
            coffee_namespace.abort(404, "Вид кофе не найден")
        data = request.json
        for key, value in data.items():
            setattr(coffee, key, value)
        db.session.commit()
        return coffee

    @coffee_namespace.doc(responses={
        200: 'Успешный DELETE-запрос, ресурс удален',
        401: 'Неавторизованный доступ',
        404: 'Ресурс не найден'
    })
    @coffee_namespace.doc(security='jwt')
    @jwt_required()
    def delete(self, coffee_id):
        """Удаление вида кофе"""
        coffee = CoffeeModel.query.get(coffee_id)
        if not coffee:
            coffee_namespace.abort(404, message='Вид кофе с id {} не найден'.format(coffee_id))
        try:
            db.session.delete(coffee)
            db.session.commit()
            return {'msg': 'Вид кофе удален'}, 200
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return {'msg': 'Ошибка. У вида кофе есть связанные объекты'}, 200
