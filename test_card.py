#test card
import unittest
from card import *



class CardTest(unittest.TestCase):

    test_cards = [["Spades", 2, "King"], ["Silly Suit", 1, "Queen"], ["Hearts", 'one', "Ten"], ["Clubs", 4, "Joker"]]
    known_results = [("Spades", 2, "King"), ("invalid suit", 1 ,"Queen"), ("Hearts", "invalid number", "Ten"), ("Clubs", 4, "invalid name")]

    def test_card(self):
        for card, result in zip(self.test_cards, self.known_results):
            c = Card(card[0], card[1], card[2])
            x = c.get_card()
            self.assertEqual(x, result)
if __name__ == '__main__':
    unittest.main()
