import unittest
from deck import Deck
from card import Card
from player import Player
from unittest.mock import patch
from game import GoFishGame


class TestUnit(unittest.TestCase):
    def test_build_deck(self):
        # Test that when deck is built it has 52 cards
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_shuffle_deck(self):
        # Ensure shuffled deck != original deck
        deck = Deck()
        original_order = deck.cards[:]
        deck.shuffle()
        self.assertNotEqual(original_order, deck.cards)

    def test_deal_cards(self):
        # Ensure number of cards delt == 5
        deck = Deck()
        num_cards = 5
        dealt_cards = deck.deal(num_cards)
        self.assertEqual(len(dealt_cards), num_cards)

    def test_card_creation(self):
        # Ensure cards are created properly
        card = Card(5, 'Hearts')
        self.assertEqual(str(card), "5 of Hearts")

    def setUp(self):
        # Set up test player for further testing
        self.player = Player("TestPlayer")

    def test_player_draw(self):
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

    @patch('builtins.input', side_effect=['11'])
    def test_take_turn(self, mock_input):
        # Ensure the turn taking aspect is correct
        game = GoFishGame(2)
        current_player = game.players[0]
        other_player = game.players[1]

        self.assertTrue(current_player.hand)

        game.take_turn(current_player, other_player)

        self.assertNotEqual(len(current_player.hand), 0)


class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Create a game with 2 players and new deck for testing
        self.game = GoFishGame(2)
        self.deck = Deck()

    def test_initial_deal(self):
        # Test if the correct number of cards is dealt to each player initially
        for player in self.game.players:
            self.assertEqual(len(player.hand), 5)

    def test_turn_logic_successful_ask(self):
        # Set up a controlled game state for testing a successful ask
        current_player = self.game.players[0]
        other_player = self.game.players[1]
        current_player.hand = [Card(4, 'Hearts')]
        other_player.hand = [Card(4, 'Clubs'), Card(4, 'Diamonds')]

        current_player.ask(other_player, 4)

        self.assertEqual(len(current_player.hand), 3)

    def test_turn_logic_go_fish(self):
        # Set up controlled player hand to ensure game ask action and player deck responds properly
        for player in self.game.players:
            player.hand = []

        current_player = self.game.players[0]
        other_player = self.game.players[1]
        current_player.hand = [Card(4, 'Hearts')]
        other_player.hand = [Card(2, 'Diamonds')]

        initial_deck_size = len(self.game.deck.cards)

        successful = current_player.ask(other_player, 4)

        self.assertFalse(successful)

        drawn_card = self.game.deck.deal(1)
        if drawn_card:
            current_player.draw(drawn_card)

        self.assertEqual(len(self.game.deck.cards), initial_deck_size - 1)

        self.assertEqual(len(current_player.hand), 2)

    def test_match_detection(self):
        # Set up a controlled player hand for testing a match detection
        current_player = self.game.players[0]
        current_player.hand = [
            Card(7, 'Hearts'),
            Card(7, 'Diamonds'),
            Card(7, 'Clubs'),
            Card(7, 'Spades')
        ]

        num_matches = current_player.check_for_matches()

        self.assertEqual(num_matches, 1)
        self.assertEqual(len(current_player.hand), 0)

    def test_deck_contains_all_cards(self):
        # Ensure that the deck contains all the proper cards
        self.assertEqual(len(self.deck.cards), 52)

        ranks = range(1, 14)
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        expected_cards = {f"{rank} of {suit}" for rank in ranks for suit in suits}

        actual_cards = {str(card) for card in self.deck.cards}

        self.assertEqual(expected_cards, actual_cards)

    def test_draw_cards_from_deck(self):
        # Ensure that drawing cards reduces the number of cards in the deck
        initial_size = len(self.deck.cards)
        drawn_cards = self.deck.deal(5)

        self.assertEqual(len(drawn_cards), 5)

        self.assertEqual(len(self.deck.cards), initial_size - 5)

        for card in drawn_cards:
            self.assertIsInstance(card, Card)

    def test_check_game_over(self):
        # Ensure the game is over when all matches are made
        self.assertFalse(self.game.check_game_over())

        current_player = self.game.players[0]
        other_player = self.game.players[1]
        current_player.matches = [1, 2, 3, 4, 5, 6]
        other_player.matches = [7, 8, 9, 10, 11, 12, 13]

        self.assertTrue(self.game.check_game_over())


if __name__ == '__main__':
    unittest.main()
