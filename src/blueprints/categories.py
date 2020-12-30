import sqlite3
from utils.database import db
from flask import Blueprint, request, session, jsonify
from flask.views import MethodView
from utils.response import json_response
from utils.messages import message
from services.categories import CategoryService, Unauthorized, CategoryExists, CategoryNotFound, CategoryNameExists


bp = Blueprint('categories', __name__)

class CategoriesView(MethodView):
    def __init__(self):
        self.category_service = CategoryService()

    def get(self):
        try:
            categories = self.category_service.get()
        except Unauthorized:
            return json_response.unauthorized()
        return json_response.success(categories)

    def post(self):
        data = request.get_json()
        
        if not data['name']:
            return json_response.bad_request(message.MSG_EMPTY_FIELD)
        try:
            category = self.category_service.post(data)
        except Unauthorized:
            return json_response.unauthorized()
        except (CategoryExists, CategoryNotFound) as e:
            return json_response.conflict()
        return json_response.created(category)
        

class CategoryView(MethodView):
    def __init__(self):
        self.category_service = CategoryService()

    def patch(self, id):
        data = request.get_json()
        if not data['name']:
            return json_response.bad_request(message.MSG_EMPTY_FIELD)
        try:
            category = self.category_service.patch(id, data)
        except Unauthorized:
            return json_response.unauthorized()
        except (CategoryNotFound, CategoryNameExists):
            return json_response.conflict()
        return json_response.created(category)

    def get(self, id):
        try:
            category = self.category_service.get_category(id)
        except Unauthorized:
            return json_response.unauthorized()
        except CategoryNotFound:
            return json_response.not_found()
        return json_response.success(category)
        
    def delete(self, id):
        try:
            category = self.category_service.delete(id)
        except Unauthorized:
            return json_response.unauthorized()
        except CategoryNotFound:
            return json_response.not_found()
        return json_response.deleted()

    

bp.add_url_rule('', view_func=CategoriesView.as_view('categories_view'))
bp.add_url_rule('/<int:id>/', view_func=CategoryView.as_view('category'))