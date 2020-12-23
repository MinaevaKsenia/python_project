import sqlite3
from utils.database import db
from flask import session, jsonify, Blueprint, request
from flask.views import MethodView
from utils.response import json_response
from datetime import datetime
from utils.messages import message

import dateutil.parser as parser


bp = Blueprint('transactions', __name__)

class TransactionsView(MethodView):
    def __init__(self):
       self.connection = db.connection
       self.user_id = session['user_id'] if session.get('user_id') else None

    def get(self):
        if not self.user_id:
            json_response.forbidden(message.MSG_NO_RIGHTS)

        temp = self.connection.execute(
           'SELECT * FROM transactions WHERE user_id = ? ORDER BY date_time',
           (self.user_id, ) 
        )
        rows = temp.fetchall()

        temp = self.connection.execute(
            '''WITH T AS (
            SELECT id, summ as s
            FROM transactions
            WHERE type = 1 AND user_id = ?
            UNION 
            SELECT id, -summ as s
            FROM transactions
            WHERE type = 2 AND user_id = ?)

            SELECT count(*) as count, CAST(sum(s) AS FLOAT) as total
            FROM T''',
            (self.user_id, self.user_id, )
        )
        vars = temp.fetchone()

        if rows is None:
           return json_response.success()
        return json_response.success({'data': [dict(row) for row in rows], 'count': vars['count'], 'total': vars['total']})

    def post(self):
        if not self.user_id:
            json_response.forbidden(message.MSG_NO_RIGHTS)

        request_json = request.json
        type = request_json.get('type')
        sum = request_json.get('summ')
        desc = request_json.get('description')
        cat_id = request_json.get('category_id')
        date_time = request_json.get('date_time')

        # date to iso
        date_time = parser.parse(date_time if date_time else datetime.now().strftime("%Y:%m:%d %H:%M:%S")).isoformat()

        if not type or not sum or not desc:
            return json_response.bad_request(message.MSG_EMPTY_FIELD)

        try:
            print(date_time)
            temp = self.connection.execute(
                'INSERT INTO transactions (type, summ, description, category_id, date_time, user_id) VALUES(?, ?, ?, ?, ?, ?)',
                (type, sum, desc, cat_id, date_time, self.user_id, )
            )
        except sqlite3.IntegrityError:
            return json_response.conflict(message.MSG_REQ_FAILED)
        self.connection.commit()

        temp = self.connection.execute(
            'SELECT last_insert_rowid() as id'
        )
        id = temp.fetchone()['id']
        return json_response.created({
            "category_id": cat_id,
            "date_time": date_time,
            "id": id,
            "sum": sum,
            "type": type
        })

class TransactionView(MethodView):
    def __init__(self):
       self.connection = db.connection
       self.user_id = session['user_id'] if session.get('user_id') else None

    def get(self, id):
        if not self.user_id:
            json_response.forbidden(message.MSG_NO_RIGHTS)

        temp = self.connection.execute(
        'SELECT * FROM transactions WHERE id = ? AND user_id = ?',
        (id, self.user_id, )
        )
        row = temp.fetchone()
        if not row:
            return json_response.not_found(message.MSG_NOT_TR_BY_ID)

        return json_response.success({
            "category_id": row['category_id'],
            "date_time": row['date_time'],
            "id": id,
            "sum": row['summ'],
            "type": row['type']
        })

    def patch(self, id):
        if not self.user_id:
            json_response.forbidden(message.MSG_NO_RIGHTS)

        temp = self.connection.execute(
        'SELECT * FROM transactions WHERE id = ? AND user_id = ?',
        (id, self.user_id, )
        )
        row = temp.fetchone()
        if not row:
            return json_response.not_found(message.MSG_NOT_TR_BY_ID)

        request_json = request.json
        sum = request_json.get('summ')
        desc = request_json.get('description')
        cat_id = request_json.get('category_id')
        date_time = request_json.get('date_time')

        date_time = parser.parse(date_time if date_time else datetime.now().strftime("%Y:%m:%d %H:%M:%S")).isoformat()

        if not sum or not desc:
            return json_response.bad_request(message.MSG_EMPTY_FIELD)

        try:
            temp = self.connection.execute(
                'UPDATE transactions '
                'SET summ = ? , category_id = ?, description = ?, date_time = ?'
                'WHERE id = ?',
                (sum, cat_id, desc, date_time, id, )
            )
        except sqlite3.IntegrityError:
            return json_response.conflict(message.MSG_REQ_FAILED)
        self.connection.commit()

        temp = self.connection.execute(
            'SELECT type FROM transactions WHERE id = ?',
            (id, )
        )
        type = temp.fetchone()['type']

        return json_response.created({
            "id": id,
            "category_id": cat_id,
            "date_time": date_time,
            "description": desc,
            "summ": sum,
            "type": type
        })

    def delete(self, id):
        if not self.user_id:
            json_response.forbidden(message.MSG_NO_RIGHTS)

        temp = self.connection.execute(
        'SELECT * FROM transactions WHERE id = ? AND user_id = ?',
        (id, self.user_id, )
        )
        row = temp.fetchone()
        if not row:
            return json_response.not_found(message.MSG_NOT_TR_BY_ID)

        try:
            temp = self.connection.execute(
                'DELETE FROM transactions '
                'WHERE id = ?',
                (id, )
            )
        except sqlite3.IntegrityError:
            return json_response.conflict(message.MSG_REQ_FAILED)
        self.connection.commit()

        return json_response.deleted()


bp.add_url_rule('', view_func=TransactionsView.as_view('transactions_view'))
bp.add_url_rule('/<int:id>/', view_func=TransactionView.as_view('transaction_view'))