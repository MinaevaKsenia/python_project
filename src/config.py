import os


class Config:
    """Класс с конфигурацией для FLASK приложения"""
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv('DEBUG', False)
    DB_CONNECTION = os.getenv('DB_CONNECTION', 'db.sqlite')
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret').encode()
