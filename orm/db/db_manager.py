from .sqlite_database import SQLiteConnection

class DatabaseManager:
    def __init__(self):
        self._connection = SQLiteConnection.connect()

    def execute(self, sql, values=None):
        cursor = self._connection.cursor()

        if values:
            cursor.execute(sql, values)
        else:
            cursor.execute(sql)
        
        self._connection.commit()
        
        return cursor
    
    def executescript(self, sql, values=None):
        cursor = self._connection.cursor()

        cursor.executescript(sql)
        self._connection.commit()

        return cursor

    def fetch_all(self, sql):
        cursor = self._connection.cursor()

        cursor.execute(sql)
        result = cursor.fetchall()
        
        cursor.close()

        return result
    
    def commit(self):
        self._connection.commit()

    def close(self):
        self._connection.close()