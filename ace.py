
from operator import itemgetter
def reverse_sort(cards):
   return sorted(cards, key = itemgetter(1))

def low_count(cards): #works  gotta wireframe everything out better.  who counts shit up for example?  who determines bust? answer: bust shoudl live in just one place.
   count = 0
   for card in cards:
       value = card[1]
       count += value
   return count

def high_count(cards):
   count = 0
   for card in cards:
       if card[1] == 1 and count <= 10:
           count += 11
       else:
           count+=card[1]
   return count

def get_high_and_low(cards):
   #cards = reverseSort(cards)
   low = low_count(cards)
   high = high_count(cards)
   return low, high

def choose_best(low, high):
    if high <= 22:
        return high
    else:
        return low

def handle_ace(cards):
    cards = reverse_sort(cards)
    low, high = get_high_and_low(cards)
    best = choose_best(low, high)
    return low, high, best





   #choose what to return
   #choose winner (separate from this test)
