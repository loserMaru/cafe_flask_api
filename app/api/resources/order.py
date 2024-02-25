import sqlalchemy
from flask import request
from flask_restx import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database import db
from app.api import order_namespace
from app.api.models import order_model, order_post_model
from app.api.resources.orm_models import OrderModel
from app.api.marshmallow.schemas import order_schema


@order_namespace.route('/')
class OrderList(Resource):
    @order_namespace.doc(security='jwt')
    @jwt_required()
    @order_namespace.marshal_list_with(order_model)
    def get(self):
        """Получение списка заказов"""
        current_user = get_jwt_identity()  # Получаем информацию о текущем пользователе из JWT
        user_role = current_user.get('role')  # Предполагается, что в JWT есть информация о роли пользователя

        if user_role == 'user':
            # Фильтрация заказов по user_id, чтобы пользователь видел только свои заказы
            user_id = current_user.get('id')
            orders = OrderModel.query.filter_by(user_id=user_id).all()
        elif user_role == 'moderator':
            # Модератор видит все заказы
            orders = OrderModel.query.all()
        else:
            # Другие роли могут обрабатываться по-разному или возвращать ошибку доступа
            return {'message': 'Доступ запрещен'}, 403

        return orders

    @order_namespace.doc(security='jwt')
    @jwt_required()
    @order_namespace.expect(order_post_model)
    @order_namespace.marshal_with(order_model)
    def post(self):
        """Создание нового заказа"""
        data = request.json
        current_user = get_jwt_identity()
        user_id = current_user.get('id')
        order = OrderModel(user_id=user_id, **data)  # Вставляем user_id из JWT токена
        print(order)
        db.session.add(order)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            order_namespace.abort(400, "Ошибка. Невозможно создать заказ")
        return order_schema.dump(order), 201


@order_namespace.route('/<int:order_id>')
class Order(Resource):
    @order_namespace.doc(security='jwt')
    @jwt_required()
    @order_namespace.marshal_with(order_model)
    def get(self, order_id):
        """Получение информации о заказе"""
        order = OrderModel.query.get(order_id)
        if not order:
            order_namespace.abort(404, "Заказ не найден")
        return order

    @order_namespace.doc(security='jwt')
    @jwt_required()
    def delete(self, order_id):
        """Удаление заказа"""
        order = OrderModel.query.get(order_id)
        if not order:
            order_namespace.abort(404, message='Заказ с id {} не найден'.format(order_id))
        try:
            db.session.delete(order)
            db.session.commit()
            return {'msg': 'Заказ удален'}, 200
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return {'msg': 'Ошибка. Невозможно удалить заказ'}, 200
