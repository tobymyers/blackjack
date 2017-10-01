# from blackjackhand import hasAce
# cards = [['1',1,'ace'],[2,2,2],[4,4,4]]
# handTotal = 12
# hand = 0
# hasAce(hand, cards, handTotal)



# from deck import *
# from card import *
# from hand import *
# from player import *
# from game import *
# import players
# from slackclient import SlackClient
#
# c= Card("ace", 4, 5)
# d = Deck()
# print(d.getPlayed())
# print(d.getUnplayed())
# print(d.getFullDeck())
# print(d.shuffle())
# print(d.dealCard(2))
# hand = Hand(d)
# print(hand.getHand())
# p = Player("player", "Toby", 011)
# print(p.addCash(100))
# print(p.bet(50))
# print(p.getCash())
# print(p.split(hand, d))
# g = Game("testGame")
# print(g.createPlayers())
# print(g.connect())
# print(g.read())

#works, still gotta figure out foreign key stuff
from player import *
from user import *
from peewee import *
from hand import *
from game import *
# from blackjackhand import *
# from convert import *
db = MySQLDatabase('blackjack', user='root', passwd='root')
db.connect()
db.create_tables([Player, User, Hand, Game])
# toby2 = User(slack_id = 12345 , name ="toby")
# toby2.save()
# toby2 = Player(user = 1 ,cash= 1000, dealer = 0)
# toby2.save()
# game1 = Game()
# game1.save()
# hand1 = Hand(player = 1, cards = '8 of clubs', game = 1)
# hand1.save()
# hand = Hand.get(Hand.cards == '8 of clubs')
# print(hand.cards)
# testUser = User.create(slack_id = "1", name = "Toby")
#
# print(type(testUser), 'testUser')
# print(type(testUser.name), 'testUser.Name')
# testUserName = User.get(User.name == "Toby").name
# print(type(testUserName))
# testPlayer = Player(user = 6, cash = 1000, dealer = 0, player_state = 0)
# testPlayer.save()
# print(testPlayer.get())
# print(testPlayer.cash, testPlayer.dealer, testPlayer.player_state)
# bj1 = BlackJackPlayer(testUser)
# print(bj1.player.cash)
# bj1.addCash(500)
# print(bj1.player.cash)
# from user import *
# import json
#
# user = User.create(slack_id = "3", name = "")
# testList = [1,2,3]
# user.name = json.dumps(testList)
# user.save()
# user = user.get(User.slack_id == "3")
# print(user.name)
# print(type(user.name))
# newList = json.loads(user.name)
# print(type(newList))
# newestList = list(newList)
# print(newestList[0])
# print(newestList)
# print(type(newestList))
# print(newestList.pop(0))
#
# ANSWER!!! json.loads and json.dumps will solve all my problems!!!!!
