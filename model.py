from orm.fields import *
from orm.models.model import Model

class Article(Model):
    table_name = "articles"

    id = IntegerField(name="id", primary_key=True, autoincrement=True)
    title = CharField()
    desc = CharField()