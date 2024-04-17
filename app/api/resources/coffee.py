import os

import sqlalchemy
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource
from imgurpython import ImgurClient
from sqlalchemy.exc import IntegrityError

from app.api import coffee_namespace
from app.api.marshmallow.schemas import coffee_schema
from app.api.models import coffee_model
from app.api.resources.orm_models import CoffeeModel, CafeModel
from app.database import db


@coffee_namespace.route('/')
class CoffeeList(Resource):
    @coffee_namespace.expect(coffee_namespace.parser().add_argument('Name', type=str, help='Filter by name'))
    @coffee_namespace.doc(security='jwt')
    @jwt_required()
    @coffee_namespace.marshal_list_with(coffee_model)
    def get(self):
        """Получение данных о кофе"""
        filter_by_name = request.args.get('Name')
        coffees = CoffeeModel.query

        if filter_by_name:
            coffees = coffees.filter(CoffeeModel.name.ilike(f'%{filter_by_name}%'))

        coffees = coffees.all()
        return coffees

    @coffee_namespace.doc(security='jwt')
    @jwt_required()
    @coffee_namespace.expect(coffee_model)
    @coffee_namespace.marshal_with(coffee_model)
    def post(self):
        """Создание нового вида кофе"""
        data = request.json
        coffee_name = data.get('name')
        cafe_name = data.get('cafe', {}).get('name')
        data.pop('cafe', None)
        coffee = CoffeeModel(**data)
        # data = data.pop('cafe', None)

        # Проверяем существование кафе с указанным именем в базе данных
        cafe = CafeModel.query.filter_by(name=cafe_name).first()

        if cafe:  # Если кафе найдено
            # Создаем кофе и связываем его с найденным кафе
            coffee = CoffeeModel(name=coffee_name, description=data.get('description'), cafe_id=cafe.id,
                                 image=data.get('image'))
        else:  # Если кафе не найдено
            coffee_namespace.abort(404, "Кафе не найдено")

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


@coffee_namespace.route('/<int:coffee_id>/pic')
class UploadCoffeePic(Resource):
    @coffee_namespace.doc(security='jwt')
    @coffee_namespace.expect(coffee_namespace.parser().add_argument('image', location='files', type='file'))
    def put(self, coffee_id):
        """Give picture for profile by his ID"""
        coffee = CoffeeModel.query.filter_by(id=coffee_id).first()
        if not coffee:
            coffee_namespace.abort(404, 'Профиль не найден')

        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")

        client = ImgurClient(client_id, client_secret)

        image = request.files.get('image')
        print(image)
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
        coffee.image = response['link']
        db.session.commit()

        return coffee_schema.dump(coffee), 201
