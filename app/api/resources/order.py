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
        user_cafe_id = current_user.get('cafe_id')  # Предполагается, что в JWT есть информация о cafe_id пользователя
        user_role = current_user.get('role')

        if user_role == 'user' and not user_cafe_id:
            orders = OrderModel.query.filter_by(user_id=current_user.get('id')).all()

        elif user_cafe_id:
            # Если у пользователя есть cafe_id, выводим все заказы с соответствующим cafe_id
            orders = OrderModel.query.filter_by(cafe_id=user_cafe_id).all()

        else:
            # Если у пользователя нет cafe_id, возвращаем ошибку доступа
            order_namespace.abort(403, "Доступ запрещен")

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
        cafe_data = data.pop('cafe', None)  # Извлекаем данные о кафе из запроса

        # Получаем текущее время в часовом поясе UTC+3
        current_time = get_current_time()

        if not cafe_data:
            order_namespace.abort(400, "Данные о кафе не указаны в запросе")
            return

        cafe_name = cafe_data.get('name')  # Извлекаем название кафе из данных о кафе
        if not cafe_name:
            order_namespace.abort(400, "Название кафе не указано в запросе")
            return

        # Находим кафе в базе данных по названию
        cafe = CafeModel.query.filter_by(name=cafe_name).first()
        if not cafe:
            order_namespace.abort(404, "Кафе с указанным названием не найдено")
            return

        cafe_id = cafe.id  # Получаем id кафе из базы данных

        # Проверяем совпадение cafe_id из данных о кофе с реальным id кафе из базы данных
        if cafe_id != coffee_data.get('cafe_id'):
            order_namespace.abort(400, "Ошибка. Кофе с указанным названием не продаётся в данном кафе")
            return

        order_data = {
            'user_id': user_id,
            'time_order_made': current_time,
            'cafe_id': cafe_id,
            **data  # Передаем оставшиеся данные из запроса
        }

        order = OrderModel(**order_data)  # Вставляем user_id из JWT токена

        user_subscription = SubscriptionModel.query.filter_by(user_id=user_id).first()
        if not user_subscription or user_subscription.quantity == 0:
            order_namespace.abort(400, "Ошибка. Вы не можете совершать заказы. Пожалуйста, продлите подписку.")
            return

        if coffee_data:  # Если есть данные о кофе
            # Проверяем существование кофе в базе данных по названию и идентификатору кафе
            existing_coffee = CoffeeModel.query.filter(
                and_(CoffeeModel.name == coffee_data['name'], CoffeeModel.cafe_id == cafe_id)).first()

            if existing_coffee:  # Если кофе уже существует
                coffee = existing_coffee
            else:  # Если кофе не существует
                order_namespace.abort(404, "Кофе с указанным названием и идентификатором кафе не найден")
                return  # Досрочный выход из функции, чтобы избежать создания заказа

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
        current_user = get_jwt_identity()
        user_role = current_user.get('role')
        print(user_role)

        if user_role != 'admin':
            order_namespace.abort(403, "У вас нет прав для выполнения данного действия")

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
