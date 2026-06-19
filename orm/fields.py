class Field:
    def __init__(self,
                 field_type=None,
                 name=None,
                 null=True, 
                 unique=False, 
                 primary_key=False,
                 validation=None
                 ):
        self._field_type = field_type
        self._name = name
        self._null = null
        self._unique = unique
        self._primary_key = primary_key
        self._validation = validation
    
    #функция собирает свойства полей sql
    def get_query(self):
        query_list = list()

        query_list.append(self._field_type)
        if self._primary_key:
            query_list.append("PRIMARY KEY")

        if hasattr(self, '_autoincrement'):
            if self._autoincrement:
                query_list.append("AUTOINCREMENT")

        if self._unique:
            query_list.append("UNIQUE")

        if not self._null:
            query_list.append("NOT NULL")

        return " ".join(query_list)
     
class CharField(Field):
    def __init__(self, 
                 max_length=None,
                 **kwargs
                 ):
        
        self._field_type = 'TEXT'
        self._max_length = max_length

        super().__init__(self._field_type, **kwargs)

class IntegerField(Field):
    def __init__(self, autoincrement=False, **kwargs):
        self._field_type = 'INTEGER'
        self._autoincrement = autoincrement
        
        super().__init__(self._field_type, **kwargs)

class FloatField(Field):
    def __init__(self, **kwargs):
        self._field_type = "REAL"
        super().__init__(self._field_type, **kwargs)
