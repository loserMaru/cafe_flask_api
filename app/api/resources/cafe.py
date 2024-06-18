import os

import sqlalchemy
from flask import request
from flask_restx import Resource
from imgurpython import ImgurClient
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.marshmallow.schemas import cafe_schema, cafe_key_schema
from app.database import db
from app.api import cafe_namespace
from app.api.models import cafe_model, cafe_key_model
from app.api.resources.orm_models import CafeModel


@cafe_namespace.route('/')
class CafeList(Resource):
    @cafe_namespace.expect(cafe_namespace.parser().add_argument('Name', type=str, help='Filter by name'))
    @cafe_namespace.doc(security='jwt')
    @jwt_required()
    @cafe_namespace.marshal_list_with(cafe_model)
    def get(self):
        """Получение данных о кафе"""
        filter_by_name = request.args.get('Name')
        cafes = CafeModel.query

        if filter_by_name:
            cafes = cafes.filter(CafeModel.name.ilike(f'%{filter_by_name}%'))

        cafes = cafes.all()

        # Обновление среднего рейтинга для каждого ресторана
        for cafe in cafes:
            cafe.star = cafe.calculate_average_rating()

        db.session.commit()  # Сохранение изменений в базе данных

        # Преобразование объектов в словари и возврат списка ресторанов
        cafe_data = [cafe.to_dict() for cafe in cafes]
        return cafe_data, 200

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


@cafe_namespace.route('/<int:cafe_id>/pic')
class UploadCafePic(Resource):
    @cafe_namespace.doc(security='jwt')
    @cafe_namespace.expect(cafe_namespace.parser().add_argument('image', location='files', type='file'))
    def put(self, cafe_id):
        """Give picture for profile by his ID"""
        cafe = CafeModel.query.filter_by(id=cafe_id).first()
        if not cafe:
            cafe_namespace.abort(404, 'Профиль не найден')

        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")

        client = ImgurClient(client_id, client_secret)

        image = request.files.get('image')
        if not image:
            return {'message': 'No image uploaded'}, 400

        # Save the image to a temporary directory
        temp_dir = os.path.join(os.getcwd(), 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        image_path = os.path.join(temp_dir, image.filename)
        image.save(image_path)

        # Upload the image to imgur
        response = client.upload_from_path(image_path)

        # Remove the temporary file
        os.remove(image_path)

        # Update profile picture
        cafe.image = response['link']
        db.session.commit()

        return cafe_schema.dump(cafe), 201


@cafe_namespace.route('/cafe_key')
class CafeKey(Resource):
    @cafe_namespace.doc(security='jwt')
    @jwt_required()
    @cafe_namespace.expect(cafe_key_model)
    def post(self):
        """Добавление нового ключа"""
        role = get_jwt_identity().get('role')
        cafe_id = get_jwt_identity().get('cafe_id')
        data = request.json

        if role != 'admin':
            cafe_namespace.abort(403, "У вас нет прав для выполнения данного действия")

        if not cafe_id:
            cafe_namespace.abort(403, "У вас нет прав для выполнения данного действия")

        new_cafe_key = data.get('cafe_key')

        cafe = CafeModel.query.get(cafe_id)
        if not cafe:
            cafe_namespace.abort(404, "Кафе не найдено")

        cafe.cafe_key = new_cafe_key

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return {'msg': 'Ошибка'}, 200

        return cafe_key_schema.dump(cafe), 201


@cafe_namespace.route('/<int:cafe_id>/pic/upload')
class UploadLocalCafePic(Resource):
    @cafe_namespace.doc(security='jwt')
    @jwt_required()
    @cafe_namespace.expect(cafe_namespace.parser().add_argument('image', location='files', type='file'))
    def put(self, cafe_id):
        """Upload picture for profile by its ID"""
        cafe = CafeModel.query.filter_by(id=cafe_id).first()
        if not cafe:
            cafe_namespace.abort(404, 'Профиль не найден')

        image = request.files.get('image')
        if not image:
            return {'message': 'No image uploaded'}, 400

        # Save the image to a directory in the project
        upload_folder = os.path.join(os.getcwd(), 'uploaded_images')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        image_path = os.path.join(upload_folder, image.filename)
        image.save(image_path)

        # Update profile picture path
        cafe.image = image_path
        db.session.commit()

        return cafe_schema.dump(cafe), 200
