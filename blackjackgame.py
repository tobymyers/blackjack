from card import *
from game import *
from hand import *
import json

class BlackJackGame:
   def __init__(self, user):

       game = Game.select().where((Game.user_id == user.id) & (Game.active == True))

       if not game.exists():
           game = Game.create(played_cards = json.dumps([]), unplayed_cards = [], active = True, user_id = user.id)
           game.save()


   def getPlayed(self):
       return Game.get(Game.id == self.game.id).played_cards

   def getUnplayed(self, user):
       game = Game.get((Game.user_id == user.id) & (Game.active == 1))
       print(game.unplayed_cards)
       return json.loads(game.unplayed_cards)


   def end(self, user):
       game = Game.get((Game.active == True) & (Game.user_id == user.id))
       game.active = False
       game.save()

       hands = Hand.select().where(Hand.active == True)
       for hand in hands:
           hand.active = False
           hand.save()

       response = "this game has ended, you can `start` a new one if you like"
       return response


   def activeHands(self):
        hand = Hand.select().where(Hand.active == True)
        if hand.exists():
            return True
        return False



   def makeDeck(self, user):
       names = ['ACE', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:', 'JACK', 'QUEEN', 'KING'] #['1','2','3','4','5','6','7','8','9','0','J','Q','K']
       numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
       suits = [":spades:", ":clubs:", ":hearts:", ":diamonds:"]#['C', 'S', 'H', 'D']
       unplayed = []
       played = []
       for suit in suits:
           for number, name in zip(numbers, names):
               card = Card(suit, number, name)
               unplayed.append(card.getCard())

       game = Game.get((Game.active == True) & (Game.user_id == user.id))
       game.unplayed_cards = json.dumps(unplayed)
       game.save()

   def getHand(self, user, dealer):
       player = Player.get((Player.user_id == user.id) & (Player.dealer == dealer))
       hand = Hand.get((Hand.player_id == player.id) & (Hand.active == True))
       return hand



   def shuffle(self, user):
       """shuffles unplayed cards"""
       from random import randrange
       game = Game.get((Game.active == True) & (Game.user_id == user.id))
       unplayed = json.loads(game.unplayed_cards)
       shuffled = []
       count = len(unplayed)
       for i in range(len(unplayed)):
           shuffled.append(unplayed.pop(randrange(count)))
           count-=1
       game.unplayed_cards = json.dumps(shuffled)
       game.save()


   def getPlayed(self):
       return Game.get(Game.id == self.game.id).played_cards


   def getId(self, user):
       return Game.get(Game.user_id == user.id).id

   def dealCard(self, numCards, user):
       game = Game.get((Game.user_id == user.id) & (Game.active == True))
       cards = []
       played = json.loads(game.played_cards)
       print(type(played))
       unplayed = json.loads(game.unplayed_cards)
       for i in range(numCards):
           card = unplayed.pop(0)
           played.append(card)
           cards.append(card)
       game.unplayed_cards = json.dumps(unplayed)
       game.played_cards = json.dumps(played)
       game.save()

       print('cards', list(cards))
       return cards

   def chooseWinner(self, user, dealerTotal, playerTotal):
       player = Player.get((Player.user_id == user.id) & (Player.dealer == False))
       hand = Hand.get((Hand.player_id == player.id) & (Hand.active == True))
       game = Game.get(Game.user_id == user.id)
       response = ''
       if dealerTotal > 21 or (playerTotal <= 21 and playerTotal >= dealerTotal):
           player.cash = int(player.cash) + int(hand.bet * 2)
           player.save()
           response = '*You win* $' + str(int(hand.bet)) + ':moneybag: You have '  +str(player.cash)+' `~bet` again?' #if exists another active hand, play it
       else:
           response = '*You lose* $' +str(hand.bet) + ':cry: `~bet` again?' #if exists another active hand, play it
       return response
