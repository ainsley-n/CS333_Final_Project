import unittest
from deck import Deck
from card import Card
from player import Player
from unittest.mock import patch
from game import GoFishGame

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
        

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestPlayer")

    def test_draw(self):
        # Test if player can draw cards
        cards = [Card(rank=2, suit='Hearts'), Card(rank=5, suit='Clubs')]
        self.player.draw(cards)
        self.assertEqual(len(self.player.hand), 2)

    def test_ask_successful(self):
        # Test if player can successfully ask for a card
        other_player = Player("OtherPlayer")
        other_player.draw([Card(rank=2, suit='Hearts')])
        self.player.draw([Card(rank=2, suit='Clubs')])
        self.assertTrue(self.player.ask(other_player, 2))
        self.assertEqual(len(self.player.hand), 2)

    def test_ask_unsuccessful(self):
        # Test if player cannot ask for a card they dont have
        other_player = Player("OtherPlayer")
        other_player.draw([Card(rank=6, suit='Hearts')])
        self.player.draw([Card(rank=2, suit='Clubs')])
        self.assertFalse(self.player.ask(other_player, 3))
        self.assertEqual(len(self.player.hand), 1)

    def test_check_for_matches(self):
        # Test if player can correctly identify and remove matches from their hand
        self.player.draw([Card(rank=2, suit='Hearts'), Card(rank=2, suit='Clubs'),
                           Card(rank=2, suit='Diamonds'), Card(rank=2, suit='Spades')])
        num_matches = self.player.check_for_matches()
        self.assertEqual(num_matches, 1)
        self.assertEqual(len(self.player.hand), 0)


class TestGoFishGame(unittest.TestCase):
    
    def setUp(self):
        self.game = GoFishGame(2) 

    def test_check_game_over(self):
        # Ensure that the game is not over at the beginning
        self.assertFalse(self.game.check_game_over())

        # Manually set up the game to simulate the end condition
        current_player = self.game.players[0]
        other_player = self.game.players[1]
        current_player.matches = [1, 2, 3, 4, 5, 6]
        other_player.matches = [7, 8, 9, 10, 11, 12, 13]
        
        # Ensure the game is over when all matches are made
        self.assertTrue(self.game.check_game_over())
        
    @patch('builtins.input', side_effect=['11'])
    def test_take_turn(self, mock_input):
        current_player = self.game.players[0]
        other_player = self.game.players[1]

        # Ensure that the players hand is not empty before taking a turn
        self.assertTrue(current_player.hand)

        # Run take_turn method
        self.game.take_turn(current_player, other_player)

        # Ensure that the players hand changes after the turn
        self.assertNotEqual(len(current_player.hand), 0)


if __name__ == '__main__':
    unittest.main()
