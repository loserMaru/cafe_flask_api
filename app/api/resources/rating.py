from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, NotFound
from app import db

from app.api import rating_namespace
from app.api.marshmallow.schemas import rating_schema
from app.api.models import rating_model
from app.api.resources.orm_models import RatingModel


@rating_namespace.route('/')
class RatingList(Resource):
    @rating_namespace.doc(security='jwt')
    @jwt_required()
    @rating_namespace.marshal_list_with(rating_model)
    def get(self):
        """Получение рейтинга по JWT токену"""
        user_id = get_jwt_identity().get('id')
        rating = RatingModel.query.filter_by(user_id=user_id).all()
        return rating, 200

    @rating_namespace.doc(security='jwt')
    @jwt_required()
    @rating_namespace.marshal_list_with(rating_model)
    @rating_namespace.expect(rating_model)
    def post(self):
        """Создание рейтинга"""
        data = request.json
        current_user = get_jwt_identity()
        user_id = current_user.get('id')

        existing_rating = RatingModel.query.filter_by(user_id=user_id, cafe_id=data.get('cafe_id')).first()
        if existing_rating:
            existing_rating.rating = data.get('rating')  # Обновляем оценку
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                rating_namespace.abort(400, "Что-то пошло не так при обновлении рейтинга")
            return existing_rating

        rating = RatingModel(user_id=user_id, **data)
        try:
            db.session.add(rating)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            rating_namespace.abort(400, "Что-то пошло не так при создании рейтинга")
        return rating


@rating_namespace.route('/<int:id>')
class Rating(Resource):
    @rating_namespace.doc(security='jwt')
    @jwt_required()
    @rating_namespace.marshal_list_with(rating_model)
    def delete(self, id):
        """Удаление рейтинга"""
        rating = RatingModel.query.filter_by(id=id).first()
        if not rating:
            raise NotFound("Rating not found.")
        db.session.delete(rating)
        db.session.commit()
        return '', 204
