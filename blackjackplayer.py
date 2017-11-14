from player import *
from user import *
from peewee import *
from game import *

class BlackJackPlayer:
    def __init__(self, user):
        """creates a player by testing to see if the user exists for that player, creating a user if not
        and then creating a player based on that user"""

        player = Player.select().where((Player.user_id == user.id) & (Player.dealer == dealer))
        if dealer:
            cash = 1000000
        else:
            cash = 1000

        if not player.exists():
            player = Player(user_id = user.id, cash = cash, dealer = dealer, player_state = 0)
            player.save()


        self.player = player.get()

    def addCash(self, user, cash):
        player = Player.get((Player.user_id == user.id) & (Player.dealer == False))
        intcash = int(player.cash)
        cash = intcash + int(cash)
        player.cash = cash
        player.save()

    def updateState(self, user, state):
        player = Player.get((Player.user_id == user.id) & (Player.dealer == False))
        player.player_state = state
        player.save()

    def getPlayer(self, user):
        player = Player.get((Player.user_id == user.id) & (Player.dealer == False))
        return player

    def registerBet(self, user, bet):
        player = Player.get((Player.user_id == user.id) & (Player.dealer == False))
        player.cash = int(player.cash) - bet
        player.save()


    def getCash(self, user):
        player = Player.get((Player.user_id == user.id) & (Player.dealer == False))
        return player.cash

    def split(self, hand, deck):
        self.hand1 = []
        self.hand2 = []
        if hand.getHand()[0][1] == hand.getHand()[1][1]:
            self.hand1.append(hand.getHand()[0])
            self.hand1.append(deck.dealCard(1))
            self.hand2.append(hand.getHand()[1])
            self.hand2.append(deck.dealCard(1))
            self.bet += self.bet
        return self.hand1, self.hand2, self.bet

    def doubleDown(self):
         self.bet += self.bet
         return self.bet
