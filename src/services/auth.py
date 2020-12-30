import sqlite3
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from models import UserModel


class EmailAlreadyExist(Exception):
    pass


class UserNotFound(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class AuthService:

    def __init__(self):
        self.model = UserModel()

    def login(self, email, password):
        user = self.model.get_by_field('email', email)

        if user is None:
            raise UserNotFound

        if not check_password_hash(user['password'], password):
            raise InvalidCredentials

        self._authorize(user)

    def register(self, attributes: dict):
        attributes['password'] = generate_password_hash(attributes['password'])
        try:
            user_id = self.model.create(attributes)
        except sqlite3.IntegrityError as e:
            raise EmailAlreadyExist from e
        return self.get_user_profile(user_id)

    def get_user_profile(self, user_id):
        user = self.model.get_by_id(user_id)
        if user is None:
            raise UserNotFound
        return user

    @classmethod
    def _authorize(cls, user):
        session['user_id'] = user['id']

    @staticmethod
    def logout():
        session.pop('user_id', None)

    @staticmethod
    def get_auth_user_id():
        return session.get('user_id')