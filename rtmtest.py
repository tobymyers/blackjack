import time
import json
import player
from slackclient import SlackClient
from user import *
from blackjackplayer import *
from blackjackhand import *
from blackjackgame import *
from basemodel import *
from deck import *
from convert import toPython
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
#bug log
#date #bug #fix_idea # did it work?
#9/23: #crashes when cash == 0, goes to blank #set to 0 as default value?
#9/24  #if you hit start after bet, hands stay open and don't close if you bet again and bust
    #tighten conditions around start to check for active hands and add end() #it worked!!
#9/24 interprets decimals as whole numbers i.e. 4.5 as 45 #change field type to float for bet
#9/24 posts undoubled bet to slack even when doubled down and subtracts the undoubled bet if you win.  don't know about database.  #probably a chooseWinner problem

print os.environ.get("SLACK_TOKEN");
#token = "xoxb-237318321376-yFZMOQoqAGKBuRD5O0vTkvo4"# found at https://api.slack.com/web#authentication
sc = SlackClient(os.environ.get("SLACK_TOKEN"))

def post(response, channel):
    sc.api_call("chat.postMessage", channel=channel,
                  text=response, as_user=True)

def troll(response, channel):
    sc.api_call("reactions.add", channel = channel, name = response)

def getOrSaveUser(slackId):
    user_info = json.loads(sc.server.api_call('users.info', user=slackId))

    user = User.select().where(User.slack_id == slackId)

    if not user.exists():
        user = User(slack_id = slackId, name = user_info['user']['name'])
        user.save()

    return user.get()

def getOrSaveGame(user):
    game = Game.select().where(Game.active == True)

    if not game.exists():
        game = Game.create(played_cards ='', unplayed_cards = '', active = True, user_id = user.id)

    game = BlackJackGame(game)
    return game

def getInt(message_text):
    nums = ['0','1','2','3','4','5','6','7','8','9']
    ints = ''
    for i in message_text:
        toPython(i)
        if i in nums:
            return True

def getBet(message_text):
    nums = ['0','1','2','3','4','5','6','7','8','9']
    ints = ''
    for i in message_text:
        toPython(i)
        if i in nums:
            ints += i
    return int(ints)


def rightPlayerAndState(user, playerState):
    user_id = user.id
    player = Player.select().where((Player.user_id == user.id)&(Player.dealer == False))
    if player.exists():
        player = Player.get((Player.user_id == user.id)&(Player.dealer == False))
        if player.player_state == playerState:
            return True
        else:
            return False
    return False

def format(cards):
    formatted = ''
    count = 0
    for card in cards:
        #formatted += 'https://deckofcardsapi.com/static/img/'+'{0}{1}'.format(card[2], card[0])+'.png \n'

        formatted += '\n{0}{1}'.format(card[2], card[0])
        count+=card[1]
    count = hasAce(cards, count)
    response =  formatted + '\n*Total:* '+str(count)
    return response

def troll(message_text):
    slackId = message_text.split(" ")[1][2:-1]
    print(slackId)
    trollee = User.get(User.slack_id == slackId)
    trollee.trolled = True
    trollee.save()



