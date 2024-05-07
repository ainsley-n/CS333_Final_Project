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

class TestGoFishIntegration(unittest.TestCase):
    def setUp(self):
        # Create a game with 2 players for testing
        self.game = GoFishGame(2)

    def test_initial_deal(self):
        # Test if the correct number of cards is dealt to each player initially
        for player in self.game.players:
            self.assertEqual(len(player.hand), 5)

    def test_turn_logic_successful_ask(self):
        # Set up a controlled state for testing a successful ask
        current_player = self.game.players[0]
        other_player = self.game.players[1]
        current_player.hand = [Card(4, 'Hearts')]
        other_player.hand = [Card(4, 'Clubs'), Card(4, 'Diamonds')]

        # Simulate asking for rank 4
        current_player.ask(other_player, 4)

        # Check if the current player now has three cards of rank 4
        self.assertEqual(len(current_player.hand), 3)

    def test_turn_logic_go_fish(self):
        # Clear the hands to establish a controlled "Go Fish" scenario
        for player in self.game.players:
            player.hand = []

        # Set up known initial states for the players' hands
        current_player = self.game.players[0]
        other_player = self.game.players[1]
        current_player.hand = [Card(4, 'Hearts')]
        other_player.hand = [Card(2, 'Diamonds')]

        # Store the initial deck size for verification after drawing
        initial_deck_size = len(self.game.deck.cards)

        # Simulate asking for a rank that isn't available in the other player's hand
        successful = current_player.ask(other_player, 4)

        # Ensure the "ask" action fails (thus causing "Go Fish")
        self.assertFalse(successful)

        # Manually simulate drawing from the deck as "Go Fish" requires
        drawn_card = self.game.deck.deal(1)
        if drawn_card:
            current_player.draw(drawn_card)

        # Verify that one card was drawn from the deck
        self.assertEqual(len(self.game.deck.cards), initial_deck_size - 1)

        # Verify that the current player's hand has one additional card
        self.assertEqual(len(current_player.hand), 2)


    def test_match_detection(self):
        # Set up a controlled state for testing a match detection
        current_player = self.game.players[0]
        current_player.hand = [
            Card(7, 'Hearts'),
            Card(7, 'Diamonds'),
            Card(7, 'Clubs'),
            Card(7, 'Spades')
        ]

        # Check for matches
        num_matches = current_player.check_for_matches()

        # Ensure one match is detected and the hand is empty
        self.assertEqual(num_matches, 1)
        self.assertEqual(len(current_player.hand), 0)

    def test_end_game_condition(self):
        # Simulate the end-game condition by manually setting all matches
        current_player = self.game.players[0]
        other_player = self.game.players[1]
        current_player.matches = list(range(1, 7))  # First 6 matches
        other_player.matches = list(range(7, 14))  # Remaining matches

        # Check if the game over condition is detected
        self.assertTrue(self.game.check_game_over())
class TestCardDeckIntegration(unittest.TestCase):
    def setUp(self):
        # Create a new deck before each test
        self.deck = Deck()

    def test_deck_contains_all_cards(self):
        # Ensure that the deck contains the correct number of cards (52)
        self.assertEqual(len(self.deck.cards), 52)

        # Verify that all ranks and suits are represented correctly
        ranks = range(1, 14)
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        expected_cards = {f"{rank} of {suit}" for rank in ranks for suit in suits}

        actual_cards = {str(card) for card in self.deck.cards}

        # Compare the set of expected card descriptions to actual cards in the deck
        self.assertEqual(expected_cards, actual_cards)

    def test_deck_shuffle(self):
        # Store the original order for comparison
        original_order = self.deck.cards[:]
        self.deck.shuffle()

        # Ensure that the deck has been shuffled, meaning the order should be different
        self.assertNotEqual(original_order, self.deck.cards)

    def test_draw_cards_from_deck(self):
        # Ensure that drawing cards reduces the number of cards in the deck
        initial_size = len(self.deck.cards)
        drawn_cards = self.deck.deal(5)

        # Verify the number of drawn cards
        self.assertEqual(len(drawn_cards), 5)

        # Check that the deck size has reduced by 5
        self.assertEqual(len(self.deck.cards), initial_size - 5)

        # Verify that the drawn objects are instances of Card
        for card in drawn_cards:
            self.assertIsInstance(card, Card)

if __name__ == '__main__':
    unittest.main()
