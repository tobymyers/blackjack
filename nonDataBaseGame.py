from player import *
import time
class Game:
    def __init__(self, name):
        self.name = name

#ask everyone to play blackjack (out)
#someone types start to start the game (in)
    def start(self):
        x = eval(input("would you like to start the game? type ?start "))
        if x == "?start":
            return 1
        else:
            return 0

#create players and dealer
    def createPlayers(self, slackClient):
        count = 0
        players = []
        message = slackClient.rtm_read()
        while True:
            if message[text]=="play":
                player = "player"+str(count)
                playerId = message["user"]
                playerName = message["user"]
                n = Player("p", playerId, playerName)
                players.append(n.getPlayer())
                count+=1
            print(players)
        return players

    #def countHand(self, hand):
    def connect(self):
        self.slack_token = ["xoxb-237318321376-yFZMOQoqAGKBuRD5O0vTkvo4"]
        sc = SlackClient(slack_token)
        if sc.rtm_connect():
            print('connected!')

    def read(self):
        message = sc.rtm_read()
        return message


#while there are cards in the deck
    #bet (in)
    #deal (out)
    #everyone sees dealers card (out)
    #ask each player what to do (in order?) (out)
    #players act (some bust) (in)
    #notify players with what happened (out)
    #dealer plays final card (out)
    #everything evaluated, money exchanged (out)
#play another game? (out)
