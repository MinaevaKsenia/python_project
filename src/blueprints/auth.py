import sqlite3
from utils.database import db
from flask import Blueprint, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from .validators import *


bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    request_json = request.json
    email = request_json.get('email')
    password = request_json.get('password')

    if not email or not password:
        return 'Не заполнено поле Email или Пароль!', 400
    
    if not check_validate_email(email):
        return 'Неверный формат Email!', 400

    if not check_validate_password(password):
        return 'Неверная длина пароля! Длина пароля должна быть от 5 до 100 символов.', 400

    connection = db.connection
    cur = connection.execute(
        'SELECT * '
        'FROM users '
        'WHERE email = ?',
        (email, ),
    )
    user = cur.fetchone()

    if user is None:
        return 'Неверный email!', 403

    if not check_password_hash(user['password'], password):
        return 'Неверный Пароль!', 403

    session['user_id'] = user['id']
    return 'Успешная авторизация!', 200

@bp.route('register', methods=['POST'])
def register():
    request_json = request.json
    first_name = request_json.get('first_name')
    last_name = request_json.get('last_name')
    email = request_json.get('email')
    password = request_json.get('password')

    if not first_name or not last_name or not email or not password:
        return {'result':'Не заполнено одно из полей!'}, 400

    if not check_validate_email(email):
        return {'result':'Неверный формат Email!'}, 400

    if not check_validate_password(password):
        return {'result':'Неверная длина пароля! Длина пароля должна быть от 5 до 100 символов.'}, 400

    connection = db.connection
    cur = connection.execute(
        'SELECT email '
        'FROM users '
        'WHERE email = ?',
        (email, ),
    )
    if cur.fetchone():
        return {'result':'Пользователь с таким Email уже существует!'}, 406

    password_hash = generate_password_hash(password)

    try:
        connection.execute(
            'INSERT INTO users (first_name, last_name, email, password) '
            'VALUES (?, ?, ?, ?)',
            (first_name, last_name, email, password_hash),
        )        
    except sqlite3.IntegrityError:
        return 'Не удалось выполнить запрос!', 409
    connection.commit()

    cur = connection.execute(
        'SELECT id FROM users WHERE email = ?',
        (email, ),
    )
    id = cur.fetchone()

    return {
            "id": id,
            "email": email,
            "first_name": first_name,
            "last_name": last_name
        }, 201

@bp.route('logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return '', 200