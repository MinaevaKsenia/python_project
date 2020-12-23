import sqlite3
from utils.database import db
from flask import Blueprint, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from .validators import *
from utils.response import json_response


bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    request_json = request.json
    email = request_json.get('email')
    password = request_json.get('password')

    if not email or not password:
        return json_response.bad_request({'error_msg': 'Не заполнено поле Email или Пароль!'})
    
    if not check_validate_email(email):
        return json_response.bad_request({'error_msg': 'Неверный формат Email!'})

    connection = db.connection
    cur = connection.execute(
        'SELECT * '
        'FROM users '
        'WHERE email = ?',
        (email, ),
    )
    user = cur.fetchone()

    if user is None:
        return json_response.forbidden({'error_msg': 'Неверный email!'})

    if not check_password_hash(user['password'], password):
        return json_response.forbidden({'error_msg': 'Неверный Пароль!'})

    session['user_id'] = user['id']
    return json_response.success({'message': 'Успешная авторизация!'})

@bp.route('register', methods=['POST'])
def register():
    request_json = request.json
    first_name = request_json.get('first_name')
    last_name = request_json.get('last_name')
    email = request_json.get('email')
    password = request_json.get('password')

    if not first_name or not last_name or not email or not password:
        return json_response.bad_request({'error_msg': 'Не заполнено одно из полей!'})

    if not check_validate_email(email):
        return json_response.bad_request({'error_msg': 'Неверный формат Email!'})

    if not check_validate_password(password):
        return json_response.bad_request({'error_msg': 'Неверная длина пароля! Длина пароля должна быть от 5 до 100 символов.'})

    connection = db.connection
    cur = connection.execute(
        'SELECT email '
        'FROM users '
        'WHERE email = ?',
        (email, ),
    )
    if cur.fetchone():
        return json_response.not_acceptable({'message': 'Пользователь с таким Email уже существует!'})

    password_hash = generate_password_hash(password)

    try:
        connection.execute(
            'INSERT INTO users (first_name, last_name, email, password) '
            'VALUES (?, ?, ?, ?)',
            (first_name, last_name, email, password_hash),
        )        
    except sqlite3.IntegrityError:
        return json_response.conflict({'message': 'Не удалось выполнить запрос!'})
    connection.commit()

    cur = connection.execute(
        'SELECT id FROM users WHERE email = ?',
        (email, ),
    )
    id = cur.fetchone()['id']

    return json_response.created({
            "id": id,
            "email": email,
            "first_name": first_name,
            "last_name": last_name
        })

@bp.route('logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return json_response.success()