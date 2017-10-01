import peewee
from peewee import *

db = MySQLDatabase('blackjack', user='root', passwd='root')

class Player(peewee.Model):
    slack_id = peewee.CharField()
    cash = peewee.IntegerField()

    class Meta:
        database = db
    
    def getCash():
        return self.cash	

existing_player = Player.select().where(Player.slack_id == '12345')

if not existing_player.exists():
    new_player = Player(slack_id="12345", cash=1000)
    new_player.save()

for player in Player.select():
    print player.id
    print player.slack_id
    print player.cash
