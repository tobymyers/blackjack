from basemodel import *
from user import *

class Game(BaseModel):
    id = PrimaryKeyField()
    played_cards = TextField()
    unplayed_cards = TextField()
    active = BooleanField()
    user = ForeignKeyField(User, related_name = 'user')
