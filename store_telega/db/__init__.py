import sqlite3
from config.config import gen_path


def connect_to_db():
    """Подключение к базе данных"""
    conn = sqlite3.connect(f"{gen_path}/db/zuzubliki.db")
    return conn
