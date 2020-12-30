import sqlite3
from utils.database import db
from flask import Blueprint, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from .validators import *
from utils.response import json_response
from services.auth import (
    AuthService,
    UserNotFound,
    InvalidCredentials,
    EmailAlreadyExist
)


bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    auth_service = AuthService()

    if not data['email'] or not data['password']:
        return json_response.bad_request({'error_msg': 'Не заполнено поле Email или Пароль!'})
    
    if not check_validate_email(data['email']):
        return json_response.bad_request({'error_msg': 'Неверный формат Email!'})

    try:
        auth_service.login(data['email'], data['password'])
    except (UserNotFound, InvalidCredentials) as e:
        return json_response.unauthorized()
    return json_response.success()

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    auth_service = AuthService()
    
    if not data['first_name'] or not data['last_name'] or not data['email'] or not data['password']:
        return json_response.bad_request({'error_msg': 'Не заполнено одно из полей!'})

    if not check_validate_email(data['email']):
        return json_response.bad_request({'error_msg': 'Неверный формат Email!'})

    if not check_validate_password(data['password']):
        return json_response.bad_request({'error_msg': 'Неверная длина пароля! Длина пароля должна быть от 5 до 100 символов.'})

    try:
        user = auth_service.register(data)
    except EmailAlreadyExist:
        return json_response.conflict()
    return json_response.success(user)


@bp.route('/logout', methods=['GET'])
def logout():
    auth_service = AuthService()
    auth_service.logout()
    return json_response.success()