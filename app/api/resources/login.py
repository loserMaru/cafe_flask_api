from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_restx import Resource, fields

from app.api import login_namespace
from app.api.models import login_model
from app.api.resources.orm_models import UserModel
from app.utils.password_utils import check_password


@login_namespace.route('/')
class UserLogin(Resource):
    @login_namespace.doc('user_login')
    @login_namespace.expect(login_model)
    def post(self):
        """Авторизация пользователя"""
        data = request.json
        email = data.get('email')
        password = data.get('password')

        user = UserModel.query.filter_by(email=email).first()
        if not user or not check_password(password, user.password):
            login_namespace.abort(401, "Invalid email or password")

        access_token = create_access_token(identity=user.to_dict())
        refresh_token = create_refresh_token(identity=user.to_dict())

        return {'access_token': access_token, 'refresh_token': refresh_token, 'user': user.to_dict()}, 200


@login_namespace.route('/refresh')
class RefreshToken(Resource):
    @login_namespace.doc('refresh_token')
    @jwt_required(refresh=True)
    def post(self):
        """Обновление access токена"""
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}, 200
