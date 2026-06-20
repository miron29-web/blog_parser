from orm.models.model import Model

class SQLiteStorage:
    """
    Класс для работы с ORM и SQLite

    Выполняет:
    -- Сохранение данных в БД
    -- Получение данных из БД
    """
    def __init__(self, model_class:Model):
        self.model = model_class

    def save_to_sqlite(self, json_data:dict):
        """
        Сохраняет список словарей в БД через ORM
        """
        for data in json_data:
            obj = self.model()
            obj.title = data["title"]
            obj.desc = data["desc"]

            obj.save()

    def get_from_sqlite(self):
        """
        Получает все данные из БД в список словарей
        """
        obj = self.model()
        data = obj.select_all()
        
        result = [
            {"title": d[1], "desc": d[2]}
            for d in data
        ]

        return result