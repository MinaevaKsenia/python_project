import sqlite3

from flask import g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'db.sqlite',
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()