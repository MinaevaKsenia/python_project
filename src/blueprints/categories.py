import sqlite3
from utils.database import db
from flask import Blueprint, request, session, jsonify
from flask.views import MethodView

bp = Blueprint('categories', __name__)

class CategoriesView(MethodView):
    def get(self):
        connection = db.connection
        cur = connection.execute(
           'SELECT * FROM users' 
        )
        rows = cur.fetchall()
        return jsonify([dict(row) for row in rows])



bp.add_url_rule('', view_func=CategoriesView.as_view('categories_view'))