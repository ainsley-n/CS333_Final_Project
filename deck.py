import random
from card import Card

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:
            for rank in range(1, 14):
                self.cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        dealt_cards = []
        for _ in range(num_cards):
            if self.cards:
                dealt_cards.append(self.cards.pop())
            else:
                print("Error: Deck is empty. Cannot deal cards.")
                return None  # Return None or handle the empty deck condition appropriately
        return dealt_cards