from peewee import *

database = MySQLDatabase('memory_master',
                         **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': '127.0.0.1',
                            'port': 3306, 'user': 'slg', 'password': 'enter'})

tx_database = MySQLDatabase('memory_master',
                             **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True,
                                'host': '81.70.172.33',
                                'port': 3306, 'user': 'slg', 'password': 'enter'})


class BaseModel(Model):
    class Meta:
        database = tx_database
        #database = database


class EnDict(BaseModel):
    content = CharField(null=True)
    create_time = DateTimeField(null=True)
    is_open = IntegerField(null=True)
    key = CharField(primary_key=True)
    pass_time = DateTimeField(null=True)
    show_time = DateTimeField(null=True)
    pass_count = IntegerField(null=True)
    voice = CharField(null=True)
    example = CharField(null=True)
    custom_eg = CharField(null=True)
    eg_tag = CharField(null=True)
    comment = CharField(null=True)
    username = CharField(null=True)

    class Meta:
        table_name = 'en_dict'


class SysUser(BaseModel):
    username = CharField(primary_key=True)
    password = CharField(null=True)

    class Meta:
        table_name = 'sys_user'
