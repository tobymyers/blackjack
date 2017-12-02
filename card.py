class Card:
    def __init__(self, suit, number, name):

        #need to validate that cards are valid
        suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
        numbers = [1,2,3,4,5,6,7,8,9,10]
        names = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]

#this validatation isn't great b/c you can still create a card, it will just be a BS one.  No error will actually be thrown
        if suit in suits:
            self.suit = suit
        else:
            self.suit = "invalid suit"

        if number in numbers:
            self.number = number
        else:
            self.number = "invalid number"

        if name in names:
            self.name = name
        else:
            self.name = "invalid name"

    def get_card(self):
        return self.suit, self.number, self.name
