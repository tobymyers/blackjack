from player import *
from hand import *
from game import *
from blackjackgame import *
import json
from operator import itemgetter

def hasAce(cards, handTotal):
    cards = sorted(cards, key = itemgetter(1)) #reverse sorts the list putting the aces at teh end, so all counts will treat Ace right
    for card in cards:
        if card[1] == 1:
            if handTotal > 6 and handTotal < 12:
                handTotal += 10
    return handTotal


class BlackJackHand:

    def __init__(self, user, game, bet, dealer):
        player = Player.get((Player.user_id == user.id) & (Player.dealer == dealer))
        hand = Hand.select().where((Hand.player_id == player.id) & (Hand.active == True))

        if not hand.exists():
            hand = Hand.create(player = player.id, game = game.getId(user), cards = json.dumps([]), bet = bet, active = True)
            hand.save()

    def addCards(self, user, newCards, dealer):
        player = Player.get((Player.user_id == user.id) & (Player.dealer == dealer))
        print(player.id ,'PlayerId')
        #hand = Hand.select().where((Hand.player_id == player.id) & (Hand.active == True))
        hand = Hand.get((Hand.player_id == player.id) & (Hand.active == True))
        print("handId", hand.id)
        print(hand.cards, "cards in hand")
        if len(json.loads(hand.cards)) > 0:
            oldCards = json.loads(hand.cards)
            print(oldCards)
        else:
            oldCards = []

        print(type(hand.cards))
        for card in newCards:
            oldCards.append(card)

        hand.cards = json.dumps(oldCards)
        hand.save()

    def close(self, user, dealer):
        player = Player.get((Player.user_id == user.id) & (Player.dealer == dealer))
        hand = Hand.get((Hand.player_id == player.id) & (Hand.active == True))
        hand.active = False
        hand.save()


    def getBet(self, user, dealer):
        player = Player.get((Player.user_id == user.id) & (Player.dealer == dealer))
        hand = Hand.get((Hand.player_id == player.id) & (Hand.active == True))
        return hand.bet

    def changeBet(self, user, dealer, newBet):
        player = Player.get((Player.user_id == user.id) & (Player.dealer == dealer))
        hand = Hand.get((Hand.player_id == player.id) & (Hand.active == True))
        hand.bet = newBet
        hand.save()

    def getCards(self, user, dealer):
        player = Player.get((Player.user_id == user.id) & (Player.dealer == dealer))
        hand = Hand.get((Hand.player_id == player.id) & (Hand.active == True))
        return json.loads(hand.cards)

    def getTotal(self, user, dealer):
        player = Player.get((Player.user_id == user.id) & (Player.dealer == dealer))
        hand = Hand.get((Hand.player_id == player.id) & (Hand.active == True))
        cards = json.loads(hand.cards)
        handCount = 0
        for card in cards:
            handCount += card[1]


        return handCount

    def count(self, user, dealer):
        player = Player.get((Player.user_id == user.id) & (Player.dealer == dealer))
        hand = Hand.get((Hand.player_id == player.id) & (Hand.active == True))
        bet = int(hand.bet)
        cards = json.loads(hand.cards)
        handCount = 0

        for card in cards:
            handCount += card[1]

        handTotal = hasAce(cards, handCount)

        message = ''

        if handTotal > 21:
            message = "*You busted!* :cry: :cry:  You lose " +str(bet)+ '\n \n *Up for another hand??*\n If so, `~bet` again! :smile:' #if another hand, close the one, play the other
            player.player_state = 0
            player.save()


        elif handTotal == 21:
            message = ":warning::moneybag: BLACKJACK!! :moneybag::warning: \n You win $"  +str(int(bet*1.5)) + '\n `~bet` again??' #if another hand, play it, close the old, play the other
            hand.bet = 0
            player.cash = int(player.cash) + int(bet*3)
            player.player_state = 0
            player.save()


        elif handTotal < 22:
            options = ''
            if len(cards)== 2:
                player.player_state = 2
                options = "You can `~double down` `~stay` or `~hit`"
                if cards[0][2] == cards[1][2]:
                    options += " `split` "
                    player.player_state = 3
            elif player.player_state == 4:
                 options = "'You *doubled down*, gotta wait and see what the dealer gets :simple_smile: :simple_smile:'"
            else:
                options = "You can `~stay` or `~hit`"
            player.save()
            message = options
            print('options', options)

        return message, handTotal
