from ..fields import Field

class ModelMeta(type):

    def __new__(cls, name, bases, attrs):
    
        fields = dict()

        #добавляем поля от родительского класса
        for base in bases:
            if hasattr(base, "_fields"):
                fields.update(base._fields)

        #Поиск атрибутов класса которые тип Field
        for key, value in attrs.items():
            if isinstance(value, Field):
                value._name = key

                fields[key] = value

        # сохраняем все найденные данные в атрибут класса словарь
        attrs['_fields'] = fields

        return super().__new__(cls, name, bases, attrs)