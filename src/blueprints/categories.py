import sqlite3
from utils.database import db
from flask import Blueprint, request, session, jsonify
from flask.views import MethodView
from utils.response import json_response
from blueprints.functions import *
from utils.messages import message



bp = Blueprint('categories', __name__)

class CategoriesView(MethodView):
    def __init__(self):
       self.connection = db.connection
       self.user_id = session['user_id'] if session.get('user_id') else None
        
    def get(self): 
        if not self.user_id:
            return json_response.forbidden(message.MSG_NO_RIGHTS)
        temp = self.connection.execute(
           'SELECT id, name FROM categories WHERE user_id = ?',
           (self.user_id, ) 
        )
        rows = temp.fetchall()
        if rows is None:
            return json_response.success(message.MSG_NOT_CAT)
        return jsonify([dict(row) for row in rows])

    def post(self):
        if not self.user_id:
            json_response.forbidden(message.MSG_NO_RIGHTS)

        request_json = request.json
        name = request_json.get('name')

        if not name:
            return json_response.bad_request(message.MSG_EMPTY_FIELD)

        temp = self.connection.execute(
            'SELECT name FROM categories WHERE user_id = ? AND name = ?',
            (self.user_id, name, )
        )
        if temp.fetchone():
            return json_response.not_acceptable(message.MSG_CAT_EXIST)

        try:
            temp = self.connection.execute(
                'INSERT INTO categories (name, user_id) VALUES(?, ?)',
                (name, self.user_id, )
            )
        except sqlite3.IntegrityError:
            return json_response.conflict(message.MSG_REQ_FAILED)
        self.connection.commit()

        temp = self.connection.execute(
            'SELECT last_insert_rowid() as id'
        )
        id = temp.fetchone()['id']

        return json_response.created({
            "id": id,
            "name": name
        })


class CategoryView(MethodView):
    def __init__(self):
       self.connection = db.connection
       self.user_id = session['user_id']

    def patch(self, id):
        if not self.user_id:
            json_response.forbidden(message.MSG_NO_RIGHTS)

        request_json = request.json
        name = request_json.get('name')

        temp = self.connection.execute(
            'SELECT * FROM categories WHERE id = ? AND user_id = ?',
            (id, self.user_id)
        )
        row = temp.fetchone()
        if not row:
            return json_response.not_found(message.MSG_NOT_CAT_BY_ID)

        if not name:
            return json_response.bad_request(message.MSG_EMPTY_FIELD)

        temp = self.connection.execute(
            'SELECT name FROM categories WHERE name = ?',
            (name, )
        )
        if temp.fetchone():
            return json_response.not_acceptable(message.MSG_CAT_EXIST)

        try:
            temp = self.connection.execute(
                'UPDATE categories '
                'SET name = ? '
                'WHERE id = ?',
                (name, id, )
            )
        except sqlite3.IntegrityError:
            return json_response.conflict(message.MSG_REQ_FAILED)
        self.connection.commit()

        return json_response.created({
            "id": id,
            "name": name
        })

    def get(self, id):
        if not self.user_id:
            json_response.forbidden(message.MSG_NO_RIGHTS)

        temp = self.connection.execute(
            'SELECT * FROM categories WHERE id = ? AND user_id = ?',
            (id, self.user_id)
        )
        row = temp.fetchone()
        if not row:
            return json_response.not_found(message.MSG_NOT_CAT_BY_ID)

        temp = self.connection.execute(
        'SELECT name FROM categories WHERE id = ?',
        (id, )
        )
        name = temp.fetchone()['name']

        return json_response.success({
            "id": id,
            "name": name
        })

    def delete(self, id):
        if not self.user_id:
            json_response.forbidden(message.MSG_NO_RIGHTS)

        temp = self.connection.execute(
            'SELECT * FROM categories WHERE id = ? AND user_id = ?',
            (id, self.user_id)
        )
        row = temp.fetchone()
        if not row:
            return json_response.not_found(message.MSG_NOT_CAT_BY_ID)

        try:
            temp = self.connection.execute(
                'DELETE FROM categories '
                'WHERE id = ?',
                (id, )
            )
        except sqlite3.IntegrityError:
            return json_response.conflict(message.MSG_REQ_FAILED)
        self.connection.commit()

        return json_response.deleted()


bp.add_url_rule('', view_func=CategoriesView.as_view('categories_view'))
bp.add_url_rule('/<int:id>/', view_func=CategoryView.as_view('category'))