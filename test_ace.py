#test for handleAce()
from itertools import *
import unittest
from ace import get_high_and_low, low_count, high_count, reverse_sort, choose_best, handle_ace

class testAce(unittest.TestCase):
    hand1 = [["spades", 1, "ace"], ["hearts", 1, "ace"], ["diamonds", 1,"ace"], ["clubs", 1, "ace"]]
    results1 = ((1, 11), (2, 12), (3, 13), (4, 14))
    hand2 = [["", 10, ""], ["", 1, ""], ["", 10, ""]]
    results2 = ((10, 10), (11, 21), (21, 31))
    hand3 = [["", 1, ""], ["", 5,""], ["", 1, ""], ["", 10, ""]]
    results3 = ((1, 11), (6, 16), (7, 17), (17, 27))
    all_hands = hand1, hand2, hand3
    all_results = results1, results2, results3
    reverse_hand_3 = [["", 1, ""],["", 1,""],["", 5, ""],["", 10, ""]]
    best = [14,21,17]
    #known_values = (#test the outcome of each hand

    def test_low_count(self): #these currently don't work at all.  would be a good idea to print in general to see what they are actually doing
        """returns lowest possible hand"""
        for hand, results in zip(self.all_hands, self.all_results):
            answer = low_count(hand)
            self.assertEqual(results[-1][0], answer)

    def test_high_count(self):
        """returns highest possible hand"""
        for hand, results in zip(self.all_hands, self.all_results):
            answer = high_count(hand)
            self.assertEqual(results[-1][1], answer)

    def test_get_high_and_low(self):
        for hand, results in zip(self.all_hands, self.all_results):
            self.assertEqual(results[-1][0], get_high_and_low(hand)[0])
            self.assertEqual(results[-1][1], get_high_and_low(hand)[1])

    def test_reverse_sort(self):
        reverse = reverse_sort(self.hand3)
        for card1, card2 in zip(reverse, self.reverse_hand_3):
            self.assertEqual(card1[1], card2[1])

    def test_choose_best(self):
        for hand, bestest in zip(self.all_hands, self.best):
            low, high = get_high_and_low(hand)
            best = choose_best(low, high)
            self.assertEqual(best, bestest)

    def test_handle_ace(self):
        count = 0
        for hand, result in zip(self.all_hands, self.all_results):
            low, high, best = handle_ace(hand)
            self.assertEqual(result[-1][0], low )
            self.assertEqual(result[-1][1], high)
            self.assertEqual(self.best[count], best )
            count+=1

if __name__ == '__main__':
    unittest.main()
