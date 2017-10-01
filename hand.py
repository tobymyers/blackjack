from player import *
from basemodel import *
from game import *

class Hand(BaseModel):
        player = ForeignKeyField(Player, related_name = 'hands')
        game = ForeignKeyField(Game, related_name = 'games')
        id = PrimaryKeyField()
        cards = CharField()
        bet = IntegerField()
        active = BooleanField()
