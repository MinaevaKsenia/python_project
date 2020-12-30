import sqlite3
from flask import session
from models import CategoryModel


class Unauthorized(Exception):
    pass

class CategoryExists(Exception):
    pass

class CategoryNameExists(Exception):
    pass

class CategoryNotFound(Exception):
    pass


class CategoryService:
    def __init__(self):
        self.model = CategoryModel()
        self.user_id = session.get('user_id')

    def get(self):
        if self.user_id is None:
            raise Unauthorized
        return self.model.get_list_some_fields(['id', 'name'], 'user_id', self.user_id)

    def post(self, attributes: dict):
        if self.user_id is None:
            raise Unauthorized
        attributes['user_id'] = self.user_id
        try:
            category = self.model.create(attributes)
        except sqlite3.IntegrityError as e:
            raise CategoryExists
        return self.get_category_by_id(category)

    def get_category_by_id(self, cat_id):
        category = self.model.get_list_some_fields(['id', 'name'], 'id', cat_id)
        if category is None:
            raise CategoryNotFound
        return category

    def patch(self, id, attributes: dict):
        if self.user_id is None:
            raise Unauthorized
        if not self.get_category_by_id(id):
            raise CategoryNotFound
        try:
            self.model.update(id, attributes)
        except sqlite3.IntegrityError:
            raise CategoryNameExists
        return self.get_category_by_id(id)

    def get_category(self, id):
        if self.user_id is None:
            raise Unauthorized
        category = self.get_category_by_id(id)
        if not category:
            raise CategoryNotFound
        return category

    def delete(self, id):
        if self.user_id is None:
            raise Unauthorized
        category = self.get_category_by_id(id)
        if not category:
            raise CategoryNotFound
        self.model.delete(id)

    