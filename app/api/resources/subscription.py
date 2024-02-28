import datetime

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource
from sqlalchemy.exc import IntegrityError

from app.api import subscription_namespace
from app.api.models import subscription_model
from app.api.resources.orm_models import SubscriptionModel
from app.database import db


@subscription_namespace.route('/')
class SubscriptionList(Resource):
    @subscription_namespace.doc(security='jwt')
    @jwt_required()
    @subscription_namespace.marshal_with(subscription_model)
    def get(self):
        """Получение данных о подписке"""
        current_user_id = get_jwt_identity()
        user_id = current_user_id['id']  # Extract the id value from the dictionary
        subscriptions = SubscriptionModel.query.filter_by(user_id=user_id).all()
        return subscriptions

    @subscription_namespace.doc(security='jwt')
    @jwt_required()
    @subscription_namespace.expect(subscription_model)
    @subscription_namespace.marshal_with(subscription_model)
    def post(self):
        """Создание подписки"""
        data = request.json
        current_user = get_jwt_identity()
        user_id = current_user.get('id')

        start_date = datetime.date.today()
        data['start_date'] = start_date

        end_date = start_date + datetime.timedelta(days=30)
        end_date = end_date.replace(day=start_date.day)
        data['end_date'] = end_date

        subscription = SubscriptionModel(user_id=user_id, **data)
        try:
            db.session.add(subscription)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            subscription_namespace.abort(400, "Something wrong")
        return subscription
