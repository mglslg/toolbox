from peewee import *

database = MySQLDatabase('memory_master',
                         **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': '127.0.0.1',
                            'port': 3306, 'user': 'slg', 'password': 'enter'})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class EnDict(BaseModel):
    content = CharField(null=True)
    create_time = DateTimeField(null=True)
    is_open = IntegerField(null=True)
    key = CharField(primary_key=True)
    pass_time = DateTimeField(null=True)
    show_time = DateTimeField(null=True)
    pass_count = IntegerField(null=True)
    voice = CharField(null=True)

    class Meta:
        table_name = 'en_dict'
