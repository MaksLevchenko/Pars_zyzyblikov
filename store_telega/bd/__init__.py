import sqlite3


def connect_to_db():
    """Подключение к базе данных"""
    conn = sqlite3.connect("zuzubliki.db")
    return conn
