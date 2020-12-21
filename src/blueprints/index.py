import sqlite3
from flask import Blueprint
from flask import request
from utils.database import db
from utils.response import json_response

from flask import Flask, session, jsonify
from .db_sqlite import get_db, close_db 


bp = Blueprint('index', __name__)

def create_sql(attributes: dict):
    field_names = attributes.keys()
    field_values = attributes.values()
    placeholder = ",".join(field_names).rstrip(',')
    placeholder_2 = ("?," * len(field_values)).rstrip(',')

    query = f""" INSERT INTO users ({placeholder}) VALUES ('test', 'test', 'test', 'test') """
    values = tuple()
    return query, values


@bp.route('/', methods=['GET', 'POST'])
def index():
    #response = {'message': 'Hello World'}
    #return json_response.success(response)

    if request.method == 'GET':
        return "Hello"
    else:
        return "This is POST!"

    # connection = db.connection

    # №1
    # query = "SELECT * FROM users"
    # result = connection.execute(query).fetchall()
    # users = [dict(row) for row in result]
    # response = {'message': 'Hello World'}

    #print(request.form['username'])
    #return json_response.success({'name': int(request.form['num'])*2})

    # №2
    #query = """
    #    INSERT INTO users (first_name, last_name, email, password) VALUES ('test', 'test', 'test', 'test')
    #"""
    #values = tuple(['test2', 'test2', 'test2', 'test2'])
    #connection.execute(query)
    #connection.commit()
    #return json_response.success()

    # №3
    #query = """
    #    INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)
    #"""
    #values = tuple(['test2', 'test2', 'test2', 'test2'])
    #connection.execute(query, values)
    #connection.commit()
    #return json_response.success()

    # №4
    # user = {
    #     'first_name': 'Ivan',
    #     'last_name': 'Ivan',
    #     'email': 'test@345.ru',
    #     'password': '12345'
    # }
    # query, values = create_sql(user)
    # connection.execute(query, values)
    # connection.commit()
    return json_response.success()

# из видео:
#bp.teardown_appcontext(close_db) # при остановке приложения все закрывается, чистится
bp.secret_key = b'skjdvk' # ключ для шифрования сессий

@bp.route('/ads')
def get_ads():
    user_id = session.get('user_id')
    if user_id is None:
        return '', 403

    con = get_db()
    cur = con.execute(
        'SELECT * '
        'FROM ad '
        'WHERE user_id = ?',
        (user_id),
    )
    result = cur.fetchall()
    #return[dict(row) for row in result]
    return jsonify([dict(row) for row in result])

