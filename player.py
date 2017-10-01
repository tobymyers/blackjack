from basemodel import *
from user import *
from game import *

class Player(BaseModel):
        user = ForeignKeyField(User, related_name = 'users')
        id = PrimaryKeyField()
        cash = CharField()
        dealer = BooleanField()
        player_state = IntegerField()
