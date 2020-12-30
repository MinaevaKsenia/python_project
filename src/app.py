from flask import Flask
from utils.database import db
from blueprints.index import bp as index_bp
from blueprints.auth import bp as auth_bp
from blueprints.categories import bp as categories_bp
from blueprints.transactions import bp as transactions_bp


def create_app():
    # Создание приложения Flask (оно будет обрабатывать наши запросы)
    app = Flask(__name__)
    # Проброс конфигурационных параметров
    app.config.from_object('config.Config')
    # Регистрация Blueprint
    app.register_blueprint(index_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth/')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    # Инициализация БД
    db.init_app(app)
    return app
