import sqlite3


class SqliteDB:
    """ Класс для установки соединения с БД SQLite"""

    def __init__(self, app=None):
        self._connection = None
        self._app = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self._app = app
        self._app.teardown_appcontext(self.close_db)

    @property
    def connection(self):
        """Устанавливает и возвращает соединение с БД"""
        self._connect()
        # Включение поддержки внешних ключей в SQLite
        self._connection.execute('PRAGMA foreign_keys=on;')
        return self._connection

    def _connect(self):
        connection_string = self._app.config['DB_CONNECTION']
        self._connection = sqlite3.connect(
            connection_string,
            timeout=10,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        self._connection.row_factory = sqlite3.Row

    def close_db(self, exception):
        """Закрывает соединение с БД"""
        if self._connection is not None:
            self._connection.close()
            self._connection = None


db = SqliteDB()
