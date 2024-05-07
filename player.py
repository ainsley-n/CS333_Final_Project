
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw(self, cards):
        self.hand.extend(cards)

    def ask(self, other_player, rank):
        matching_cards = [card for card in other_player.hand if card.rank == rank]
        if matching_cards:
            other_player.hand = [card for card in other_player.hand if card.rank != rank]
            self.hand.extend(matching_cards)
            return True
        else:
            return False

    def check_for_matches(self):
        ranks_count = {}
        for card in self.hand:
            if card.rank in ranks_count:
                ranks_count[card.rank] += 1
            else:
                ranks_count[card.rank] = 1
        matches = [rank for rank, count in ranks_count.items() if count == 4]
        for rank in matches:
            self.hand = [card for card in self.hand if card.rank != rank]
        return len(matches)
