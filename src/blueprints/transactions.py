import sqlite3
from utils.database import db
from flask import session, jsonify, Blueprint, request
from flask.views import MethodView
from utils.response import json_response
from datetime import datetime
from utils.messages import message
from services.transactions import TransactionService
from services.transactions import TransactionService, Unauthorized, TransactionExists, TransactionNotFound, TransactionError

import dateutil.parser as parser


bp = Blueprint('transactions', __name__)

class TransactionsView(MethodView):
    def __init__(self):
        self.transaction_service = TransactionService()

    def get(self):
        try:
            transactions = self.transaction_service.get()
        except Unauthorized:
            return json_response.unauthorized()
        return json_response.success(transactions)

    def post(self):
        data = request.get_json()
        
        if not data['type'] or not data['summ'] or not data['description']:
            return json_response.bad_request(message.MSG_EMPTY_FIELD)
        try:
            transaction = self.transaction_service.post(data)
        except Unauthorized:
            return json_response.unauthorized()
        except (TransactionExists, TransactionNotFound) as e:
            return json_response.conflict()
        return json_response.created(transaction)

class TransactionView(MethodView):
    def __init__(self):
        self.transaction_service = TransactionService()

    def get(self, id):
        try:
            transaction = self.transaction_service.get_transaction(id)
        except Unauthorized:
            return json_response.unauthorized()
        except TransactionNotFound:
            return json_response.not_found()
        return json_response.success(transaction)

    def patch(self, id):
        data = request.get_json()
        if not data['summ'] or not data['description']:
            return json_response.bad_request(message.MSG_EMPTY_FIELD)
        try:
            transaction = self.transaction_service.patch(id, data)
        except Unauthorized:
            return json_response.unauthorized()
        except (TransactionNotFound, TransactionError):
            return json_response.conflict()
        return json_response.created(transaction)

    def delete(self, id):
        try:
            transaction = self.transaction_service.delete(id)
        except Unauthorized:
            return json_response.unauthorized()
        except TransactionNotFound:
            return json_response.not_found()
        return json_response.deleted()

bp.add_url_rule('', view_func=TransactionsView.as_view('transactions_view'))
bp.add_url_rule('/<int:id>/', view_func=TransactionView.as_view('transaction_view'))