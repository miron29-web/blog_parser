from .model_meta import ModelMeta
from ..fields import Field

from ..db.db_manager import DatabaseManager

class Model(metaclass=ModelMeta):
    #Объект для управления БД
    db_manager = DatabaseManager()

    def __init__(self, **kwargs):
        #Получаем название таблицы. Если не название в переменную table_name то названием будет имя класса
        self.table_name = getattr(
            self.__class__,
            "table_name",
            self.__class__.__name__.lower()
        )

        #Присваиваем поля из дочернего класса
        for key, value in kwargs.items():
            setattr(self, key, value)

        super().__init__()

    #Создание таблицы
    def create_table(self):
        query_fields = list()

        # собираем свойства полей SQL из словаря _fields
        for name, field in self._fields.items():
            query_fields.append(name + " " + field.get_query())

        sql = f"""CREATE TABLE IF NOT EXISTS `{self.table_name}` (
            {", ".join(query_fields)}
        );"""

        self.db_manager.execute(sql)
        self.db_manager.commit()

        return sql

    #запись в БД
    def save(self):
        fields = list()
        values = list()

        #перебираем все поля модели из словаря _fields
        for name, field in self._fields.items():
            value = getattr(self, name, None)

            #если поле не было заполнено данными вместо Field присваиваем None
            if isinstance(value, Field):
                value = None

            #если поле автоинкриментное пропускаем его
            if getattr(field, "_autoincrement", False) and value is None:
                continue

            #Проверка на обязательные для заполнения поля
            if not field._null and value is None:
                raise ValueError(f"Поле {name} не может быть пустым")
            
            #Запуск валидации переданной в поле Field
            if field._validation:
                field._validation(value)

            fields.append(name)
            values.append(value)

        sql = f"INSERT OR IGNORE INTO {self.table_name} ({', '.join(fields)}) VALUES ({', '.join(['?']*len(values))})"

        cursor = self.db_manager.execute(sql, tuple(values))

        #сохранение id
        if "id" in self._fields:
            self.id = cursor.lastrowid

        cursor.close()

        return sql

    #Возвращение всех записей из таблицы
    def select_all(self):
        sql = f"SELECT * FROM `{self.table_name}`"

        return self.db_manager.fetch_all(sql)
    
    #Обновление данных по ключу
    def update(self):
        new_values = []
        values = []

        pk_name = None
        pk_value = None

        #собираем новые данные
        for name, field in self._fields.items():

            if field._primary_key:
                pk_name = name
                pk_value = getattr(self, name)

            new_values.append(f"{name} = ?")
            values.append(getattr(self, name))

        if pk_name is None:
            raise ValueError("Первичный ключ не найден")
        
        if isinstance(pk_value, Field):
            raise ValueError("Объект не сохранен в БД")
        
        values.append(pk_value)

        sql = f"UPDATE {self.table_name} SET {', '.join(new_values)} WHERE {pk_name} = ?"

        self.db_manager.execute(sql, tuple(values))

        return sql
    
    #Возвращает список колонок из БД
    def get_columns(self):
        sql = f"PRAGMA table_info({self.table_name})"
        
        result = self.db_manager.fetch_all(sql)

        return [row[1] for row in result]
    
    #Добавляет в БД новые поля которых нет
    def migrate(self):
        columns = self.get_columns()

        alerts = list()

        #Ищем отсутствующие колонки
        for name, field in self._fields.items():
            if name not in columns:
                alerts.append(f"ALTER TABLE {self.table_name} ADD COLUMN {name} {field.get_query()};")

        sql = f"""
            BEGIN TRANSACTION;
            {" ".join(alerts)}
            COMMIT;"""

        self.db_manager.executescript(sql)