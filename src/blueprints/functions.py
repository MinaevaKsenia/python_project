import sqlite3
from utils.database import db
from flask import session


def is_authorised():
    user_id = session['user_id']
    if not user_id:
        return False
    return True