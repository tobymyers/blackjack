class Card:
    def __init__(self, suit, number, name):
        self.suit = suit
        self.number = number
        self.name = name

    def getCard(self):
        return self.suit, self.number, self.name
