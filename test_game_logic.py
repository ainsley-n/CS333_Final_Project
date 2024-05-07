import unittest
from deck import Deck
from card import Card

class TestDeck(unittest.TestCase):
    def test_build_deck(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_shuffle_deck(self):
        deck = Deck()
        original_order = deck.cards[:]
        deck.shuffle()
        self.assertNotEqual(original_order, deck.cards)

    def test_deal_cards(self):
        deck = Deck()
        num_cards = 5
        dealt_cards = deck.deal(num_cards)
        self.assertEqual(len(dealt_cards), num_cards)

class TestCard(unittest.TestCase):
    def test_card_creation(self):
        card = Card(5, 'Hearts')
        self.assertEqual(str(card), "5 of Hearts")

if __name__ == '__main__':
    unittest.main()
