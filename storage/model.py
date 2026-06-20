from orm.fields import *
from orm.models.model import Model

class Article(Model):
    """
    Описание модели для хранения данных в БД через ORM
    """
    table_name = "articles"

    id = IntegerField(name="id", primary_key=True, autoincrement=True)
    title = CharField(unique=True)
    desc = CharField()