def handleMessage(message):
    print(message)

    if 'user' in message and 'text' in message and message['user'] != 'U6Z9C9FB2':
        timestamp = message['ts']
        user = getOrSaveUser(message['user']) #this gets us the user that sent a message, which we need to do every time
        game = BlackJackGame(user) #get all the shit here, once
        channel = message['channel']
        message_text = message['text'] #gets text field from the message sent from slack
        #blackjack gameplay lives here.

        if "~watch" in message_text:
            troll(message_text)

        if user.trolled == True:

            sc.api_call("reactions.add", channel=channel, name="eyes", timestamp=timestamp)

        if '~cash?' in message_text:
            player = BlackJackPlayer(user, False)
            response = 'You have $*'  + str(player.getCash(user)) +'* :moneybag: :moneybag: You can also `add $ amount`'
            post(response, channel)

        elif '~add' in message_text:
            player = BlackJackPlayer(user, False)
            cash = message_text.split(' ')[1]
            player.addCash(user, cash)
            cash = player.getCash(user)
            response = "You now have *$" + str(cash)+ "*"
            post(response, channel)

        elif '~end' in message_text:
            response = game.end(user)
            post(response, channel)

        else:
            if '~start' in message_text:
                if game.activeHands():
                    response = "Looks like you're in the middle of a hand.  \nYou can `end` this game and start a new one if you want, otherwise `hit`, `stay`, or whatever "
                    post(response, channel)
                else:
                    game.makeDeck(user)
                    game.shuffle(user)

                    player = BlackJackPlayer(user, False)
                    player.updateState(user, 0)

                    response = ":woop: :snoop: Ayooo! \nWelcome to BlackJack *"+str(user.name)+'*! :heart_eyes: You have $'+ str(player.getCash(user))+'\n Place your `bet` !* :moneybag:'
                    post(response, channel)


            elif '~bet' in message_text and rightPlayerAndState(user, 0):

                if getInt(message_text):
                    player = BlackJackPlayer(user, False)
                    dealer = BlackJackPlayer(user, True)
                    bet = getBet(message_text)
                    if bet <= int(player.getCash(user)) and bet > 0:

                        player.registerBet(user, bet)

                        response = 'Got your bet *'+str(user.name)+'*! Dealing...'
                        time.sleep(1)
                        post(response, channel)

                        playerHand = BlackJackHand(user, game, bet, False)
                        cards = game.dealCard(2, user)
                        playerHand.addCards(user, cards, False)

                        dealerHand = BlackJackHand(user, game, bet, True)
                        cards = game.dealCard(1, user)
                        dealerHand.addCards(user, cards, True)
                        if hasAce(dealerHand.getCards(user, True), dealerHand.getTotal(user, True)) == 21 or hasAce(playerHand.getCards(user, False), playerHand.getTotal(user, False)) == 21: #this should now be good

                            dealerHand.close(user, True)
                            playerHand.close(user, False)
                        response = "The dealer is showing:\n" + format(dealerHand.getCards(user, True)) + '\n\nYou have:' + format(playerHand.getCards(user, False))
                        post(response, channel)

                        response, handTotal = playerHand.count(user, False)
                        post(response, channel)
                else:
                    response = "Not a valid bet :person_frowning: :person_frowning: \n it's gotta have *a number* and the word `~bet` "
                    post(response, channel)

            #elif rightPlayerAndState(user, 3) and 'split' in message_text:
                #get the hand
                #create a new one
                #split the cards
                #double the bet

            elif rightPlayerAndState(user, 2) or rightPlayerAndState(user, 3):
                if '~stay' in message_text:
                    if False:#there are two active player hands:
                        playerHand = BlackJackHand(user, game, 0, False)
                        nothing, playerTotal = playerHand.count(user, False)
                        #close one hand
                    else:
                        playerHand = BlackJackHand(user, game, 0, False)
                        nothing, playerTotal = playerHand.count(user, False) # these two lines we get the new hand

                        dealerHand = BlackJackHand(user, game, 0, True)

                        message, dealerTotal = dealerHand.count(user, True)
                    while dealerTotal < 17:
                        card = game.dealCard(1, user)
                        dealerHand.addCards(user, card, True)
                        message, dealerTotal = dealerHand.count(user, True)
                        response = 'Dealer draws' + format(card)
                        post(response, channel)
                        time.sleep(1)

                    response = "*Dealer final hand:*" + format(dealerHand.getCards(user, True))
                    post(response, channel)

                    response = game.chooseWinner(user, dealerTotal, playerTotal) #
                    post(response, channel)
                    player = BlackJackPlayer(user, False)
                    player.updateState(user, 0)
                    dealerHand.close(user, True)
                    playerHand.close(user, False)

                elif '~hit' in message_text:
                    playerHand = BlackJackHand(user, game, 0, False)
                    dealerHand = BlackJackHand(user, game, 0, True)
                    card = game.dealCard(1, user)
                    playerHand.addCards(user, card, False)
                    response = 'You draw a ' + format(card)
                    post(response, channel)

                    response = 'Your hand is ' + format(playerHand.getCards(user, False))
                    post(response, channel)

                    response, playerTotal = playerHand.count(user, False)
                    post(response, channel)
                    if playerTotal >= 21:
                        playerHand.close(user, False)
                        dealerHand.close(user, True)



                elif '~double down' in message_text:
                    player = BlackJackPlayer(user, False)
                    player.updateState(user, 4)
                    playerHand = BlackJackHand(user, game, 0, False)
                    dealerHand = BlackJackHand(user, game, 0, True)
                    bet = playerHand.getBet(user, False)
                    newBet = int(bet * 2)
                    playerHand.changeBet(user, False, newBet)
                    player.registerBet(user, newBet)
                    response = "You've doubled your bet to $*"+str(newBet)+"*\n:muscle: *Bold move* :muscle:"
                    post(response, channel)
                    card = game.dealCard(1, user)
                    playerHand.addCards(user, card, False)
                    response = 'You draw a ' + format(card)
                    post(response, channel)
                    response = 'Your hand is ' + format(playerHand.getCards(user, False))
                    post(response, channel)
                    response, playerTotal = playerHand.count(user, False)
                    post(response, channel)
                    player = BlackJackPlayer(user, False)
                    player.updateState(user, 0)

                    if playerTotal < 21:
                        message, dealerTotal = dealerHand.count(user, True)
                        while dealerTotal < 17:
                            card = game.dealCard(1, user)
                            dealerHand.addCards(user, card, True)
                            message, dealerTotal = dealerHand.count(user, True)
                            response = 'Dealer draws' + format(card)
                            post(response, channel)
                            time.sleep(1)
                        #post entire hand
                        response = "*Dealer final hand:*" + format(dealerHand.getCards(user, True))
                        post(response, channel)

                        response = game.chooseWinner(user, dealerTotal, playerTotal)
                        post(response, channel)

                    dealerHand.close(user, True)
                    playerHand.close(user, False)

if sc.rtm_connect():
    db.connect()
    #db.create_tables([Player, User, Hand, Game])
    while True:
        message = sc.rtm_read()
        if message and len(message) > 0:
            for output in message:
                if output and 'text':
                    handleMessage(output)


        # print message

        # handle_message(message)
    time.sleep(1)
else:
    print "Connection Failed, invalid token?"
