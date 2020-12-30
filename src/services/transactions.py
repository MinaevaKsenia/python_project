import sqlite3
from flask import session
from models import TransactionModel
from datetime import datetime
import dateutil.parser as parser


class Unauthorized(Exception):
    pass

class TransactionExists(Exception):
    pass

class TransactionNotFound(Exception):
    pass

class TransactionError(Exception):
    pass


class TransactionService:
    def __init__(self):
        self.model = TransactionModel()
        self.user_id = session.get('user_id')

    def get(self):
        if self.user_id is None:
            raise Unauthorized
        return self.model.get_total(['id', 'date_time', 'description', 'category_id', 'summ', 'type'], self.user_id)

    def post(self, attributes: dict):
        if self.user_id is None:
            raise Unauthorized
        attributes['user_id'] = self.user_id
        try:
            date_time = parser.parse(attributes['date_time'] if 'date_time' in attributes and attributes['date_time'] else datetime.now().strftime("%Y:%m:%d %H:%M:%S")).isoformat()
            attributes['date_time'] = date_time
            transaction = self.model.create(attributes)
        except sqlite3.IntegrityError as e:
            raise TransactionExists
        return self.get_transaction_by_id(transaction)

    def get_transaction_by_id(self, tr_id):
        transaction = self.model.get_list_some_fields(['id', 'date_time', 'description', 'category_id', 'summ', 'type'], 'id', tr_id)
        if transaction is None:
            raise TransactionNotFound
        return transaction

    def patch(self, id, attributes: dict):
        if self.user_id is None:
            raise Unauthorized
        if not self.get_transaction_by_id(id):
            raise TransactionNotFound
        try:
            self.model.update(id, attributes)
        except sqlite3.IntegrityError:
            raise TransactionError
        return self.get_transaction_by_id(id)

    def get_transaction(self, id):
        if self.user_id is None:
            raise Unauthorized
        transaction = self.get_transaction_by_id(id)
        if not transaction:
            raise TransactionNotFound
        return transaction

    def delete(self, id):
        if self.user_id is None:
            raise Unauthorized
        transaction = self.get_transaction_by_id(id)
        if not transaction:
            raise TransactionNotFound
        self.model.delete(id)

    