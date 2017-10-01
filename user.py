from peewee import *
from basemodel import BaseModel

class User(BaseModel):
    id = PrimaryKeyField() #test won't save the user if this is a primary key field
    slack_id = CharField()
    name = CharField()
    trolled = BooleanField()
