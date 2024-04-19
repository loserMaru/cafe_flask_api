import sqlalchemy

from flask import request
from sqlalchemy import and_
from flask_restx import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database import db

from app.api import order_namespace
from app.api.models import order_model, order_put_model
from app.utils.time_utils import get_current_time
from app.api.marshmallow.schemas import order_schema
from app.api.resources.orm_models import OrderModel, CoffeeModel, CafeModel, SubscriptionModel


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
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    def post(self):
        """Создание нового заказа"""
        data = request.json
        current_user = get_jwt_identity()
        user_id = current_user.get('id')
        coffee_data = data.pop('coffee', None)  # Извлекаем данные о кофе из запроса

        # Получаем текущее время в часовом поясе UTC+3
        current_time = get_current_time()

        order = OrderModel(user_id=user_id, time_order_made=current_time, **data)  # Вставляем user_id из JWT токена

        user_subscription = SubscriptionModel.query.filter_by(user_id=user_id).first()
        if not user_subscription or user_subscription.quantity == 0:
            order_namespace.abort(400, "Ошибка. Вы не можете совершать заказы. Пожалуйста, продлите подписку.")
            return

        cafe = CafeModel.query.get(data['cafe_id'])
        if not cafe:
            order_namespace.abort(404, "Кафе с указанным идентификатором не найдено")
            return

        if coffee_data:  # Если есть данные о кофе
            if data['cafe_id'] != coffee_data['cafe_id']:
                order_namespace.abort(400, "Ошибка. В данном кафе такого кофе не существует")
                return

            # Проверяем существование кофе в базе данных по названию и идентификатору кафе
            existing_coffee = CoffeeModel.query.filter(
                and_(CoffeeModel.name == coffee_data['name'], CoffeeModel.cafe_id == coffee_data['cafe_id'])).first()

            if existing_coffee:  # Если кофе уже существует
                coffee = existing_coffee
            else:  # Если кофе не существует
                order_namespace.abort(404, "Кофе с указанным названием и идентификатором кафе не найден")
                return  # Досрочный выход из функции, чтобы избежать создания заказа

            try:
                db.session.commit()  # Фиксируем изменения, чтобы получить ID кофе
            except IntegrityError:
                db.session.rollback()
                order_namespace.abort(400, "Ошибка. Невозможно создать заказ")

            order.coffee_id = coffee.id  # Привязываем кофе к заказу

        db.session.add(order)  # Добавляем заказ в сессию БД
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            order_namespace.abort(400, "Ошибка. Невозможно создать заказ")

        user_subscription.quantity -= 1

        try:
            db.session.commit()  # Сохраняем изменения в подписке пользователя
        except IntegrityError:
            db.session.rollback()
            order_namespace.abort(500, "Ошибка при обновлении подписки пользователя")

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
    @order_namespace.expect(order_put_model)
    @order_namespace.marshal_with(order_model)
    def put(self, order_id):
        """Обновление информации о заказе"""
        order = OrderModel.query.get(order_id)
        if not order:
            order_namespace.abort(404, "Вид кофе не найден")
        data = request.json
        for key, value in data.items():
            setattr(order, key, value)
        db.session.commit()
        return order_schema.dump(order)


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
