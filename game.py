from deck import Deck
from player import Player

class GoFishGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = [Player(f"Player {i+1}") for i in range(num_players)]
        self.deck = Deck()
        self.deck.shuffle()
        self.deal_initial_cards()

    def deal_initial_cards(self):
        num_cards_per_player = 5
        for player in self.players:
            player.draw(self.deck.deal(num_cards_per_player))

    def take_turn(self, current_player, other_player):
        print(f"{current_player.name}, it's your turn.")
        print("Your hand:")
        for card in current_player.hand:
            print(card)

        while True:
            if not current_player.hand:
                print("Oops! You have no cards left.")
                return

            rank_input = input("Enter a rank to ask for (1-13): ")
            if rank_input.strip():  # Check if the input is not empty
                try:
                    rank = int(rank_input)
                    if 1 <= rank <= 13:
                        break
                    else:
                        print("Invalid rank. Please enter a number between 1 and 13.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            else:
                print("Please enter a rank.")

        if not other_player.hand:
            print("Oops! The other player has no cards left.")
            return

        if current_player.ask(other_player, rank):
            print("Success! You got a card.")
        else:
            print("Go fish!")
            drawn_card = self.deck.deal(1)
            if drawn_card:
                current_player.draw(drawn_card)
            else:
                print("Oops! The deck is empty.")


    def play(self):
        print("Super Awesome Go Fish Game!!!")
        current_player_idx = 0
        while True:
            current_player = self.players[current_player_idx]
            other_player = self.players[(current_player_idx + 1) % self.num_players]
            self.take_turn(current_player, other_player)
            if self.check_game_over():
                break
            current_player_idx = (current_player_idx + 1) % self.num_players
        self.display_results()

    def check_game_over(self):
        total_matches = sum(player.check_for_matches() for player in self.players)
        print(f"Total matches: {total_matches}")
        return total_matches == 13


    def display_results(self):
        print("\nGame Over!")
        for player in self.players:
            print(f"{player.name} score:", player.check_for_matches())

if __name__ == "__main__":
    num_players = int(input("Enter the number of players: "))
    game = GoFishGame(num_players)
    game.play()
