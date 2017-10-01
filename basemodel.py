from peewee import *

db = MySQLDatabase('blackjack', user='root', passwd='root')

class BaseModel(Model):
        class Meta:
            database = db
