from flask import Flask
from utils.database import db
from blueprints.index import bp as index_bp


def create_app():
    # Создание приложения Flask
    app = Flask(__name__)
    # Проброс конфигурационных параметров
    app.config.from_object('config.Config')
    # Регистрация Blueprint
    app.register_blueprint(index_bp, url_prefix='/')
    # Инициализация БД
    db.init_app(app)
    return app
