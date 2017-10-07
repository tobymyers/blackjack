#learning_inheritance
from blackjackhand import BlackJackHand
from player import *
from hand import *
from game import *
from blackjackgame import *
from blackjackplayer import *
import json


#i create a hand, assign it self.hand, alter it, then return self.hand
#if I get the unaltered version, it's saving a static version of the hand in self.hand
#if I get the altered version, every time I ask for self.hand it uses the query in the constructor
  #this is good b/c that way I don't have to do so much querying, I can just construct it once and then use the instance variables

my_user = User(slack_id = 1234, name = "toby's hand", trolled = False)
my_user.save()
my_game = BlackJackGame(my_user)
my_player = BlackJackPlayer(my_user, False)
my_hand = BlackJackHand(my_user, my_game, 0, False)
print(my_hand.hand.active, "active1")
my_hand.close2()
print(my_hand.hand.active, "active2")

#inheritance happens here!  every time I ask for self.hand, it executes the query and gives me the most updated version!
#this means that I can instantiate self.everything in the __init__ and then not fuck with the Python going forward!
#should have done a branch here
