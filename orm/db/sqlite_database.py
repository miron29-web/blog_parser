import sqlite3

from .absrtact_database import DatabaseConnection
from ..settings import DATABASE_PATH

class SQLiteConnection(DatabaseConnection):
    db_path = DATABASE_PATH
    _connect = None

    @classmethod
    def connect(cls):
        if not cls._connect:
            cls._connect = sqlite3.connect(cls.db_path)
        return cls._connect

    @classmethod
    def commit(cls):
        cls._connect.commit()
        
    @classmethod
    def close(cls):
        if cls._connect:
            cls._connect.close()
            cls._connect = None
